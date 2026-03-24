-- Minu esimene UrbanStyle paring
-- Nimi: [Sinu Nimi]
-- Kuupaev: [Tanane kuupaev]

-- Loo meeskonnaliikmete tabel
CREATE TABLE IF NOT EXISTS team_members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(100),
    week INT DEFAULT 0,
    joined_at TIMESTAMP DEFAULT NOW()
);

-- Lisa minu andmed
INSERT INTO team_members (name, role, week)
VALUES ('[Kätlin Tootmaa]', 'Andmeanaluutik', 0);

-- Vaata tulemust
SELECT * FROM team_members ORDER BY joined_at;