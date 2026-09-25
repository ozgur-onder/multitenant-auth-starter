CREATE TABLE sifre_sifirlama_talepleri (
    id SERIAL PRIMARY KEY,
    sicil VARCHAR(20) NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    talep_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    gecerlilik_suresi TIMESTAMP,           
    kullanildi BOOLEAN DEFAULT FALSE,
    ip_adresi INET,
    FOREIGN KEY (sicil) REFERENCES kullanicilar(sicil));