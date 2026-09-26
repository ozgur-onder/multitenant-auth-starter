import secrets
from merkez.veritabani import vt_getir
from merkez.guvenlik import sifreyi_hashle


async def sifirlama_talebi_olustur(email: str) -> str | None:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        kullanici = await db.fetchrow(
            "SELECT sicil FROM kullanicilar WHERE email = $1 AND durum = TRUE;", email
        )
        if not kullanici:
            return None
        token = secrets.token_urlsafe(32)
        async with db.transaction():
            await db.execute(
                "UPDATE sifre_sifirlama_talepleri SET kullanildi = TRUE WHERE sicil = $1 AND kullanildi = FALSE;",
                kullanici["sicil"],
            )
            await db.execute(
                """INSERT INTO sifre_sifirlama_talepleri (sicil, token, gecerlilik_suresi)
                   VALUES ($1, $2, NOW() + INTERVAL '1 hour');""",
                kullanici["sicil"], token,
            )
        return token


async def sifreyi_sifirla(token: str, yeni_sifre: str) -> bool:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        talep = await db.fetchrow(
            """SELECT sicil FROM sifre_sifirlama_talepleri
               WHERE token = $1 AND kullanildi = FALSE AND gecerlilik_suresi > NOW();""",
            token,
        )
        if not talep:
            return False
        async with db.transaction():
            await db.execute(
                "UPDATE kullanicilar SET parola = $1 WHERE sicil = $2;",
                sifreyi_hashle(yeni_sifre), talep["sicil"],
            )
            await db.execute(
                "UPDATE sifre_sifirlama_talepleri SET kullanildi = TRUE WHERE token = $1;", token,
            )
        return True