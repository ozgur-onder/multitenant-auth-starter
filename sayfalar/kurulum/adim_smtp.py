from nicegui import ui
from sayfalar.ortak.bilesenler import alan, sayi_alani, aciklama, degisince_hatayi_temizle
from .butonlar.smtp_test_et_ilerle import smtp_test_et_ilerle_butonu


def smtp_adimini_olustur(stepper: ui.stepper, smtp_verisi: dict) -> None:
    with ui.step("E-posta (SMTP) Ayarları"):
        aciklama(
            "Sistemin şifremi unuttum ve bildirim e-postalarını göndereceği SMTP hesap "
            "bilgilerini girin. Bilgiler kaydedilmeden önce sunucuya bağlanılarak test edilir."
        )
        with ui.row().classes("w-full gap-2 no-wrap"):
            sunucu = alan("SMTP Sunucu *", "mail.firma.com", genislik="flex-1")
            port   = sayi_alani("Port *",  "465", basamak=5, genislik="w-24")
        with ui.row().classes("w-full gap-2 no-wrap"):
            kullanici = alan("Gönderici E-Posta Adresi *", "ornek@firma.com", genislik="flex-1")
            sifre     = alan("Şifre *", password=True, genislik="flex-1")
        gonderen = alan("Gönderici Adı *", "Lütfen Yanıtlamayınız")
        hata     = ui.label("").classes("text-negative text-caption")
        degisince_hatayi_temizle(hata, sunucu, port, kullanici, sifre, gonderen)

        with ui.stepper_navigation():
            smtp_test_et_ilerle_butonu(
                stepper, smtp_verisi, hata,
                sunucu=sunucu, port=port, kullanici=kullanici, sifre=sifre, gonderen=gonderen,
            )