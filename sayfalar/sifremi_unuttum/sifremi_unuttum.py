from nicegui import ui
from sayfalar.ortak.bilesenler import alan, MesajKutusu
from sayfalar.ortak.kimlik_iskeleti import kimlik_iskeleti
from sayfalar.ortak.butonlar.giris_sayfasina_don import giris_sayfasina_don_butonu
from .butonlar.baglanti_gonder import baglanti_gonder_butonu


@ui.page("/sifremi-unuttum")
async def sifremi_unuttum_sayfasi():
    with kimlik_iskeleti(
        "Şifremi Unuttum",
        "Sicil numaranızı ve kayıtlı e-posta adresinizi girin. Bilgiler eşleşirse "
        "şifre sıfırlama bağlantısı e-posta adresinize gönderilir.",
        "lock_reset",
    ) as icerik:
        sicil = alan("Sicil No", "20260001", ikon="badge").props("outlined")
        email = alan("E-posta", "ad@firma.com", ikon="mail").props("outlined")
        mesaj = MesajKutusu()
        sicil.on_value_change(mesaj.temizle)
        email.on_value_change(mesaj.temizle)
        baglanti_gonder_butonu(icerik, mesaj, sicil=sicil, email=email)
        giris_sayfasina_don_butonu()