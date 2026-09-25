CREATE TABLE firma (
    id SERIAL PRIMARY KEY,
    firma_kodu VARCHAR(50) UNIQUE NOT NULL,
    firma_adi VARCHAR(255) NOT NULL,
    durum BOOLEAN DEFAULT TRUE,            
    olusturma_guncelleme_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    olusturan_guncelleyen_sicil VARCHAR(20));