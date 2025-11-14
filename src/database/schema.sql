-- Schéma de base de données pour Serene
-- Table: check_ins - Enregistrement des check-ins quotidiens

CREATE TABLE IF NOT EXISTS check_ins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    mood_score INTEGER NOT NULL CHECK(mood_score BETWEEN 1 AND 10),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index pour améliorer les performances des requêtes par date
CREATE INDEX IF NOT EXISTS idx_check_ins_timestamp ON check_ins(timestamp);

-- Table: conversations - Enregistrement des conversations avec l'IA
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    tokens_used INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index pour améliorer les performances des requêtes par date
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);

-- Table: insights_log - Enregistrement des insights IA générés
CREATE TABLE IF NOT EXISTS insights_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    insight_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    based_on_data TEXT,
    tokens_used INTEGER
);

-- Index pour améliorer les performances des requêtes par type et date
CREATE INDEX IF NOT EXISTS idx_insights_log_type_created ON insights_log(insight_type, created_at DESC);
