CREATE TABLE rol_yetkileri (
    rol_kodu      INT NOT NULL,
    yetki_kodu    VARCHAR(100) NOT NULL,
    atanma_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atayan_sicil  VARCHAR(20),
    PRIMARY KEY (rol_kodu, yetki_kodu),
    CONSTRAINT fk_rol FOREIGN KEY (rol_kodu) REFERENCES roller(rol_kodu) ON DELETE CASCADE,
    CONSTRAINT fk_yetki FOREIGN KEY (yetki_kodu) REFERENCES yetkiler(yetki_kodu) ON DELETE CASCADE);