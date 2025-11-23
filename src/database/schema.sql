-- Schéma de base de données pour Serene

-- Table: users - Gestion des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    display_name TEXT,
    full_name TEXT,  -- Nom complet de l'utilisateur
    birth_year INTEGER,  -- Année de naissance
    timezone TEXT,  -- Fuseau horaire / zone géographique
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    preferences TEXT  -- JSON string pour stocker les préférences utilisateur
);

-- Index pour améliorer les performances des requêtes de connexion
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Table: check_ins - Enregistrement des check-ins quotidiens
CREATE TABLE IF NOT EXISTS check_ins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    mood_score INTEGER NOT NULL CHECK(mood_score BETWEEN 0 AND 10),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index pour améliorer les performances des requêtes par date et utilisateur
CREATE INDEX IF NOT EXISTS idx_check_ins_timestamp ON check_ins(timestamp);
CREATE INDEX IF NOT EXISTS idx_check_ins_user_id ON check_ins(user_id);

-- Table: conversations - Enregistrement des conversations avec l'IA
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    tokens_used INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index pour améliorer les performances des requêtes par date et utilisateur
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);

-- Table: insights_log - Enregistrement des insights IA générés
CREATE TABLE IF NOT EXISTS insights_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    insight_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    based_on_data TEXT,
    tokens_used INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index pour améliorer les performances des requêtes par type, utilisateur et date
CREATE INDEX IF NOT EXISTS idx_insights_log_type_created ON insights_log(insight_type, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_insights_log_user_id ON insights_log(user_id);

-- Table: action_items - Suivi des objectifs et actions identifiés
CREATE TABLE IF NOT EXISTS action_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed', 'abandoned')),
    source TEXT DEFAULT 'manual',  -- 'manual' ou 'ai_extracted'
    conversation_id INTEGER,  -- Référence à la conversation d'origine si extrait par l'IA
    deadline DATETIME,  -- Date limite optionnelle
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL
);

-- Index pour améliorer les performances des requêtes par utilisateur et statut
CREATE INDEX IF NOT EXISTS idx_action_items_user_id ON action_items(user_id);
CREATE INDEX IF NOT EXISTS idx_action_items_status ON action_items(status);
CREATE INDEX IF NOT EXISTS idx_action_items_created_at ON action_items(created_at DESC);
