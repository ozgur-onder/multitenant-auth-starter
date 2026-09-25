CREATE TABLE kullanici_sifre_degisim_loglari (
    id SERIAL PRIMARY KEY,
    sicil VARCHAR(20) NOT NULL,
    tur VARCHAR(20) NOT NULL,              
    talep_eden_kullanici_sicil VARCHAR(20) NOT NULL,
    ip_adresi INET,                        
    zaman TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sicil) REFERENCES kullanicilar(sicil));