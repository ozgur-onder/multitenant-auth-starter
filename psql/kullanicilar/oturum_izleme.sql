CREATE TABLE kullanici_oturumlari (
    id SERIAL PRIMARY KEY,
    sicil TEXT NOT NULL,
    oturum_token TEXT UNIQUE NOT NULL,
    ip_adresi INET,
    tarayici TEXT,
    giris_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    son_aktivite_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cikis_zamani TIMESTAMP,
    durum VARCHAR(20) DEFAULT 'aktif',     
    FOREIGN KEY (sicil) REFERENCES kullanicilar(sicil));