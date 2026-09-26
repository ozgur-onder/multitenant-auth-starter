from nicegui import ui
from merkez.semalar.smtp import SmtpBilgileri
from merkez.servisler.smtp import smtp_baglantisini_test_et
from sayfalar.ortak.bilesenler import alan_degeri


def smtp_test_et_ilerle_butonu(
    stepper: ui.stepper,
    smtp_verisi: dict,
    hata: ui.label,
    *,
    sunucu: ui.input,
    port: ui.input,
    kullanici: ui.input,
    sifre: ui.input,
    gonderen: ui.input,
) -> None:
    async def tikla() -> None:
        hata.text = ""
        if not all(alan_degeri(girdi) for girdi in (sunucu, port, kullanici, sifre, gonderen)):
            hata.text = "Yıldızlı (*) alanlar zorunludur."
            return
        if not 1 <= int(alan_degeri(port)) <= 65535:
            hata.text = "Port 1 ile 65535 arasında olmalıdır."
            return

        bilgiler = SmtpBilgileri(
            sunucu=alan_degeri(sunucu),
            port=int(alan_degeri(port)),
            kullanici_adi=alan_degeri(kullanici),
            sifre=sifre.value or "",
            gonderici_adi=alan_degeri(gonderen),
        )
        buton.props("loading")
        try:
            await smtp_baglantisini_test_et(bilgiler)
        except ValueError as e:
            hata.text = str(e)
            return
        finally:
            buton.props(remove="loading")

        smtp_verisi.clear()
        smtp_verisi.update(bilgiler.model_dump())
        ui.notify("SMTP bağlantısı doğrulandı.", type="positive")
        stepper.next()

    buton = ui.button("Test Et ve İlerle", icon="send", on_click=tikla).props("color=primary")