import hashlib
import secrets
from urllib.parse import quote
from merkez.ayarlar import UYGULAMA_ADRESI
from merkez.veritabani import vt_getir
from merkez.guvenlik import sifreyi_hashle
from merkez.parola_kurallari import eksik_parola_kurallari
from merkez.servisler.smtp import varsayilan_smtp_ile_gonder

SIFIRLAMA_GECERLILIK_DAKIKA = 60


def _token_ozeti(token: str) -> str:
    # Veritabanında token'ın kendisi değil özeti tutulur; veritabanı sızsa bile bağlantılar kullanılamaz.
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


async def sifirlama_baglantisi_gonder(sicil: str, email: str) -> None:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        kullanici = await db.fetchrow(
            """SELECT sicil, ad, soyad, email FROM kullanicilar
               WHERE sicil = $1 AND lower(email) = lower($2) AND durum = TRUE;""",
            sicil, email,
        )
        if not kullanici:
            raise ValueError("Sicil numarası ve e-posta adresi eşleşmiyor.")

        token = secrets.token_urlsafe(32)
        async with db.transaction():
            await db.execute(
                "UPDATE sifre_sifirlama_talepleri SET kullanildi = TRUE WHERE sicil = $1 AND kullanildi = FALSE;",
                kullanici["sicil"],
            )
            await db.execute(
                """INSERT INTO sifre_sifirlama_talepleri (sicil, token, gecerlilik_suresi)
                   VALUES ($1, $2, NOW() + make_interval(mins => $3));""",
                kullanici["sicil"], _token_ozeti(token), SIFIRLAMA_GECERLILIK_DAKIKA,
            )

    baglanti = f"{UYGULAMA_ADRESI}/sifre-sifirla?token={quote(token)}"
    await varsayilan_smtp_ile_gonder(
        alici=kullanici["email"],
        konu="Şifre Sıfırlama Talebi",
        govde=(
            f"Merhaba {kullanici['ad']} {kullanici['soyad']},\n\n"
            f"Şifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın. "
            f"Bağlantı {SIFIRLAMA_GECERLILIK_DAKIKA} dakika geçerlidir ve yalnızca bir kez kullanılabilir.\n\n"
            f"{baglanti}\n\n"
            f"Bu talebi siz yapmadıysanız bu e-postayı dikkate almayın; şifreniz değişmez."
        ),
    )


async def sifirlama_baglantisi_gecerli_mi(token: str) -> bool:
    if not token:
        return False
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        sayi = await db.fetchval(
            """SELECT COUNT(*) FROM sifre_sifirlama_talepleri
               WHERE token = $1 AND kullanildi = FALSE AND gecerlilik_suresi > NOW();""",
            _token_ozeti(token),
        )
    return (sayi or 0) > 0


async def sifreyi_sifirla(token: str, yeni_sifre: str) -> None:
    eksikler = eksik_parola_kurallari(yeni_sifre)
    if eksikler:
        raise ValueError("Parola şu kuralları sağlamıyor: " + ", ".join(eksikler) + ".")
    parola_hash = sifreyi_hashle(yeni_sifre)

    havuz = await vt_getir()
    async with havuz.acquire() as db:
        async with db.transaction():
            # Aynı bağlantı iki kez kullanılamasın diye kontrol ve işaretleme tek sorguda yapılır.
            sicil = await db.fetchval(
                """UPDATE sifre_sifirlama_talepleri SET kullanildi = TRUE
                   WHERE token = $1 AND kullanildi = FALSE AND gecerlilik_suresi > NOW()
                   RETURNING sicil;""",
                _token_ozeti(token),
            )
            if not sicil:
                raise ValueError("Şifre sıfırlama bağlantısı geçersiz veya süresi dolmuş.")
            await db.execute("UPDATE kullanicilar SET parola = $1 WHERE sicil = $2;", parola_hash, sicil)
            await db.execute(
                """INSERT INTO kullanici_sifre_degisim_loglari (sicil, tur, talep_eden_kullanici_sicil)
                   VALUES ($1, 'sifirlama', $1);""",
                sicil,
            )
            # Şifre değişince açık kalmış tüm oturumlar kapatılır.
            await db.execute(
                """UPDATE kullanici_oturumlari SET durum = 'pasif', cikis_zamani = NOW()
                   WHERE sicil = $1 AND durum = 'aktif';""",
                sicil,
            )