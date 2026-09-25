#!/bin/bash
# PostgreSQL Docker init scripti.
# /docker-entrypoint-initdb.d/ klasörü alt dizinleri çalıştırmaz,
# bu yüzden SQL dosyaları bu script aracılığıyla sırayla çalıştırılır.
set -e

PSQL="psql -v ON_ERROR_STOP=1 --username $POSTGRES_USER --dbname $POSTGRES_DB"

echo "──────────────────────────────────────────────"
echo "  Veritabanı şeması oluşturuluyor..."
echo "──────────────────────────────────────────────"

# 1. Bağımsız tablolar (FK yok)
echo "→ [1/6] Temel tablolar..."
$PSQL -f /psql/firma/firma_table.sql
$PSQL -f /psql/kullanicilar/kullanicilar_table.sql
$PSQL -f /psql/roller/roller_table.sql
$PSQL -f /psql/yetkiler/yetkiler_table.sql

# 2. FK bağımlı tablolar
echo "→ [2/6] İlişkisel tablolar..."
$PSQL -f /psql/kullanicilar/kullanici_yetkileri_tablosu.sql
$PSQL -f /psql/yetkiler/rol_yetkileri_tablosu.sql
$PSQL -f /psql/kullanicilar/oturum_izleme.sql
$PSQL -f /psql/kullanicilar/giris_loglari.sql
$PSQL -f /psql/sifreler/sifirlama_talepleri.sql
$PSQL -f /psql/sifreler/degisim_loglari.sql
$PSQL -f /psql/smpt/smtp_table.sql
$PSQL -f /psql/smpt/smtp_loglari.sql

# 3. Log ve güncelleme tabloları
echo "→ [3/6] Log tabloları..."
$PSQL -f /psql/firma/guncelleme_loglari.sql
$PSQL -f /psql/roller/guncelleme_loglari.sql
$PSQL -f /psql/yetkiler/rol_yetki_guncelleme_loglari.sql
$PSQL -f /psql/kullanici_davranislari/kullanici_davranis_loglari.sql

# 4. İndeksler
echo "→ [4/6] İndeksler..."
$PSQL -f /psql/kullanici_davranislari/sayfa_ziyaret_indeksleri.sql

# 5. Başlangıç verileri
echo "→ [5/6] Başlangıç verileri yükleniyor..."
$PSQL -f /psql/firma/kurulum_insert.sql
$PSQL -f /psql/roller/kurulum_insert.sql
$PSQL -f /psql/yetkiler/kurulum_insert.sql
$PSQL -f /psql/yetkiler/kurulum_veri_eklemeleri.sql

# 6. Sequence güncelleme
echo "→ [6/6] Sequence değerleri güncelleniyor..."
$PSQL -f /psql/yetkiler/yetkiler_sayaci.sql

echo "──────────────────────────────────────────────"
echo "  Veritabanı başarıyla hazırlandı."
echo "──────────────────────────────────────────────"