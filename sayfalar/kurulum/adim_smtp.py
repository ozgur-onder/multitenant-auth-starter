from nicegui import ui
from ._yardimci import _alan


def smtp_adimini_olustur(stepper, smtp_verisi: dict) -> None:
    with ui.step("E-posta (SMTP) Ayarları"):
        sunucu    = _alan("SMTP Sunucu *",   "smtp.gmail.com")
        port      = ui.number("Port *", value=587, min=1, max=65535).classes("w-full")
        kullanici = _alan("Kullanıcı Adı *", "ornek@firma.com")
        sifre     = _alan("Şifre *",         password=True)
        gonderen  = _alan("Gönderici Adı",   "İş Zekası Platformu")
        hata      = ui.label("").classes("text-negative text-caption")

        def ileri():
            hata.text = ""
            if not all([sunucu.value.strip(), kullanici.value.strip(), sifre.value.strip()]):
                hata.text = "Yıldızlı (*) alanlar zorunludur."
                return
            smtp_verisi.update({
                "sunucu":        sunucu.value.strip(),
                "port":          int(port.value or 587),
                "kullanici_adi": kullanici.value.strip(),
                "sifre":         sifre.value.strip(),
                "gonderici_adi": gonderen.value.strip() or kullanici.value.strip(),
            })
            stepper.next()

        with ui.stepper_navigation():
            ui.button("İleri", on_click=ileri).props("color=primary")