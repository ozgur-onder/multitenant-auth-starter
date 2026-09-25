INSERT INTO rol_yetkileri (rol_kodu, yetki_kodu, atayan_sicil)
SELECT 1, yetki_kodu, 'SYSTEM' FROM yetkiler WHERE durum = TRUE;