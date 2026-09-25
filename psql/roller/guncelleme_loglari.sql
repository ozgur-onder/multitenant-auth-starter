CREATE TABLE rol_guncelleme_loglari (
    id SERIAL PRIMARY KEY,
    rol_kodu INT NOT NULL,
    rol_adi VARCHAR(255) NOT NULL,
    yapilan_islem VARCHAR(255) NOT NULL,
    islem_yapan_kullanici_sicil VARCHAR(20),
    islem_zamani TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP);