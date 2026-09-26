import asyncio
import smtplib
import socket
import ssl
from asyncpg.pool import PoolConnectionProxy
from merkez.sabitler import SISTEM_YONETICISI_ROL_KODU
from merkez.semalar.smtp import SmtpBilgileri

_ZAMAN_ASIMI_SANIYE = 10
_SSL_PORTU = 465


def _baglan_ve_giris_yap(bilgiler: SmtpBilgileri) -> None:
    baglam = ssl.create_default_context()
    if bilgiler.port == _SSL_PORTU:
        istemci = smtplib.SMTP_SSL(bilgiler.sunucu, bilgiler.port, timeout=_ZAMAN_ASIMI_SANIYE, context=baglam)
    else:
        istemci = smtplib.SMTP(bilgiler.sunucu, bilgiler.port, timeout=_ZAMAN_ASIMI_SANIYE)
    with istemci:
        istemci.ehlo()
        if bilgiler.port != _SSL_PORTU:
            # Şifre ağda açık metin gitmesin diye şifrelenmemiş bağlantıda giriş yapılmaz.
            if not istemci.has_extn("starttls"):
                raise ValueError("Sunucu şifreli bağlantıyı (STARTTLS) desteklemiyor.")
            istemci.starttls(context=baglam)
            istemci.ehlo()
        istemci.login(bilgiler.kullanici_adi, bilgiler.sifre)


async def smtp_baglantisini_test_et(bilgiler: SmtpBilgileri) -> None:
    try:
        await asyncio.to_thread(_baglan_ve_giris_yap, bilgiler)
    except smtplib.SMTPAuthenticationError:
        raise ValueError("SMTP mail adresi veya şifresi hatalı.")
    except smtplib.SMTPNotSupportedError:
        raise ValueError("SMTP sunucusu mail adresi/şifre ile girişi desteklemiyor.")
    except socket.gaierror:
        raise ValueError("SMTP sunucusu bulunamadı. Sunucu adresini kontrol edin.")
    except ConnectionRefusedError:
        raise ValueError("SMTP sunucusu bağlantıyı reddetti. Port numarasını kontrol edin.")
    except ssl.SSLCertVerificationError:
        raise ValueError("SMTP sunucusunun SSL sertifikası doğrulanamadı.")
    except ssl.SSLError:
        raise ValueError("SSL/TLS hatası. Port numarasının doğru olduğundan emin olun (SSL: 465, STARTTLS: 587).")
    except (TimeoutError, smtplib.SMTPServerDisconnected):
        raise ValueError("SMTP sunucusu yanıt vermedi. Sunucu adresini ve portu kontrol edin.")
    except (smtplib.SMTPException, OSError) as hata:
        raise ValueError(f"SMTP bağlantısı kurulamadı: {hata}")


async def smtp_ayarlarini_kaydet(db: PoolConnectionProxy, firma_kodu: str, olusturan_sicil: str, bilgiler: SmtpBilgileri) -> None:
    await db.execute(
        """INSERT INTO smtp_ayarlari
           (firma_kodu, rol_kodu, sunucu, port, kullanici_adi, sifre,
            gonderici_adi, varsayilan_mi, olusturan_guncelleyen_sicil)
           VALUES ($1, $2, $3, $4, $5, $6, $7, TRUE, $8);""",
        firma_kodu,
        SISTEM_YONETICISI_ROL_KODU,
        bilgiler.sunucu,
        bilgiler.port,
        bilgiler.kullanici_adi,
        bilgiler.sifre,
        bilgiler.gonderici_adi,
        olusturan_sicil,
    )