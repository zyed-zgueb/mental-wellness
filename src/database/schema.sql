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
