"""Module d'extraction automatique d'actions/objectifs depuis les conversations."""

import os
import json
from typing import List, Dict, Optional
from anthropic import Anthropic

from src.utils.prompts import ACTION_EXTRACTION_PROMPT
from src.database.db_manager import DatabaseManager


class ActionExtractor:
    """Extrait automatiquement les actions et objectifs des conversations."""

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialiser l'extracteur d'actions.

        Args:
            db_manager: Instance du gestionnaire de base de données.
        """
        self.db_manager = db_manager
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def extract_actions_from_message(
        self, user_message: str, user_id: int, conversation_id: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Extraire les actions/objectifs d'un message utilisateur.

        Args:
            user_message: Message de l'utilisateur à analyser.
            user_id: ID de l'utilisateur.
            conversation_id: ID de la conversation (optionnel).

        Returns:
            Liste des actions extraites et sauvegardées.
        """
        try:
            # Appel à l'API Claude pour extraction
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=ACTION_EXTRACTION_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )

            # Parser la réponse JSON
            response_text = response.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                # Extract JSON from markdown code block
                lines = response_text.split("\n")
                response_text = "\n".join(
                    line for line in lines if not line.startswith("```")
                )

            result = json.loads(response_text)
            extracted_actions = result.get("actions", [])

            # Sauvegarder les actions comme propositions dans la base de données
            saved_proposals = []
            for action in extracted_actions:
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

            return saved_proposals

        except json.JSONDecodeError as e:
            print(f"Erreur de parsing JSON: {e}")
            print(f"Réponse reçue: {response_text}")
            return []
        except Exception as e:
            print(f"Erreur lors de l'extraction d'actions: {e}")
            return []

    def extract_actions_batch(
        self, conversations: List[Dict], user_id: int
    ) -> List[Dict[str, str]]:
        """
        Extraire des actions depuis plusieurs conversations (traitement par batch).

        Args:
            conversations: Liste de dicts contenant 'id' et 'user_message'.
            user_id: ID de l'utilisateur.

        Returns:
            Liste de toutes les actions extraites.
        """
        all_actions = []

        for conv in conversations:
            actions = self.extract_actions_from_message(
                user_message=conv.get("user_message", ""),
                user_id=user_id,
                conversation_id=conv.get("id"),
            )
            all_actions.extend(actions)

        return all_actions
