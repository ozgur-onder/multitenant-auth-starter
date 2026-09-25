from merkez.veritabani import vt_getir
from merkez.guvenlik import sifreyi_hashle
from merkez.semalar.kurulum import KurulumGirisi


async def ilk_kurulumu_yap(veri: KurulumGirisi) -> None:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        kullanici_sayisi = await db.fetchval("SELECT COUNT(*) FROM kullanicilar;")
        if kullanici_sayisi > 0:
            raise ValueError("Sistem zaten kurulmuş. Tekrar kurulum yapılamaz.")

        # Firma oluştur
        await db.execute(
            """INSERT INTO firma (firma_kodu, firma_adi, olusturan_guncelleyen_sicil)
               VALUES ($1, $2, 'SYSTEM')
               ON CONFLICT (firma_kodu) DO NOTHING;""",
            veri.firma_kodu, veri.firma_adi,
        )

        # Sistem Yöneticisi rolünü oluştur (yoksa)
        await db.execute(
            """INSERT INTO roller (rol_kodu, rol_adi, olusturan_guncelleyen_sicil)
               VALUES (1, 'Sistem Yöneticisi', 'SYSTEM')
               ON CONFLICT (rol_kodu) DO NOTHING;""",
        )

        # Admin kullanıcısını oluştur
        hashli_parola = sifreyi_hashle(veri.parola)
        await db.execute(
            """INSERT INTO kullanicilar (sicil, ad, soyad, email, parola, olusturan_kullanici_sicil)
               VALUES ($1, $2, $3, $4, $5, 'SYSTEM');""",
            veri.sicil, veri.ad, veri.soyad, veri.email, hashli_parola,
        )

        # Kullanıcıya firma + rol ata
        firma = await db.fetchrow("SELECT id FROM firma WHERE firma_kodu = $1;", veri.firma_kodu)
        await db.execute(
            """INSERT INTO kullanici_yetkileri (sicil, firma_id, rol_id, tanimlayan_kullanici_sicil)
               VALUES ($1, $2, 1, 'SYSTEM');""",
            veri.sicil, firma["id"],
        )
