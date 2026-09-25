CREATE TABLE IF NOT EXISTS sayfa_ziyaret_loglari (
    id              SERIAL PRIMARY KEY,
    sicil           VARCHAR(20) NOT NULL,
    sayfa           VARCHAR(200) NOT NULL,
    sayfa_basligi   VARCHAR(200),
    oturum_token    TEXT NOT NULL,
    giris_zamani    TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    son_guncelleme  TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sure_saniye     INTEGER DEFAULT 0,
    FOREIGN KEY (sicil) REFERENCES kullanicilar(sicil)
);