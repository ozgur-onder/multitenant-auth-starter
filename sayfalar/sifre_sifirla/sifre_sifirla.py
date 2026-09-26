from nicegui import ui
from merkez.servisler.sifre import sifirlama_baglantisi_gecerli_mi
from sayfalar.ortak.bilesenler import alan, MesajKutusu
from sayfalar.ortak.kimlik_iskeleti import kimlik_iskeleti, sonuc_ekrani
from sayfalar.ortak.parola_kurallari import parola_kurallarini_goster
from sayfalar.ortak.butonlar.giris_sayfasina_don import giris_sayfasina_don_butonu
from .butonlar.sifreyi_kaydet import sifreyi_kaydet_butonu


@ui.page("/sifre-sifirla")
async def sifre_sifirla_sayfasi(token: str = ""):
    with kimlik_iskeleti("Yeni Şifre Belirle", "Hesabınız için yeni bir parola belirleyin.", "password") as icerik:
        if not await sifirlama_baglantisi_gecerli_mi(token):
            sonuc_ekrani(
                icerik, "link_off", "negative", "Bağlantı geçersiz",
                "Şifre sıfırlama bağlantısı geçersiz, kullanılmış veya süresi dolmuş. Yeni bir bağlantı isteyin.",
            )
            with icerik:
                ui.button("Yeni bağlantı iste", icon="lock_reset", on_click=lambda: ui.navigate.to("/sifremi-unuttum")) \
                    .props("unelevated no-caps color=primary").classes("w-full")
                giris_sayfasina_don_butonu()
            return

        parola        = alan("Yeni Parola",        password=True, ikon="key").props("outlined")
        parola_tekrar = alan("Yeni Parola Tekrar", password=True, ikon="key").props("outlined")
        parola_kurallarini_goster(parola, parola_tekrar)
        mesaj = MesajKutusu()
        parola.on_value_change(mesaj.temizle)
        parola_tekrar.on_value_change(mesaj.temizle)
        sifreyi_kaydet_butonu(icerik, mesaj, token, parola=parola, parola_tekrar=parola_tekrar)
        giris_sayfasina_don_butonu()