"""Gestionnaire de base de données SQLite pour Serene."""

import sqlite3
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta


class DatabaseManager:
    """Gestionnaire de base de données pour les opérations CRUD."""

    def __init__(self, db_path: str = "serene.db"):
        """
        Initialiser la connexion et créer les tables.

        Args:
            db_path: Chemin vers le fichier de base de données SQLite.
                    Utiliser ":memory:" pour une base de données en mémoire (tests).
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable dict-like access
        self._init_db()

    def _init_db(self):
        """Créer les tables si elles n'existent pas."""
        # Pour les DB in-memory (tests), utiliser le schéma directement
        if self.db_path == ":memory:":
            schema = """
            CREATE TABLE IF NOT EXISTS check_ins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                mood_score INTEGER NOT NULL CHECK(mood_score BETWEEN 1 AND 10),
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_check_ins_timestamp ON check_ins(timestamp);

            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                tokens_used INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
            """
        else:
            # Pour les DB sur disque, charger depuis schema.sql
            schema_path = os.path.join(
                os.path.dirname(__file__), "schema.sql"
            )
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = f.read()

        self.conn.executescript(schema)
        self.conn.commit()

    def save_checkin(self, mood_score: int, notes: str = "") -> int:
        """
        Enregistrer un check-in.

        Args:
            mood_score: Score d'humeur (1-10).
            notes: Notes optionnelles de l'utilisateur.

        Returns:
            ID du check-in créé.

        Raises:
            ValueError: Si mood_score est hors limites (1-10).
        """
        if not isinstance(mood_score, int) or not 1 <= mood_score <= 10:
            raise ValueError(
                f"mood_score doit être un entier entre 1 et 10, reçu: {mood_score}"
            )

        try:
            cursor = self.conn.execute(
                "INSERT INTO check_ins (mood_score, notes) VALUES (?, ?)",
                (mood_score, notes),
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Erreur d'intégrité de la base de données: {e}")

    def get_mood_history(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Récupérer l'historique des check-ins (derniers N jours).

        Args:
            days: Nombre de jours d'historique à récupérer (défaut: 30).

        Returns:
            Liste de dicts contenant: id, timestamp, mood_score, notes, created_at.
            Trié du plus récent au plus ancien.
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        cursor = self.conn.execute(
            """
            SELECT id, timestamp, mood_score, notes, created_at
            FROM check_ins
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
            """,
            (cutoff_date,),
        )

        return [dict(row) for row in cursor.fetchall()]

    def save_conversation(
        self, user_message: str, ai_response: str, tokens_used: int = 0
    ) -> int:
        """
        Enregistrer une conversation.

        Args:
            user_message: Message de l'utilisateur.
            ai_response: Réponse de l'IA.
            tokens_used: Nombre de tokens utilisés (optionnel).

        Returns:
            ID de la conversation créée.

        Raises:
            ValueError: Si les messages sont vides.
        """
        if not user_message or not ai_response:
            raise ValueError("Les messages ne peuvent pas être vides")

        try:
            cursor = self.conn.execute(
                """
                INSERT INTO conversations (user_message, ai_response, tokens_used)
                VALUES (?, ?, ?)
                """,
                (user_message, ai_response, tokens_used),
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Erreur d'intégrité de la base de données: {e}")

    def get_conversation_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Récupérer l'historique des conversations.

        Args:
            limit: Nombre maximum de conversations à récupérer (défaut: 50).

        Returns:
            Liste de dicts contenant: id, timestamp, user_message, ai_response, tokens_used, created_at.
            Trié du plus récent au plus ancien.
        """
        cursor = self.conn.execute(
            """
            SELECT id, timestamp, user_message, ai_response, tokens_used, created_at
            FROM conversations
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )

        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        """Fermer la connexion à la base de données."""
        if self.conn:
            self.conn.close()
