CREATE TABLE kullanicilar (
    id SERIAL PRIMARY KEY,
    sicil VARCHAR(20) UNIQUE NOT NULL, 
    ad VARCHAR(100) NOT NULL,
    soyad VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    parola VARCHAR(255) NOT NULL,        
    durum BOOLEAN DEFAULT TRUE,          
    olusturma_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    olusturan_kullanici_sicil VARCHAR(20));