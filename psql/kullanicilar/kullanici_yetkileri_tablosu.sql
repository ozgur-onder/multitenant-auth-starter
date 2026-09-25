CREATE TABLE kullanici_yetkileri (
    id SERIAL PRIMARY KEY,
    sicil VARCHAR(20) NOT NULL,
    firma_kodu INT NOT NULL,
    rol_kodu INT NOT NULL,
    tanimlayan_kullanici_sicil VARCHAR(20),
    durum BOOLEAN DEFAULT TRUE,
    olusturma_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sicil) REFERENCES kullanicilar(sicil),
    FOREIGN KEY (firma_kodu) REFERENCES firma(firma_kodu),
    FOREIGN KEY (rol_kodu) REFERENCES roller(rol_kodu));