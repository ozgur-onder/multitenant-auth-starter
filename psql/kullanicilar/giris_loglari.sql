CREATE TABLE kullanici_giris_loglari (
    id SERIAL PRIMARY KEY,
    sicil VARCHAR(20) NOT NULL,
    durum VARCHAR(20) NOT NULL,            
    ip_adresi INET,                        
    tarayici TEXT,                 
    hata_mesaji VARCHAR(255),              
    islem_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sicil) REFERENCES kullanicilar(sicil));