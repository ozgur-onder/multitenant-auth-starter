CREATE INDEX IF NOT EXISTS idx_svl_sicil  ON sayfa_ziyaret_loglari(sicil);
CREATE INDEX IF NOT EXISTS idx_svl_sayfa  ON sayfa_ziyaret_loglari(sayfa);
CREATE INDEX IF NOT EXISTS idx_svl_giris  ON sayfa_ziyaret_loglari(giris_zamani);