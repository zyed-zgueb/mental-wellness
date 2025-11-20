"""Générateur d'insights IA adaptatifs pour le bien-être mental."""

import os
import json
from typing import Optional
from datetime import datetime, timedelta
from anthropic import Anthropic
from src.database.db_manager import DatabaseManager
from src.utils.prompts import INSIGHTS_SYSTEM_PROMPT

# =========================
# Global constants
# =========================

REGENERATE_INSIGHTS_AFTER_HOURS = 24  # heures

class InsightsGenerator:
    """
    Générateur d'insights IA avec logique adaptative et cache.
    La durée du cache en heures est dans REGENERATE_INSIGHTS_AFTER_HOURS
    """

    def __init__(self, db_manager: DatabaseManager, user_id: int):
        """
        Initialiser le générateur d'insights.

        Args:
            db_manager: Instance de DatabaseManager pour la persistance.
            user_id: ID de l'utilisateur pour lequel générer les insights.

        Raises:
            ValueError: Si ANTHROPIC_API_KEY n'est pas définie.
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.client = Anthropic(api_key=api_key)
        self.db = db_manager
        self.user_id = user_id

    def get_adaptive_insight(self) -> str:
        """
        Récupérer un insight adaptatif (cached ou nouveau).

        Cette méthode vérifie d'abord si un insight récent existe (voir REGENERATE_INSIGHTS_AFTER_HOURS).
        Si oui, elle le retourne. Sinon, elle génère un nouvel insight adaptatif.

        Returns:
            Insight en format markdown.

        Raises:
            Exception: En cas d'erreur API.
        """
        # Vérifier si régénération nécessaire
        if not self._should_regenerate_insights():
            # Retourner insight cached
            cached = self.db.get_latest_insight(self.user_id, "weekly")
            if cached:
                return cached["content"]

        # Générer nouveau insight
        return self.generate_adaptive_summary()

    def generate_adaptive_summary(self) -> str:
        """
        Générer un nouvel insight adaptatif basé sur les données disponibles.

        Cette méthode:
        1. Récupère les données disponibles (check-ins, conversations)
        2. Détermine le niveau de maturité des données
        3. Construit un prompt adaptatif avec contexte
        4. Appelle Claude API
        5. Sauvegarde l'insight dans la DB

        Returns:
            Insight généré en format markdown.

        Raises:
            Exception: En cas d'erreur API.
        """
        try:
            # Récupérer toutes les données disponibles
            mood_data = self.db.get_mood_history(self.user_id, days=30)
            conv_count = self.db.get_conversation_count(self.user_id, days=30)
            conv_history = self.db.get_conversation_history(self.user_id, limit=10)  # 10 dernières conversations

            # Déterminer niveau de maturité
            # Calculer le nombre de jours depuis le premier check-in
            if mood_data:
                # mood_data est trié du plus récent au plus ancien
                oldest_checkin = datetime.fromisoformat(mood_data[-1]["timestamp"])
                days_with_data = (datetime.now() - oldest_checkin).days + 1  # +1 pour inclure le jour actuel
            else:
                days_with_data = 0

            maturity_level = self._get_data_maturity_level(days_with_data)

            # Construire contexte des données
            data_context = self._build_data_context(mood_data, conv_count, days_with_data, conv_history)

            # Formater le system prompt avec les variables
            system_prompt = INSIGHTS_SYSTEM_PROMPT.format(
                maturity_level=maturity_level,
                days_count=days_with_data
            )

            # Appeler Claude API (pas de streaming pour insights)
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": data_context}]
            )

            # Extraire le contenu
            insight_content = message.content[0].text
            tokens_used = message.usage.input_tokens + message.usage.output_tokens

            # Préparer metadata
            based_on_data = json.dumps({
                "days_count": days_with_data,
                "maturity_level": maturity_level,
                "conv_count": conv_count,
                "avg_mood": self._calculate_avg_mood(mood_data) if mood_data else None
            })

            # Sauvegarder dans DB
            self.db.save_insight(
                self.user_id,
                insight_type="weekly",
                content=insight_content,
                based_on_data=based_on_data,
                tokens_used=tokens_used
            )

            return insight_content

        except Exception as e:
            error_msg = "Je suis désolée, je ne peux pas générer d'insights pour le moment. Veuillez réessayer plus tard."
            print(f"Insights API Error: {e}")
            return error_msg

    def _should_regenerate_insights(self) -> bool:
        """
        Vérifier si un nouvel insight doit être généré (>n heures  depuis le dernier).
        voir REGENERATE_INSIGHTS_AFTER_HOURS
        Returns:
            True si régénération nécessaire, False si insight cached valide.
        """
        latest = self.db.get_latest_insight(self.user_id, "weekly")

        if not latest:
            # Aucun insight existant
            return True

        # Parser le timestamp
        created_at = datetime.fromisoformat(latest["created_at"])
        now = datetime.now()

        # Vérifier si >REGENERATE_INSIGHTS_AFTER_HOURS heures
        time_diff = now - created_at
        return time_diff > timedelta(hours=REGENERATE_INSIGHTS_AFTER_HOURS)

    def _get_data_maturity_level(self, days_count: int) -> str:
        """
        Déterminer le niveau de maturité des données.

        Args:
            days_count: Nombre de jours avec des données.

        Returns:
            "early" (<3 jours), "developing" (3-6 jours), ou "mature" (≥7 jours).
        """
        if days_count < 3:
            return "early"
        elif days_count < 7:
            return "developing"
        else:
            return "mature"

    def _build_data_context(self, mood_data: list, conv_count: int, days_count: int, conv_history: list = None) -> str:
        """
        Construire le contexte des données pour le prompt.

        Args:
            mood_data: Liste des check-ins récents.
            conv_count: Nombre de conversations.
            days_count: Nombre de jours de données.
            conv_history: Liste des conversations récentes (optionnel).

        Returns:
            Contexte formaté en texte.
        """
        context_parts = [
            f"Nombre de jours de données: {days_count}",
            f"Nombre de conversations: {conv_count}"
        ]

        if mood_data:
            avg_mood = self._calculate_avg_mood(mood_data)
            context_parts.append(f"Score d'humeur moyen: {avg_mood:.1f}/10")

            # Extraire quelques notes récentes (max 3)
            recent_notes = [
                item["notes"] for item in mood_data[:3]
                if item.get("notes") and item["notes"].strip()
            ]

            if recent_notes:
                context_parts.append(
                    f"Notes de check-ins récents:\n" + "\n".join(f"- {note}" for note in recent_notes)
                )

        # Ajouter extraits de conversations récentes
        if conv_history and len(conv_history) > 0:
            # Extraire les 5 messages utilisateur les plus récents
            recent_messages = []
            for conv in conv_history[:5]:
                user_msg = conv.get("user_message", "")
                # Limiter à 200 caractères pour éviter surcharge tokens
                if user_msg:
                    truncated = user_msg[:200] + "..." if len(user_msg) > 200 else user_msg
                    recent_messages.append(truncated)

            if recent_messages:
                context_parts.append(
                    f"Extraits de conversations récentes:\n" + "\n".join(f"- {msg}" for msg in recent_messages)
                )

        return "\n\n".join(context_parts)

    def _calculate_avg_mood(self, mood_data: list) -> float:
        """
        Calculer le score d'humeur moyen.

        Args:
            mood_data: Liste des check-ins.

        Returns:
            Score moyen (float).
        """
        if not mood_data:
            return 0.0

        scores = [item["mood_score"] for item in mood_data]
        return sum(scores) / len(scores)
