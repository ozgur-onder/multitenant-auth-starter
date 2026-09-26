from merkez.veritabani import vt_getir
from merkez.guvenlik import sifreyi_hashle
from merkez.semalar.kurulum import KurulumGirisi

SISTEM_YONETICISI_ROL_KODU = 1


async def kurulum_yapilmis_mi() -> bool:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        sayi = await db.fetchval(
            "SELECT COUNT(*) FROM kullanici_yetkileri WHERE rol_kodu = $1 AND durum = TRUE;",
            SISTEM_YONETICISI_ROL_KODU,
        )
    return (sayi or 0) > 0


async def ilk_kurulumu_yap(veri: KurulumGirisi) -> None:
    parola_hash = sifreyi_hashle(veri.parola)
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        async with db.transaction():
            # Aynı anda iki kurulum isteği gelirse ikincisi birincinin bitmesini bekler.
            await db.execute("LOCK TABLE kullanici_yetkileri IN EXCLUSIVE MODE;")
            yonetici_var = await db.fetchval(
                "SELECT COUNT(*) FROM kullanici_yetkileri WHERE rol_kodu = $1 AND durum = TRUE;",
                SISTEM_YONETICISI_ROL_KODU,
            )
            if yonetici_var:
                raise ValueError("Kurulum zaten yapılmış.")

            eklenen_firma = await db.fetchval(
                """INSERT INTO firma (firma_kodu, firma_adi, olusturan_guncelleyen_sicil)
                   VALUES ($1, $2, $3)
                   ON CONFLICT (firma_kodu) DO NOTHING
                   RETURNING firma_kodu;""",
                veri.firma_kodu, veri.firma_adi, veri.sicil,
            )
            if eklenen_firma:
                await db.execute(
                    """INSERT INTO firma_guncelleme_loglari
                       (firma_kodu, firma_adi, yapilan_islem, islem_yapan_kullanici_sicil)
                       VALUES ($1, $2, 'Firma Eklendi', $3);""",
                    veri.firma_kodu, veri.firma_adi, veri.sicil,
                )

            await db.execute(
                """INSERT INTO kullanicilar
                   (sicil, ad, soyad, email, parola, olusturan_kullanici_sicil)
                   VALUES ($1, $2, $3, $4, $5, 'SYSTEM');""",
                veri.sicil, veri.ad, veri.soyad, veri.email, parola_hash,
            )

            await db.execute(
                """INSERT INTO kullanici_yetkileri
                   (sicil, firma_kodu, rol_kodu, tanimlayan_kullanici_sicil)
                   VALUES ($1, $2, $3, 'SYSTEM');""",
                veri.sicil, veri.firma_kodu, SISTEM_YONETICISI_ROL_KODU,
            )