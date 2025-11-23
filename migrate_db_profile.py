#!/usr/bin/env python3
"""
Script de migration de base de données pour ajouter les colonnes de profil utilisateur.
Phase 1.2 : Profil utilisateur

Ce script ajoute les colonnes suivantes à la table users:
- full_name (TEXT): Nom complet de l'utilisateur
- birth_year (INTEGER): Année de naissance
- timezone (TEXT): Fuseau horaire / zone géographique
"""

import sqlite3
import sys
import os


def migrate_database(db_path="serene.db"):
    """
    Migrer la base de données pour ajouter les colonnes de profil.

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

        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]

        migrations_needed = []

        if "full_name" not in columns:
            migrations_needed.append(("full_name", "TEXT"))

        if "birth_year" not in columns:
            migrations_needed.append(("birth_year", "INTEGER"))

        if "timezone" not in columns:
            migrations_needed.append(("timezone", "TEXT"))

        if not migrations_needed:
            print("✅ Aucune migration nécessaire - la base de données est déjà à jour")
            conn.close()
            return True

        # Apply migrations
        print(f"📝 {len(migrations_needed)} migration(s) à appliquer:")
        for col_name, col_type in migrations_needed:
            print(f"   - Ajout de la colonne '{col_name}' ({col_type})")

        print()

        for col_name, col_type in migrations_needed:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
                print(f"✅ Colonne '{col_name}' ajoutée avec succès")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"⚠️  Colonne '{col_name}' existe déjà (ignoré)")
                else:
                    raise

        conn.commit()
        print()
        print("✅ Migration terminée avec succès !")

        # Verify migration
        cursor.execute("PRAGMA table_info(users)")
        columns_after = [col[1] for col in cursor.fetchall()]

        print()
        print("📊 Colonnes de la table 'users' après migration:")
        for col in columns_after:
            print(f"   - {col}")

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
    print("Migration de la base de données - Profil utilisateur")
    print("Phase 1.2 : Profil utilisateur")
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
