"""Module de suggestion d'actions personnalisées par l'IA."""

import os
import json
from typing import List, Dict, Optional
from anthropic import Anthropic

from src.utils.prompts import ACTION_SUGGESTION_PROMPT
from src.database.db_manager import DatabaseManager


class ActionSuggester:
    """Suggère des actions personnalisées basées sur l'historique de l'utilisateur."""

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialiser le suggestionneur d'actions.

        Args:
            db_manager: Instance du gestionnaire de base de données.
        """
        self.db_manager = db_manager
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def _build_context(self, user_id: int) -> str:
        """
        Construire le contexte utilisateur pour les suggestions.

        Args:
            user_id: ID de l'utilisateur.

        Returns:
            Contexte formaté pour le prompt.
        """
        # Récupérer les check-ins récents (7 derniers jours)
        recent_checkins = self.db_manager.get_checkins(user_id, limit=7)

        # Récupérer les conversations récentes
        recent_conversations = self.db_manager.get_recent_conversations(user_id, limit=5)

        # Récupérer les actions en cours et complétées
        active_actions = self.db_manager.get_action_items(user_id, status="in_progress", limit=10)
        completed_actions = self.db_manager.get_action_items(user_id, status="completed", limit=5)

        # Formater le contexte
        context = "CONTEXTE UTILISATEUR:\n\n"

        # Check-ins
        if recent_checkins:
            context += "📊 Check-ins récents:\n"
            for checkin in recent_checkins:
                mood = checkin.get("mood_score", "N/A")
                notes = checkin.get("notes", "")
                context += f"- Humeur: {mood}/10"
                if notes:
                    context += f" | Notes: {notes[:100]}"
                context += "\n"
            context += "\n"

        # Conversations
        if recent_conversations:
            context += "💭 Extraits de conversations récentes:\n"
            for conv in recent_conversations[:3]:  # Limiter à 3 conversations
                user_msg = conv.get("user_message", "")[:200]  # Limiter la longueur
                context += f"- {user_msg}\n"
            context += "\n"

        # Actions en cours
        if active_actions:
            context += "⏳ Actions en cours:\n"
            for action in active_actions:
                context += f"- {action['title']}\n"
            context += "\n"

        # Actions complétées
        if completed_actions:
            context += "✅ Actions récemment complétées:\n"
            for action in completed_actions:
                context += f"- {action['title']}\n"
            context += "\n"

        return context

    def suggest_actions(
        self, user_id: int, conversation_id: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Suggérer des actions personnalisées pour l'utilisateur.

        Args:
            user_id: ID de l'utilisateur.
            conversation_id: ID de la conversation (optionnel).

        Returns:
            Dict contenant le message et les actions suggérées, ou None en cas d'erreur.
        """
        try:
            # Construire le contexte
            context = self._build_context(user_id)

            # Appel à l'API Claude pour génération de suggestions
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=ACTION_SUGGESTION_PROMPT,
                messages=[{"role": "user", "content": context}],
            )

            # Parser la réponse JSON
            response_text = response.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(
                    line for line in lines if not line.startswith("```")
                )

            result = json.loads(response_text)

            # Sauvegarder les suggestions comme propositions
            message = result.get("message", "")
            suggested_actions = result.get("actions", [])

            saved_proposals = []
            for action in suggested_actions:
                if action.get("title"):
                    proposal_id = self.db_manager.save_proposed_action(
                        user_id=user_id,
                        title=action["title"],
                        description=action.get("description", ""),
                        conversation_id=conversation_id,
                    )

                    saved_proposals.append(
                        {
                            "id": proposal_id,
                            "title": action["title"],
                            "description": action.get("description", ""),
                        }
                    )

            return {
                "message": message,
                "proposals": saved_proposals,
                "count": len(saved_proposals),
            }

        except json.JSONDecodeError as e:
            print(f"Erreur de parsing JSON: {e}")
            print(f"Réponse reçue: {response_text}")
            return None
        except Exception as e:
            print(f"Erreur lors de la suggestion d'actions: {e}")
            return None
