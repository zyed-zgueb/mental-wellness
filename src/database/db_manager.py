"""Gestionnaire de base de données SQLite pour Serene."""

import sqlite3
import os
import hashlib
import json
from typing import List, Dict, Any, Optional
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
                mood_score INTEGER NOT NULL CHECK(mood_score BETWEEN 0 AND 10),
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

            CREATE TABLE IF NOT EXISTS insights_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                insight_type VARCHAR(50) NOT NULL,
                content TEXT NOT NULL,
                based_on_data TEXT,
                tokens_used INTEGER
            );
            CREATE INDEX IF NOT EXISTS idx_insights_log_type_created ON insights_log(insight_type, created_at DESC);
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

    def save_checkin(self, user_id: int, mood_score: int, notes: str = "") -> int:
        """
        Enregistrer un check-in.

        Args:
            user_id: ID de l'utilisateur.
            mood_score: Score d'humeur (0-10).
            notes: Notes optionnelles de l'utilisateur.

        Returns:
            ID du check-in créé.

        Raises:
            ValueError: Si mood_score est hors limites (0-10) ou user_id invalide.
        """
        if not isinstance(mood_score, int) or not 0 <= mood_score <= 10:
            raise ValueError(
                f"mood_score doit être un entier entre 0 et 10, reçu: {mood_score}"
            )

        if not user_id:
            raise ValueError("user_id est requis")

        try:
            cursor = self.conn.execute(
                "INSERT INTO check_ins (user_id, mood_score, notes) VALUES (?, ?, ?)",
                (user_id, mood_score, notes),
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Erreur d'intégrité de la base de données: {e}")

    def get_mood_history(self, user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """
        Récupérer l'historique des check-ins (derniers N jours).

        Args:
            user_id: ID de l'utilisateur.
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
            WHERE user_id = ? AND timestamp >= ?
            ORDER BY timestamp DESC
            """,
            (user_id, cutoff_date),
        )

        return [dict(row) for row in cursor.fetchall()]

    def save_conversation(
        self, user_id: int, user_message: str, ai_response: str, tokens_used: int = 0
    ) -> int:
        """
        Enregistrer une conversation.

        Args:
            user_id: ID de l'utilisateur.
            user_message: Message de l'utilisateur.
            ai_response: Réponse de l'IA.
            tokens_used: Nombre de tokens utilisés (optionnel).

        Returns:
            ID de la conversation créée.

        Raises:
            ValueError: Si les messages sont vides ou user_id invalide.
        """
        if not user_message or not ai_response:
            raise ValueError("Les messages ne peuvent pas être vides")

        if not user_id:
            raise ValueError("user_id est requis")

        try:
            cursor = self.conn.execute(
                """
                INSERT INTO conversations (user_id, user_message, ai_response, tokens_used)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, user_message, ai_response, tokens_used),
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Erreur d'intégrité de la base de données: {e}")

    def get_conversation_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Récupérer l'historique des conversations.

        Args:
            user_id: ID de l'utilisateur.
            limit: Nombre maximum de conversations à récupérer (défaut: 50).

        Returns:
            Liste de dicts contenant: id, timestamp, user_message, ai_response, tokens_used, created_at.
            Trié du plus récent au plus ancien.
        """
        cursor = self.conn.execute(
            """
            SELECT id, timestamp, user_message, ai_response, tokens_used, created_at
            FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp ASC
            LIMIT ?
            """,
            (user_id, limit),
        )

        return [dict(row) for row in cursor.fetchall()]

    def get_conversation_count(self, user_id: int, days: int = 7) -> int:
        """
        Compter le nombre de conversations (derniers N jours).

        Args:
            user_id: ID de l'utilisateur.
            days: Nombre de jours à considérer (défaut: 7).

        Returns:
            Nombre total de conversations dans la période.
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        cursor = self.conn.execute(
            """
            SELECT COUNT(*) as count
            FROM conversations
            WHERE user_id = ? AND timestamp >= ?
            """,
            (user_id, cutoff_date),
        )

        result = cursor.fetchone()
        return result["count"] if result else 0

    def save_insight(
        self,
        user_id: int,
        insight_type: str,
        content: str,
        based_on_data: str = "",
        tokens_used: int = 0,
    ) -> int:
        """
        Enregistrer un insight IA.

        Args:
            user_id: ID de l'utilisateur.
            insight_type: Type d'insight (ex: "weekly", "monthly").
            content: Contenu de l'insight généré.
            based_on_data: Métadonnées sur les données utilisées (JSON string optionnel).
            tokens_used: Nombre de tokens utilisés pour la génération.

        Returns:
            ID de l'insight créé.

        Raises:
            ValueError: Si les paramètres sont invalides.
        """
        if not insight_type or not content:
            raise ValueError("insight_type et content ne peuvent pas être vides")

        if not user_id:
            raise ValueError("user_id est requis")

        try:
            cursor = self.conn.execute(
                """
                INSERT INTO insights_log (user_id, insight_type, content, based_on_data, tokens_used)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, insight_type, content, based_on_data, tokens_used),
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Erreur d'intégrité de la base de données: {e}")

    def get_latest_insight(self, user_id: int, insight_type: str) -> Optional[Dict[str, Any]]:
        """
        Récupérer le dernier insight d'un type donné.

        Args:
            user_id: ID de l'utilisateur.
            insight_type: Type d'insight à récupérer.

        Returns:
            Dict contenant l'insight (id, created_at, insight_type, content, based_on_data, tokens_used),
            ou None si aucun insight trouvé.
        """
        cursor = self.conn.execute(
            """
            SELECT id, created_at, insight_type, content, based_on_data, tokens_used
            FROM insights_log
            WHERE user_id = ? AND insight_type = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (user_id, insight_type),
        )

        result = cursor.fetchone()
        return dict(result) if result else None

    # ===== User Authentication Methods =====

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash a password using SHA-256.

        Args:
            password: Plain text password.

        Returns:
            Hashed password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(
        self, email: str, password: str, display_name: Optional[str] = None
    ) -> int:
        """
        Create a new user account.

        Args:
            email: User's email address (must be unique).
            password: Plain text password (will be hashed).
            display_name: Optional display name for the user.

        Returns:
            ID of the created user.

        Raises:
            ValueError: If email already exists or inputs are invalid.
        """
        if not email or not password:
            raise ValueError("Email et mot de passe sont requis")

        # Check if email already exists
        existing_user = self.get_user_by_email(email)
        if existing_user:
            raise ValueError(f"Un utilisateur avec l'email '{email}' existe déjà")

        password_hash = self._hash_password(password)

        try:
            cursor = self.conn.execute(
                """
                INSERT INTO users (email, password_hash, display_name, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (email, password_hash, display_name, datetime.now().isoformat()),
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Erreur lors de la création de l'utilisateur: {e}")

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user with email and password.

        Args:
            email: User's email address.
            password: Plain text password.

        Returns:
            User dict if authentication successful, None otherwise.
            Dict contains: id, email, display_name, created_at, last_login, preferences
        """
        if not email or not password:
            return None

        user = self.get_user_by_email(email)
        if not user:
            return None

        password_hash = self._hash_password(password)
        if user["password_hash"] != password_hash:
            return None

        # Update last login
        self.update_last_login(user["id"])

        # Remove password_hash from returned data
        user_data = {k: v for k, v in user.items() if k != "password_hash"}
        return user_data

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.

        Args:
            user_id: User's ID.

        Returns:
            User dict or None if not found.
        """
        cursor = self.conn.execute(
            """
            SELECT id, email, password_hash, display_name, created_at, last_login, preferences
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        )

        result = cursor.fetchone()
        return dict(result) if result else None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email.

        Args:
            email: User's email address.

        Returns:
            User dict or None if not found.
        """
        cursor = self.conn.execute(
            """
            SELECT id, email, password_hash, display_name, created_at, last_login, preferences
            FROM users
            WHERE email = ?
            """,
            (email,),
        )

        result = cursor.fetchone()
        return dict(result) if result else None

    def update_last_login(self, user_id: int) -> None:
        """
        Update user's last login timestamp.

        Args:
            user_id: User's ID.
        """
        self.conn.execute(
            """
            UPDATE users
            SET last_login = ?
            WHERE id = ?
            """,
            (datetime.now().isoformat(), user_id),
        )
        self.conn.commit()

    def update_user_preferences(
        self, user_id: int, preferences: Dict[str, Any]
    ) -> None:
        """
        Update user preferences.

        Args:
            user_id: User's ID.
            preferences: Dict of user preferences (will be stored as JSON).
        """
        preferences_json = json.dumps(preferences)

        self.conn.execute(
            """
            UPDATE users
            SET preferences = ?
            WHERE id = ?
            """,
            (preferences_json, user_id),
        )
        self.conn.commit()

    def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """
        Get user preferences.

        Args:
            user_id: User's ID.

        Returns:
            Dict of user preferences, or empty dict if none set.
        """
        user = self.get_user_by_id(user_id)
        if not user or not user.get("preferences"):
            return {}

        try:
            return json.loads(user["preferences"])
        except json.JSONDecodeError:
            return {}

    def change_password(self, user_id: int, new_password: str) -> None:
        """
        Change user's password.

        Args:
            user_id: User's ID.
            new_password: New plain text password (will be hashed).

        Raises:
            ValueError: If password is empty.
        """
        if not new_password:
            raise ValueError("Le mot de passe ne peut pas être vide")

        password_hash = self._hash_password(new_password)

        self.conn.execute(
            """
            UPDATE users
            SET password_hash = ?
            WHERE id = ?
            """,
            (password_hash, user_id),
        )
        self.conn.commit()

    def update_user_profile(
        self,
        user_id: int,
        display_name: Optional[str] = None,
        full_name: Optional[str] = None,
        birth_year: Optional[int] = None,
        timezone: Optional[str] = None,
    ) -> None:
        """
        Update user profile information.

        Args:
            user_id: User's ID.
            display_name: Display name (optional).
            full_name: Full name (optional).
            birth_year: Birth year (optional).
            timezone: Timezone/location (optional).
        """
        # Build dynamic update query based on provided fields
        updates = []
        params = []

        if display_name is not None:
            updates.append("display_name = ?")
            params.append(display_name)

        if full_name is not None:
            updates.append("full_name = ?")
            params.append(full_name)

        if birth_year is not None:
            updates.append("birth_year = ?")
            params.append(birth_year)

        if timezone is not None:
            updates.append("timezone = ?")
            params.append(timezone)

        if not updates:
            return  # Nothing to update

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"

        self.conn.execute(query, params)
        self.conn.commit()

    def export_user_data(self, user_id: int) -> Dict[str, Any]:
        """
        Export all user data for RGPD compliance.

        Args:
            user_id: User's ID.

        Returns:
            Dict containing all user data including profile, check-ins, conversations, and insights.
        """
        # Get user profile
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"Utilisateur {user_id} introuvable")

        # Remove password_hash from export
        user_data = {k: v for k, v in user.items() if k != "password_hash"}

        # Get all check-ins
        cursor = self.conn.execute(
            """
            SELECT id, timestamp, mood_score, notes, created_at
            FROM check_ins
            WHERE user_id = ?
            ORDER BY timestamp DESC
            """,
            (user_id,),
        )
        check_ins = [dict(row) for row in cursor.fetchall()]

        # Get all conversations
        cursor = self.conn.execute(
            """
            SELECT id, timestamp, user_message, ai_response, tokens_used, created_at
            FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            """,
            (user_id,),
        )
        conversations = [dict(row) for row in cursor.fetchall()]

        # Get all insights
        cursor = self.conn.execute(
            """
            SELECT id, created_at, insight_type, content, based_on_data, tokens_used
            FROM insights_log
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
        insights = [dict(row) for row in cursor.fetchall()]

        # Get all action items
        cursor = self.conn.execute(
            """
            SELECT id, title, description, status, source, conversation_id,
                   deadline, created_at, completed_at, updated_at
            FROM action_items
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
        action_items = [dict(row) for row in cursor.fetchall()]

        # Parse preferences if available
        if user_data.get("preferences"):
            try:
                user_data["preferences"] = json.loads(user_data["preferences"])
            except json.JSONDecodeError:
                pass

        return {
            "user_profile": user_data,
            "check_ins": check_ins,
            "conversations": conversations,
            "insights": insights,
            "action_items": action_items,
            "export_timestamp": datetime.now().isoformat(),
        }

    # ===== Action Items Methods =====

    def save_action_item(
        self,
        user_id: int,
        title: str,
        description: str = "",
        source: str = "manual",
        conversation_id: Optional[int] = None,
        deadline: Optional[str] = None,
    ) -> int:
        """
        Enregistrer un nouvel objectif/action.

        Args:
            user_id: ID de l'utilisateur.
            title: Titre de l'action.
            description: Description détaillée (optionnelle).
            source: Source de l'action ('manual' ou 'ai_extracted').
            conversation_id: ID de la conversation d'origine si extrait par l'IA.
            deadline: Date limite au format ISO (optionnelle).

        Returns:
            ID de l'action créée.

        Raises:
            ValueError: Si les paramètres sont invalides.
        """
        if not title:
            raise ValueError("Le titre ne peut pas être vide")

        if not user_id:
            raise ValueError("user_id est requis")

        if source not in ["manual", "ai_extracted"]:
            raise ValueError("source doit être 'manual' ou 'ai_extracted'")

        try:
            cursor = self.conn.execute(
                """
                INSERT INTO action_items (user_id, title, description, source, conversation_id, deadline)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, title, description, source, conversation_id, deadline),
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Erreur d'intégrité de la base de données: {e}")

    def get_action_items(
        self, user_id: int, status: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Récupérer les actions d'un utilisateur.

        Args:
            user_id: ID de l'utilisateur.
            status: Filtrer par statut (optionnel: 'pending', 'in_progress', 'completed', 'abandoned').
            limit: Nombre maximum d'actions à récupérer (défaut: 100).

        Returns:
            Liste de dicts contenant les informations des actions.
            Trié par date de création (plus récent en premier).
        """
        if status:
            cursor = self.conn.execute(
                """
                SELECT id, user_id, title, description, status, source,
                       conversation_id, deadline, created_at, completed_at, updated_at
                FROM action_items
                WHERE user_id = ? AND status = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (user_id, status, limit),
            )
        else:
            cursor = self.conn.execute(
                """
                SELECT id, user_id, title, description, status, source,
                       conversation_id, deadline, created_at, completed_at, updated_at
                FROM action_items
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (user_id, limit),
            )

        return [dict(row) for row in cursor.fetchall()]

    def update_action_item(
        self,
        action_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> None:
        """
        Mettre à jour une action.

        Args:
            action_id: ID de l'action.
            title: Nouveau titre (optionnel).
            description: Nouvelle description (optionnelle).
            status: Nouveau statut (optionnel).
            deadline: Nouvelle deadline (optionnelle).

        Raises:
            ValueError: Si le statut est invalide.
        """
        if status and status not in ["pending", "in_progress", "completed", "abandoned"]:
            raise ValueError(
                "status doit être 'pending', 'in_progress', 'completed' ou 'abandoned'"
            )

        # Build dynamic update query
        updates = ["updated_at = ?"]
        params = [datetime.now().isoformat()]

        if title is not None:
            updates.append("title = ?")
            params.append(title)

        if description is not None:
            updates.append("description = ?")
            params.append(description)

        if status is not None:
            updates.append("status = ?")
            params.append(status)
            # Set completed_at timestamp if status is completed
            if status == "completed":
                updates.append("completed_at = ?")
                params.append(datetime.now().isoformat())
            elif status in ["pending", "in_progress", "abandoned"]:
                # Reset completed_at if status is changed back
                updates.append("completed_at = ?")
                params.append(None)

        if deadline is not None:
            updates.append("deadline = ?")
            params.append(deadline)

        params.append(action_id)
        query = f"UPDATE action_items SET {', '.join(updates)} WHERE id = ?"

        self.conn.execute(query, params)
        self.conn.commit()

    def delete_action_item(self, action_id: int) -> None:
        """
        Supprimer une action.

        Args:
            action_id: ID de l'action à supprimer.
        """
        self.conn.execute(
            """
            DELETE FROM action_items
            WHERE id = ?
            """,
            (action_id,),
        )
        self.conn.commit()

    def get_action_item_by_id(self, action_id: int) -> Optional[Dict[str, Any]]:
        """
        Récupérer une action par son ID.

        Args:
            action_id: ID de l'action.

        Returns:
            Dict contenant les informations de l'action, ou None si non trouvée.
        """
        cursor = self.conn.execute(
            """
            SELECT id, user_id, title, description, status, source,
                   conversation_id, deadline, created_at, completed_at, updated_at
            FROM action_items
            WHERE id = ?
            """,
            (action_id,),
        )

        result = cursor.fetchone()
        return dict(result) if result else None

    def get_action_items_stats(self, user_id: int) -> Dict[str, int]:
        """
        Obtenir des statistiques sur les actions d'un utilisateur.

        Args:
            user_id: ID de l'utilisateur.

        Returns:
            Dict avec le nombre d'actions par statut.
        """
        cursor = self.conn.execute(
            """
            SELECT status, COUNT(*) as count
            FROM action_items
            WHERE user_id = ?
            GROUP BY status
            """,
            (user_id,),
        )

        stats = {
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "abandoned": 0,
            "total": 0,
        }

        for row in cursor.fetchall():
            stats[row["status"]] = row["count"]
            stats["total"] += row["count"]

        return stats

    def close(self):
        """Fermer la connexion à la base de données."""
        if self.conn:
            self.conn.close()
