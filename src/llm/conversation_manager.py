"""Gestionnaire de conversations avec l'API Claude."""

import os
from typing import Generator, List, Dict
from anthropic import Anthropic
import anthropic
from src.database.db_manager import DatabaseManager
from src.utils.prompts import CONVERSATION_SYSTEM_PROMPT, CRISIS_KEYWORDS


class ConversationManager:
    """Gestionnaire de conversations avec Claude API."""

    # Configuration de la gestion du contexte
    MAX_CONTEXT_TOKENS = 180000  # Limite de sécurité (Claude-4 supporte 200k)
    MAX_HISTORY_MESSAGES = 50  # Nombre maximum de messages à récupérer
    MIN_RECENT_MESSAGES = 10  # Toujours garder les N derniers messages

    def __init__(self, db_manager: DatabaseManager, enable_action_extraction: bool = True):
        """
        Initialiser le gestionnaire de conversations.

        Args:
            db_manager: Instance de DatabaseManager pour la persistance.
            enable_action_extraction: Activer l'extraction automatique d'actions (défaut: True).

        Raises:
            ValueError: Si ANTHROPIC_API_KEY n'est pas définie.
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.client = Anthropic(api_key=api_key)
        self.db = db_manager
        self.system_prompt = CONVERSATION_SYSTEM_PROMPT
        self.enable_action_extraction = enable_action_extraction
        self.action_extractor = None

        # Lazy load action extractor pour éviter import circulaire
        if enable_action_extraction:
            from src.llm.action_extractor import ActionExtractor
            self.action_extractor = ActionExtractor(db_manager)

    def _estimate_tokens(self, text: str) -> int:
        """
        Estimer le nombre de tokens dans un texte.

        Règle approximative : ~4 caractères = 1 token pour le français.

        Args:
            text: Texte à analyser.

        Returns:
            Nombre estimé de tokens.
        """
        return len(text) // 4

    def _build_conversation_context(self, user_id: int, current_message: str) -> List[Dict[str, str]]:
        """
        Construire le contexte de conversation avec gestion intelligente de la limite de tokens.

        Args:
            user_id: ID de l'utilisateur.
            current_message: Message actuel de l'utilisateur.

        Returns:
            Liste de messages formatés pour l'API Claude (role + content).
        """
        # Récupérer l'historique depuis la base de données
        history = self.db.get_conversation_history(user_id, limit=self.MAX_HISTORY_MESSAGES)

        # Construire les messages alternés user/assistant
        messages = []
        cumulative_tokens = self._estimate_tokens(self.system_prompt)

        for conv in history:
            user_msg = {"role": "user", "content": conv['user_message']}
            assistant_msg = {"role": "assistant", "content": conv['ai_response']}

            # Estimer les tokens pour ces messages
            msg_tokens = self._estimate_tokens(conv['user_message']) + \
                        self._estimate_tokens(conv['ai_response'])

            # Vérifier si on peut ajouter ces messages sans dépasser la limite
            if cumulative_tokens + msg_tokens < self.MAX_CONTEXT_TOKENS or \
               len(messages) < self.MIN_RECENT_MESSAGES * 2:  # Toujours garder minimum messages
                messages.append(user_msg)
                messages.append(assistant_msg)
                cumulative_tokens += msg_tokens
            else:
                # On a atteint la limite, arrêter d'ajouter des messages plus anciens
                break

        # Ajouter le message actuel
        current_tokens = self._estimate_tokens(current_message)
        messages.append({"role": "user", "content": current_message})
        cumulative_tokens += current_tokens

        # Log pour debugging (optionnel)
        print(f"📊 Contexte construit: {len(messages)} messages, ~{cumulative_tokens} tokens estimés")

        return messages

    def send_message(self, user_id: int, user_message: str) -> Generator[str, None, None]:
        """
        Envoyer un message à Claude avec streaming et contexte complet.

        Args:
            user_id: ID de l'utilisateur.
            user_message: Message de l'utilisateur.

        Yields:
            Chunks de texte de la réponse (streaming).

        Raises:
            Exception: En cas d'erreur API (retourne message d'erreur convivial).
        """
        try:
            # Construire le contexte complet de la conversation
            messages = self._build_conversation_context(user_id, user_message)

            # Envoyer avec l'historique complet
            with self.client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,  # Augmenté pour des réponses plus complètes
                system=self.system_prompt,
                messages=messages  # ✅ Contexte complet !
            ) as stream:
                response_text = ""
                for text in stream.text_stream:
                    response_text += text
                    yield text

                # Sauvegarder après complétion
                usage = stream.get_final_message().usage
                tokens = usage.input_tokens + usage.output_tokens
                conversation_id = self.db.save_conversation(
                    user_id, user_message, response_text, tokens
                )

                # Extraire les actions automatiquement
                if self.enable_action_extraction and self.action_extractor:
                    try:
                        self.action_extractor.extract_actions_from_message(
                            user_message, user_id, conversation_id
                        )
                    except Exception as e:
                        print(f"Erreur extraction d'actions: {e}")
                        # Ne pas bloquer la conversation si l'extraction échoue

        except Exception as e:
            error_msg = "Je suis désolé, je rencontre des difficultés techniques. Veuillez réessayer."
            # Log l'erreur pour debugging
            print(f"API Error: {e}")
            yield error_msg

    def detect_crisis(self, message: str) -> bool:
        """
        Détecter les mots-clés de crise dans un message.

        Args:
            message: Message de l'utilisateur.

        Returns:
            True si un mot-clé de crise est détecté, False sinon.
        """
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in CRISIS_KEYWORDS)
