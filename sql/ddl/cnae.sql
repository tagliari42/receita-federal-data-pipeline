CREATE TABLE IF NOT EXISTS dim_cnae (
    cnae_codigo CHAR(7) PRIMARY KEY,
    cnae_descricao TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
