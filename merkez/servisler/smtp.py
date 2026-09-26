from merkez.veritabani import vt_getir
from merkez.semalar.smtp import SmtpAyarlariGirisi
from merkez.servisler.kurulum import SISTEM_YONETICISI_ROL_KODU


async def smtp_ayarlarini_kaydet(veri: SmtpAyarlariGirisi) -> None:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        await db.execute(
            """INSERT INTO smtp_ayarlari
               (firma_kodu, rol_kodu, sunucu, port, kullanici_adi, sifre,
                gonderici_adi, varsayilan_mi, olusturan_guncelleyen_sicil)
               VALUES ($1, $2, $3, $4, $5, $6, $7, TRUE, $8);""",
            veri.firma_kodu,
            SISTEM_YONETICISI_ROL_KODU,
            veri.sunucu,
            veri.port,
            veri.kullanici_adi,
            veri.sifre,
            veri.gonderici_adi,
            veri.olusturan_sicil,
        )