CREATE TABLE firma_guncelleme_loglari(
    id SERIAL PRIMARY KEY,
    firma_kodu VARCHAR(50) NOT NULL,
    firma_adi VARCHAR(255) NOT NULL,
    yapilan_islem VARCHAR(255),
    islem_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    islem_yapan_kullanici_sicil VARCHAR(20));