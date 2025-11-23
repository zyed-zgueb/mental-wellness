#!/usr/bin/env python3
"""
Script de migration pour ajouter la table proposed_actions
pour le système d'approbation des actions proposées par l'IA.
"""

import sqlite3
import sys
from pathlib import Path


def migrate_proposed_actions(db_path: str = "serene.db") -> None:
    """
    Ajouter la table proposed_actions à la base de données.

    Args:
        db_path: Chemin vers le fichier de base de données.
    """
    print(f"🔧 Migration de la base de données: {db_path}")

    # Vérifier si le fichier existe
    if not Path(db_path).exists():
        print(f"❌ Erreur: La base de données '{db_path}' n'existe pas.")
        print("   Créez d'abord la base de données principale.")
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Vérifier si la table existe déjà
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='proposed_actions'
            """
        )

        if cursor.fetchone():
            print("ℹ️  La table 'proposed_actions' existe déjà.")
        else:
            print("📊 Création de la table 'proposed_actions'...")

            # Créer la table proposed_actions
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS proposed_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'accepted', 'rejected')),
                    conversation_id INTEGER,
                    proposed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    reviewed_at DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL
                )
                """
            )

            # Créer les index
            print("📊 Création des index...")
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_proposed_actions_user_id
                ON proposed_actions(user_id)
                """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_proposed_actions_status
                ON proposed_actions(status)
                """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_proposed_actions_proposed_at
                ON proposed_actions(proposed_at DESC)
                """
            )

            conn.commit()
            print("✅ Table 'proposed_actions' créée avec succès !")

        # Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(proposed_actions)")
        columns = cursor.fetchall()

        print("\n📋 Structure de la table 'proposed_actions':")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")

        print("\n✅ Migration terminée avec succès !")

    except sqlite3.Error as e:
        print(f"❌ Erreur lors de la migration: {e}")
        conn.rollback()
        sys.exit(1)

    finally:
        conn.close()


if __name__ == "__main__":
    # Permettre de spécifier un chemin de base de données personnalisé
    db_path = sys.argv[1] if len(sys.argv) > 1 else "serene.db"
    migrate_proposed_actions(db_path)
