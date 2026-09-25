CREATE TABLE rol_yetki_guncelleme_loglari (
    id SERIAL PRIMARY KEY,
    rol_kodu INT NOT NULL,
    yapilan_islem TEXT NOT NULL,
    islem_yapan_kullanici_sicil VARCHAR(20),
    islem_zamani TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP);