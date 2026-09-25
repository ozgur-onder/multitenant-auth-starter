from datetime import datetime, timezone
from merkez.veritabani import vt_getir
from merkez.guvenlik import sifre_dogrula, jwt_olustur, jwt_coz


async def giris_yap(
    sicil: str,
    parola: str,
    ip_adresi: str | None = None,
    tarayici: str | None = None,
) -> dict | None:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        kullanici = await db.fetchrow(
            "SELECT sicil, ad, soyad, parola, durum FROM kullanicilar WHERE sicil = $1;",
            sicil,
        )

        if not kullanici or not kullanici["durum"]:
            await _giris_logu_kaydet(db, sicil, "basarisiz", ip_adresi, tarayici, "Kullanıcı bulunamadı veya pasif.")
            return None

        if not sifre_dogrula(parola, kullanici["parola"]):
            await _giris_logu_kaydet(db, sicil, "basarisiz", ip_adresi, tarayici, "Hatalı şifre.")
            return None

        token = jwt_olustur({"sub": sicil, "ad": kullanici["ad"], "soyad": kullanici["soyad"]})

        await db.execute(
            """INSERT INTO kullanici_oturumlari (sicil, oturum_token, ip_adresi, tarayici)
               VALUES ($1, $2, $3::inet, $4);""",
            sicil, token, ip_adresi, tarayici,
        )

        await _giris_logu_kaydet(db, sicil, "basarili", ip_adresi, tarayici, None)

        return {
            "token": token,
            "sicil": sicil,
            "ad": kullanici["ad"],
            "soyad": kullanici["soyad"],
        }


async def cikis_yap(token: str) -> None:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        await db.execute(
            """UPDATE kullanici_oturumlari
               SET cikis_zamani = $1, durum = 'kapali'
               WHERE oturum_token = $2 AND durum = 'aktif';""",
            datetime.now(timezone.utc), token,
        )


async def oturum_kontrol(token: str) -> bool:
    if not jwt_coz(token):
        return False

    havuz = await vt_getir()
    async with havuz.acquire() as db:
        oturum = await db.fetchrow(
            "SELECT id FROM kullanici_oturumlari WHERE oturum_token = $1 AND durum = 'aktif';",
            token,
        )
        if not oturum:
            return False

        await db.execute(
            "UPDATE kullanici_oturumlari SET son_aktivite_zamani = $1 WHERE oturum_token = $2;",
            datetime.now(timezone.utc), token,
        )
    return True


async def _giris_logu_kaydet(
    db, sicil: str, durum: str, ip: str | None, tarayici: str | None, hata: str | None
) -> None:
    try:
        await db.execute(
            """INSERT INTO kullanici_giris_loglari (sicil, durum, ip_adresi, tarayici, hata_mesaji)
               VALUES ($1, $2, $3::inet, $4, $5);""",
            sicil, durum, ip, tarayici, hata,
        )
    except Exception:
        pass
