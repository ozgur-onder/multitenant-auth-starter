#!/bin/bash
# psql/kurulum.sh
# PostgreSQL init scripti — psql/ altındaki SQL dosyalarını sırayla çalıştırır.
set -e

PSQL="psql -v ON_ERROR_STOP=1 --username=$POSTGRES_USER --dbname=$POSTGRES_DB"

calistir() {
    echo "→ $1"
    $PSQL -f "$1"
}

# 1. Bağımsız tablolar (FK yok)
calistir /psql/firma/firma_tablosu.sql
calistir /psql/firma/guncelleme_loglari.sql
calistir /psql/roller/roller_table.sql
calistir /psql/roller/guncelleme_loglari.sql
calistir /psql/yetkiler/yetkiler_table.sql
calistir /psql/yetkiler/rol_yetki_guncelleme_loglari.sql

# 2. Kullanıcılar (firmaya bağımlı değil)
calistir /psql/kullanicilar/kullanicilar_table.sql

# 3. FK bağımlı tablolar
calistir /psql/kullanicilar/kullanici_yetkileri_tablosu.sql
calistir /psql/yetkiler/rol_yetkileri_tablosu.sql
calistir /psql/kullanicilar/giris_loglari.sql
calistir /psql/kullanicilar/oturum_izleme.sql
calistir /psql/smpt/smtp_table.sql
calistir /psql/smpt/smtp_loglari.sql
calistir /psql/sifreler/sifirlama_talepleri.sql
calistir /psql/sifreler/degisim_loglari.sql
calistir /psql/kullanici_davranislari/kullanici_davranis_loglari.sql

# 4. İndeksler
calistir /psql/kullanici_davranislari/sayfa_ziyaret_indeksleri.sql

# 5. Seed verisi (tablolar hazır olduktan sonra)
calistir /psql/firma/kurulum_insert.sql
calistir /psql/roller/kurulum_insert.sql
calistir /psql/yetkiler/kurulum_insert.sql
calistir /psql/yetkiler/yetkiler_sayaci.sql
calistir /psql/yetkiler/kurulum_veri_eklemeleri.sql