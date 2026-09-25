INSERT INTO roller (rol_kodu, rol_adi, durum, olusturan_guncelleyen_sicil) 
VALUES (1, 'Sistem Yöneticisi', true, 'SYSTEM');

INSERT INTO rol_guncelleme_loglari (rol_kodu, rol_adi, yapilan_islem, islem_yapan_kullanici_sicil)
VALUES ('1', 'Sistem Yöneticisi', 'Rol Eklendi', 'SYSTEM');