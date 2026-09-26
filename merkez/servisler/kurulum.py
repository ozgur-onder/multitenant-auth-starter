from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy
from merkez.veritabani import vt_getir
from merkez.guvenlik import sifreyi_hashle
from merkez.parola_kurallari import eksik_parola_kurallari
from merkez.sabitler import SISTEM_YONETICISI_ROL_KODU
from merkez.semalar.kurulum import KurulumGirisi
from merkez.servisler.smtp import smtp_ayarlarini_kaydet

# Docker ilk açılışta psql/firma/kurulum_insert.sql ile ilk firmayı ekler; yönetici o firmaya bağlanır.
_VARSAYILAN_FIRMA_SORGUSU = "SELECT firma_kodu, firma_adi FROM firma WHERE durum = TRUE ORDER BY id LIMIT 1;"


async def kurulum_yapilmis_mi() -> bool:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        sayi = await db.fetchval(
            "SELECT COUNT(*) FROM kullanici_yetkileri WHERE rol_kodu = $1 AND durum = TRUE;",
            SISTEM_YONETICISI_ROL_KODU,
        )
    return (sayi or 0) > 0


async def varsayilan_firmayi_getir() -> Record | None:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        return await db.fetchrow(_VARSAYILAN_FIRMA_SORGUSU)


async def _varsayilan_firma_kodu(db: PoolConnectionProxy) -> str:
    firma = await db.fetchrow(_VARSAYILAN_FIRMA_SORGUSU)
    if not firma:
        raise ValueError("Sistemde kayıtlı firma bulunamadı. Veritabanı kurulumunu kontrol edin.")
    return firma["firma_kodu"]


async def ilk_kurulumu_yap(veri: KurulumGirisi) -> None:
    eksikler = eksik_parola_kurallari(veri.parola)
    if eksikler:
        raise ValueError("Parola şu kuralları sağlamıyor: " + ", ".join(eksikler) + ".")
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

            firma_kodu = await _varsayilan_firma_kodu(db)

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
                veri.sicil, firma_kodu, SISTEM_YONETICISI_ROL_KODU,
            )
            await smtp_ayarlarini_kaydet(db, firma_kodu, veri.sicil, veri.smtp)