from merkez.veritabani import vt_getir
from merkez.guvenlik import sifre_dogrula, jwt_olustur
from merkez.semalar.giris import GirisGirisi, GirisCiktisi


async def giris_yap(veri: GirisGirisi, ip: str = "", tarayici: str = "") -> GirisCiktisi:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        kullanici = await db.fetchrow(
            "SELECT sicil, parola FROM kullanicilar WHERE sicil = $1 AND durum = TRUE;",
            veri.sicil,
        )
        if not kullanici or not sifre_dogrula(veri.parola, kullanici["parola"]):
            # Log tablosunda sicil FK olduğu için sadece var olan kullanıcının hatalı denemesi loglanır.
            if kullanici:
                await _giris_logu_kaydet(db, veri.sicil, "basarisiz", ip, tarayici, "Geçersiz parola.")
            raise ValueError("Sicil veya parola hatalı.")

        token = jwt_olustur(veri.sicil)
        await db.execute(
            """INSERT INTO kullanici_oturumlari (sicil, oturum_token, ip_adresi, tarayici)
               VALUES ($1, $2, $3::inet, $4);""",
            veri.sicil, token, ip or None, tarayici,
        )
        await _giris_logu_kaydet(db, veri.sicil, "basarili", ip, tarayici)
        return GirisCiktisi(token=token, sicil=veri.sicil)


async def cikis_yap(token: str) -> None:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        await db.execute(
            "UPDATE kullanici_oturumlari SET durum = 'pasif', cikis_zamani = NOW() WHERE oturum_token = $1;",
            token,
        )


async def oturum_kontrol(token: str) -> bool:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        sayi = await db.fetchval(
            "SELECT COUNT(*) FROM kullanici_oturumlari WHERE oturum_token = $1 AND durum = 'aktif';",
            token,
        )
    return (sayi or 0) > 0


async def _giris_logu_kaydet(db, sicil: str, durum: str, ip: str, tarayici: str, hata: str = "") -> None:
    await db.execute(
        """INSERT INTO kullanici_giris_loglari (sicil, durum, ip_adresi, tarayici, hata_mesaji)
           VALUES ($1, $2, $3::inet, $4, $5);""",
        sicil, durum, ip or None, tarayici, hata or None,
    )