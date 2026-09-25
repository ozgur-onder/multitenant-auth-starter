CREATE TABLE roller (
    id SERIAL PRIMARY KEY,
    rol_kodu INT UNIQUE NOT NULL,
    rol_adi VARCHAR(255) NOT NULL,
    durum BOOLEAN DEFAULT TRUE,
    olusturma_guncelleme_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    olusturan_guncelleyen_sicil VARCHAR(20));