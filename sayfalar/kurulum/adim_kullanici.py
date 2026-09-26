from nicegui import ui
from ._yardimci import _alan, _aciklama, _buyuk_harfle_yazdir, _degisince_hatayi_temizle
from .parola_kurallari import parola_kurallarini_goster
from .butonlar.sicil_uret import sicil_uret_butonu
from .butonlar.kurulumu_tamamla import kurulumu_tamamla_butonu


def kullanici_adimini_olustur(stepper: ui.stepper, smtp_verisi: dict, firma_adi: str) -> None:
    with ui.step("Sistem Yöneticisi"):
        _aciklama(
            f"Sisteme ilk giriş yapacak yönetici hesabını oluşturun. Bu kullanıcı "
            f"'{firma_adi}' firmasına en yüksek yetkiye sahip Sistem Yöneticisi rolüyle tanımlanır."
        )
        with ui.row().classes("w-full gap-2 no-wrap"):
            sicil = _alan("Sicil No *", "20260001",        genislik="flex-1")
            email = _alan("E-posta *",  "admin@firma.com", genislik="flex-1")
        with ui.row().classes("w-full gap-2 no-wrap"):
            ad    = _alan("Ad *",    genislik="flex-1")
            soyad = _alan("Soyad *", genislik="flex-1")
        _buyuk_harfle_yazdir(ad)
        _buyuk_harfle_yazdir(soyad)
        with ui.row().classes("w-full gap-2 no-wrap"):
            parola        = _alan("Parola *",        password=True, genislik="flex-1")
            parola_tekrar = _alan("Parola Tekrar *", password=True, genislik="flex-1")
        parola_kurallarini_goster(parola, parola_tekrar)
        hata = ui.label("").classes("text-negative text-caption")
        _degisince_hatayi_temizle(hata, sicil, email, ad, soyad, parola, parola_tekrar)
        sicil_uret_butonu(sicil, hata)

        with ui.stepper_navigation():
            ui.button("Geri", on_click=stepper.previous).props("flat")
            kurulumu_tamamla_butonu(
                smtp_verisi, hata,
                sicil=sicil, email=email, ad=ad, soyad=soyad,
                parola=parola, parola_tekrar=parola_tekrar,
            )