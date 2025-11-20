"""Gestionnaire de conversations avec l'API Claude."""

import os
from typing import Generator
from anthropic import Anthropic
import anthropic
from src.database.db_manager import DatabaseManager
from src.utils.prompts import CONVERSATION_SYSTEM_PROMPT, CRISIS_KEYWORDS


class ConversationManager:
    """Gestionnaire de conversations avec Claude API."""

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialiser le gestionnaire de conversations.

        Args:
            db_manager: Instance de DatabaseManager pour la persistance.

        Raises:
            ValueError: Si ANTHROPIC_API_KEY n'est pas définie.
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.client = Anthropic(api_key=api_key)
        self.db = db_manager
        self.system_prompt = CONVERSATION_SYSTEM_PROMPT

    def send_message(self, user_id: int, user_message: str) -> Generator[str, None, None]:
        """
        Envoyer un message à Claude avec streaming.

        Args:
            user_id: ID de l'utilisateur.
            user_message: Message de l'utilisateur.

        Yields:
            Chunks de texte de la réponse (streaming).

        Raises:
            Exception: En cas d'erreur API (retourne message d'erreur convivial).
        """
        try:
            with self.client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=self.system_prompt,
                messages=[{"role": "user", "content": user_message}]
            ) as stream:
                response_text = ""
                for text in stream.text_stream:
                    response_text += text
                    yield text

                # Sauvegarder après complétion
                usage = stream.get_final_message().usage
                tokens = usage.input_tokens + usage.output_tokens
                self.db.save_conversation(user_id, user_message, response_text, tokens)

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
