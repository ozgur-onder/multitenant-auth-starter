import secrets
from datetime import datetime, timedelta, timezone
from merkez.veritabani import vt_getir
from merkez.guvenlik import sifreyi_hashle


async def sifirlama_talebi_olustur(email: str, ip_adresi: str | None = None) -> str | None:
    """E-postaya göre kullanıcı arar, sıfırlama tokeni oluşturur ve DB'ye kaydeder."""
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        kullanici = await db.fetchrow(
            "SELECT sicil FROM kullanicilar WHERE email = $1 AND durum = true;", email
        )
        if not kullanici:
            return None

        token = secrets.token_urlsafe(40)
        gecerlilik = datetime.now(timezone.utc) + timedelta(hours=1)

        await db.execute(
            """INSERT INTO sifre_sifirlama_talepleri (sicil, token, gecerlilik_suresi, ip_adresi)
               VALUES ($1, $2, $3, $4::inet);""",
            kullanici["sicil"], token, gecerlilik, ip_adresi,
        )
    return token


async def sifreyi_sifirla(token: str, yeni_parola: str) -> bool:
    """Geçerli token ile kullanıcının parolasını günceller."""
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        talep = await db.fetchrow(
            """SELECT sicil FROM sifre_sifirlama_talepleri
               WHERE token = $1
                 AND kullanildi = false
                 AND gecerlilik_suresi > $2;""",
            token, datetime.now(timezone.utc),
        )
        if not talep:
            return False

        hashli = sifreyi_hashle(yeni_parola)
        await db.execute(
            "UPDATE kullanicilar SET parola = $1 WHERE sicil = $2;",
            hashli, talep["sicil"],
        )
        await db.execute(
            "UPDATE sifre_sifirlama_talepleri SET kullanildi = true WHERE token = $1;",
            token,
        )
    return True
