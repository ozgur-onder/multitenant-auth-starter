from merkez.veritabani import vt_getir
from merkez.semalar.smtp import SmtpAyarlariGirisi


async def smtp_ayarlarini_kaydet(veri: SmtpAyarlariGirisi) -> None:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        rol = await db.fetchrow("SELECT id FROM roller WHERE rol_kodu = 1;")
        await db.execute(
            """INSERT INTO smtp_ayarlari
               (firma_kodu, rol_id, sunucu, port, kullanici_adi, sifre,
                gonderici_adi, varsayilan_mi, olusturan_guncelleyen_sicil)
               VALUES ($1, $2, $3, $4, $5, $6, $7, TRUE, $8);""",
            veri.firma_kodu,
            rol["id"] if rol else None,
            veri.sunucu,
            veri.port,
            veri.kullanici_adi,
            veri.sifre,
            veri.gonderici_adi,
            veri.olusturan_sicil,
        )