from nicegui import ui, app as nicegui_app
from merkez.servisler import giris as servis_giris
from merkez.servisler.kurulum import kurulum_yapilmis_mi
from sayfalar.ortak.bilesenler import alan, MesajKutusu
from sayfalar.ortak.kimlik_iskeleti import kimlik_iskeleti
from .butonlar.giris_yap import giris_yap_butonu
from .butonlar.sifremi_unuttum import sifremi_unuttum_butonu


@ui.page("/giris")
async def giris_sayfasi():
    if not await kurulum_yapilmis_mi():
        ui.navigate.to("/kurulum")
        return
    token = nicegui_app.storage.user.get("oturum_token")
    if token and await servis_giris.oturum_kontrol(token):
        ui.navigate.to("/panel")
        return

    with kimlik_iskeleti("Giriş Yap", "Sicil numaranız veya e-posta adresinizle giriş yapın.", "lock"):
        kimlik = alan("Sicil No veya E-posta", "20260001 / ad@firma.com", ikon="person").props("outlined")
        parola = alan("Parola", password=True, ikon="key").props("outlined")
        mesaj = MesajKutusu()
        kimlik.on_value_change(mesaj.temizle)
        parola.on_value_change(mesaj.temizle)
        giris_yap_butonu(mesaj, kimlik=kimlik, parola=parola)
        sifremi_unuttum_butonu()