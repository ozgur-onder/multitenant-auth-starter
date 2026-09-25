CREATE TABLE yetkiler (
    id          SERIAL PRIMARY KEY,
    modul       VARCHAR(100) NOT NULL,
    yetki_kodu  VARCHAR(100) UNIQUE NOT NULL,
    yetki_adi   VARCHAR(100) NOT NULL,
    durum       BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_modul_yetki UNIQUE (modul, yetki_kodu));