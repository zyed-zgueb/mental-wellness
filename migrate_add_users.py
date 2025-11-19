"""
Migration script to add users table and user_id to existing tables.

This script safely migrates existing Serene databases to support multi-user authentication.
It creates a default user and assigns all existing data to this user.

Usage:
    python migrate_add_users.py

The script will:
1. Backup the existing database
2. Create the users table
3. Add user_id columns to check_ins, conversations, and insights_log
4. Create a default user
5. Assign all existing data to the default user
"""

import sqlite3
import hashlib
import os
import shutil
from datetime import datetime

DB_PATH = "serene.db"
BACKUP_PATH = f"serene.db.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Default user credentials
DEFAULT_EMAIL = "user@serene.local"
DEFAULT_PASSWORD = "serene123"  # User should change this after first login
DEFAULT_DISPLAY_NAME = "Utilisateur"


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def backup_database():
    """Create a backup of the existing database."""
    if os.path.exists(DB_PATH):
        print(f"📦 Creating backup: {BACKUP_PATH}")
        shutil.copy2(DB_PATH, BACKUP_PATH)
        print("✅ Backup created successfully")
    else:
        print("ℹ️  No existing database found, starting fresh")


def migrate_database():
    """Execute the migration."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Step 1: Create users table if it doesn't exist
        print("\n📝 Creating users table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                display_name TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME,
                preferences TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        print("✅ Users table created")

        # Step 2: Check if default user exists, create if not
        print("\n👤 Creating default user...")
        cursor.execute("SELECT id FROM users WHERE email = ?", (DEFAULT_EMAIL,))
        existing_user = cursor.fetchone()

        if existing_user:
            default_user_id = existing_user[0]
            print(f"ℹ️  Default user already exists (ID: {default_user_id})")
        else:
            password_hash = hash_password(DEFAULT_PASSWORD)
            cursor.execute("""
                INSERT INTO users (email, password_hash, display_name, created_at)
                VALUES (?, ?, ?, ?)
            """, (DEFAULT_EMAIL, password_hash, DEFAULT_DISPLAY_NAME, datetime.now().isoformat()))
            default_user_id = cursor.lastrowid
            print(f"✅ Default user created (ID: {default_user_id})")
            print(f"   Email: {DEFAULT_EMAIL}")
            print(f"   Password: {DEFAULT_PASSWORD}")
            print("   ⚠️  Please change this password after first login!")

        # Step 3: Add user_id to check_ins table
        print("\n🔧 Migrating check_ins table...")
        cursor.execute("PRAGMA table_info(check_ins)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'user_id' not in columns:
            # SQLite doesn't support ADD COLUMN with NOT NULL + DEFAULT in one go
            # We need to recreate the table
            cursor.execute("""
                CREATE TABLE check_ins_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    mood_score INTEGER NOT NULL CHECK(mood_score BETWEEN 0 AND 10),
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            # Copy existing data with default user_id
            cursor.execute(f"""
                INSERT INTO check_ins_new (id, user_id, timestamp, mood_score, notes, created_at)
                SELECT id, {default_user_id}, timestamp, mood_score, notes, created_at
                FROM check_ins
            """)

            # Drop old table and rename new one
            cursor.execute("DROP TABLE check_ins")
            cursor.execute("ALTER TABLE check_ins_new RENAME TO check_ins")

            # Recreate indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_check_ins_timestamp ON check_ins(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_check_ins_user_id ON check_ins(user_id)")

            count = cursor.execute("SELECT COUNT(*) FROM check_ins").fetchone()[0]
            print(f"✅ Migrated {count} check-ins to default user")
        else:
            print("ℹ️  check_ins table already has user_id column")

        # Step 4: Add user_id to conversations table
        print("\n🔧 Migrating conversations table...")
        cursor.execute("PRAGMA table_info(conversations)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'user_id' not in columns:
            cursor.execute("""
                CREATE TABLE conversations_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_message TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    tokens_used INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            cursor.execute(f"""
                INSERT INTO conversations_new (id, user_id, timestamp, user_message, ai_response, tokens_used, created_at)
                SELECT id, {default_user_id}, timestamp, user_message, ai_response, tokens_used, created_at
                FROM conversations
            """)

            cursor.execute("DROP TABLE conversations")
            cursor.execute("ALTER TABLE conversations_new RENAME TO conversations")

            cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id)")

            count = cursor.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
            print(f"✅ Migrated {count} conversations to default user")
        else:
            print("ℹ️  conversations table already has user_id column")

        # Step 5: Add user_id to insights_log table
        print("\n🔧 Migrating insights_log table...")
        cursor.execute("PRAGMA table_info(insights_log)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'user_id' not in columns:
            cursor.execute("""
                CREATE TABLE insights_log_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    insight_type VARCHAR(50) NOT NULL,
                    content TEXT NOT NULL,
                    based_on_data TEXT,
                    tokens_used INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            cursor.execute(f"""
                INSERT INTO insights_log_new (id, user_id, created_at, insight_type, content, based_on_data, tokens_used)
                SELECT id, {default_user_id}, created_at, insight_type, content, based_on_data, tokens_used
                FROM insights_log
            """)

            cursor.execute("DROP TABLE insights_log")
            cursor.execute("ALTER TABLE insights_log_new RENAME TO insights_log")

            cursor.execute("CREATE INDEX IF NOT EXISTS idx_insights_log_type_created ON insights_log(insight_type, created_at DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_insights_log_user_id ON insights_log(user_id)")

            count = cursor.execute("SELECT COUNT(*) FROM insights_log").fetchone()[0]
            print(f"✅ Migrated {count} insights to default user")
        else:
            print("ℹ️  insights_log table already has user_id column")

        # Commit all changes
        conn.commit()
        print("\n✅ Migration completed successfully!")
        print("\n" + "="*60)
        print("IMPORTANT: Default login credentials")
        print("="*60)
        print(f"Email:    {DEFAULT_EMAIL}")
        print(f"Password: {DEFAULT_PASSWORD}")
        print("="*60)
        print("⚠️  Please change this password after your first login!")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        print(f"Database has been rolled back. Backup is available at: {BACKUP_PATH}")
        raise
    finally:
        conn.close()


def main():
    """Main migration entry point."""
    print("="*60)
    print("Serene Database Migration - Add Multi-User Support")
    print("="*60)

    # Create backup
    backup_database()

    # Run migration
    migrate_database()

    print(f"\n💾 Backup saved to: {BACKUP_PATH}")
    print("Keep this backup until you've verified the migration worked correctly.")


if __name__ == "__main__":
    main()
