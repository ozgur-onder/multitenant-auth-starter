from nicegui import ui
from ._yardimci import _alan, _sayi_alani, _metin, _aciklama


def smtp_adimini_olustur(stepper, smtp_verisi: dict) -> None:
    with ui.step("E-posta (SMTP) Ayarları"):
        _aciklama(
            "Sistemin şifremi unuttum ve bildirim e-postalarını göndereceği SMTP hesap "
            "bilgilerini girin. Daha sonra yönetim panelinden değiştirilebilir."
        )
        with ui.row().classes("w-full gap-2 flex-nowrap"):
            sunucu = _alan("SMTP Sunucu *", "mail.firma.com", genislik="flex-1")
            port   = _sayi_alani("Port *",  "465", basamak=5, genislik="w-24")
        with ui.row().classes("w-full gap-2 flex-nowrap"):
            kullanici = _alan("Gönderici E-Posta Adresi *", "ornek@firma.com", genislik="flex-1")
            sifre     = _alan("Şifre *",         password=True,     genislik="flex-1")
        gonderen = _alan("Gönderici Adı *", "İş Zekası Platformu")
        hata     = ui.label("").classes("text-negative text-caption")

        def ileri():
            hata.text = ""
            if not all([_metin(sunucu), _metin(port), _metin(kullanici), _metin(sifre)]):
                hata.text = "Yıldızlı (*) alanlar zorunludur."
                return
            if not 1 <= int(_metin(port)) <= 65535:
                hata.text = "Port 1 ile 65535 arasında olmalıdır."
                return
            smtp_verisi.update({
                "sunucu":        _metin(sunucu),
                "port":          int(_metin(port)),
                "kullanici_adi": _metin(kullanici),
                "sifre":         _metin(sifre),
                "gonderici_adi": _metin(gonderen) or _metin(kullanici),
            })
            stepper.next()

        with ui.stepper_navigation():
            ui.button("İleri", on_click=ileri).props("color=primary")