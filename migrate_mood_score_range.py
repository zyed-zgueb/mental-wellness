#!/usr/bin/env python3
"""
Script de migration pour modifier la contrainte CHECK de mood_score
De: BETWEEN 1 AND 10
À: BETWEEN 0 AND 10

En SQLite, on ne peut pas modifier directement une contrainte CHECK.
Il faut recréer la table.
"""

import sqlite3
import sys
import os


def migrate_database(db_path: str = "serene.db"):
    """
    Migre la base de données pour accepter mood_score de 0 à 10.

    Args:
        db_path: Chemin vers la base de données
    """
    if not os.path.exists(db_path):
        print(f"✅ Aucune base de données trouvée à {db_path}")
        print("   La nouvelle contrainte sera appliquée automatiquement à la création.")
        return

    print(f"🔄 Migration de la base de données: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Vérifier si la migration est nécessaire
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='check_ins'")
        result = cursor.fetchone()

        if result and "BETWEEN 0 AND 10" in result[0]:
            print("✅ La base de données est déjà à jour (contrainte 0-10)")
            return

        if result and "BETWEEN 1 AND 10" not in result[0]:
            print("⚠️  Schéma de table inattendu. Migration annulée.")
            print(f"   Schéma actuel: {result[0]}")
            return

        print("📋 Début de la migration...")

        # Désactiver les contraintes de clés étrangères temporairement
        cursor.execute("PRAGMA foreign_keys=OFF")

        # Commencer une transaction
        cursor.execute("BEGIN TRANSACTION")

        # 1. Créer une nouvelle table avec la nouvelle contrainte
        cursor.execute("""
            CREATE TABLE check_ins_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                mood_score INTEGER NOT NULL CHECK(mood_score BETWEEN 0 AND 10),
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  ✓ Nouvelle table créée")

        # 2. Copier toutes les données (seules les valeurs 1-10 existent déjà)
        cursor.execute("""
            INSERT INTO check_ins_new (id, timestamp, mood_score, notes, created_at)
            SELECT id, timestamp, mood_score, notes, created_at
            FROM check_ins
        """)
        count = cursor.rowcount
        print(f"  ✓ {count} enregistrements copiés")

        # 3. Supprimer l'ancienne table
        cursor.execute("DROP TABLE check_ins")
        print("  ✓ Ancienne table supprimée")

        # 4. Renommer la nouvelle table
        cursor.execute("ALTER TABLE check_ins_new RENAME TO check_ins")
        print("  ✓ Nouvelle table renommée")

        # 5. Recréer l'index
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_check_ins_timestamp ON check_ins(timestamp)")
        print("  ✓ Index recréé")

        # Commiter la transaction
        conn.commit()
        print("✅ Migration réussie !")

        # Réactiver les contraintes de clés étrangères
        cursor.execute("PRAGMA foreign_keys=ON")

    except Exception as e:
        conn.rollback()
        print(f"❌ Erreur lors de la migration: {e}")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "serene.db"
    print(f"🔍 Vérification de la base de données: {db_path}")
    migrate_database(db_path)
