from nicegui import ui
from merkez.semalar.smtp import SmtpBilgileri
from merkez.servisler.smtp import smtp_baglantisini_test_et
from .._yardimci import _metin


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
        if not all(_metin(alan) for alan in (sunucu, port, kullanici, sifre, gonderen)):
            hata.text = "Yıldızlı (*) alanlar zorunludur."
            return
        if not 1 <= int(_metin(port)) <= 65535:
            hata.text = "Port 1 ile 65535 arasında olmalıdır."
            return

        bilgiler = SmtpBilgileri(
            sunucu=_metin(sunucu),
            port=int(_metin(port)),
            kullanici_adi=_metin(kullanici),
            sifre=sifre.value or "",
            gonderici_adi=_metin(gonderen),
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