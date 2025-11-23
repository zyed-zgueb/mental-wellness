#!/usr/bin/env python3
"""
Script de migration de base de données pour ajouter la table action_items.
Phase 2.1 : Suivi Contextuel & Mémoire de l'IA - Goals & Actions

Ce script crée la table action_items pour le suivi des objectifs et actions.
"""

import sqlite3
import sys
import os


def migrate_database(db_path="serene.db"):
    """
    Migrer la base de données pour ajouter la table action_items.

    Args:
        db_path: Chemin vers le fichier de base de données SQLite.
    """
    if not os.path.exists(db_path):
        print(f"❌ Base de données introuvable: {db_path}")
        print("ℹ️  Assurez-vous que l'application a été lancée au moins une fois")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print(f"🔧 Migration de la base de données: {db_path}")
        print()

        # Check if table already exists
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='action_items'
            """
        )
        table_exists = cursor.fetchone() is not None

        if table_exists:
            print("✅ Table 'action_items' existe déjà - aucune migration nécessaire")
            conn.close()
            return True

        # Create action_items table
        print("📝 Création de la table 'action_items'...")
        print()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed', 'abandoned')),
                source TEXT DEFAULT 'manual',
                conversation_id INTEGER,
                deadline DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL
            )
            """
        )

        # Create indexes
        print("📝 Création des index...")
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_action_items_user_id ON action_items(user_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_action_items_status ON action_items(status)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_action_items_created_at ON action_items(created_at DESC)"
        )

        conn.commit()
        print()
        print("✅ Migration terminée avec succès !")

        # Verify migration
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='action_items'
            """
        )
        if cursor.fetchone():
            print()
            print("📊 Table 'action_items' créée avec succès")

            # Show table schema
            cursor.execute("PRAGMA table_info(action_items)")
            columns = cursor.fetchall()
            print()
            print("Colonnes:")
            for col in columns:
                col_id, name, col_type, notnull, default_val, pk = col
                print(f"   - {name} ({col_type})")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Point d'entrée principal."""
    print("=" * 60)
    print("Migration de la base de données - Action Items")
    print("Phase 2.1 : Suivi Contextuel & Mémoire de l'IA")
    print("=" * 60)
    print()

    # Get database path from command line or use default
    db_path = sys.argv[1] if len(sys.argv) > 1 else "serene.db"

    success = migrate_database(db_path)

    print()
    print("=" * 60)

    if success:
        print("✅ Migration réussie !")
        sys.exit(0)
    else:
        print("❌ Migration échouée")
        sys.exit(1)


if __name__ == "__main__":
    main()
