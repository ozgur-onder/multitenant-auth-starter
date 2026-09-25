CREATE TABLE kullanici_yetkileri (
    id SERIAL PRIMARY KEY,
    sicil VARCHAR(20) NOT NULL,
    firma_id INT NOT NULL,
    rol_id INT NOT NULL,
    tanimlayan_kullanici_sicil VARCHAR(20),
    durum BOOLEAN DEFAULT TRUE,
    olusturma_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sicil) REFERENCES kullanicilar(sicil),
    FOREIGN KEY (firma_id) REFERENCES firma(id),
    FOREIGN KEY (rol_id) REFERENCES roller(id));