from nicegui import ui
from merkez.parola_kurallari import eksik_parola_kurallari
from merkez.semalar.kurulum import KurulumGirisi
from merkez.semalar.smtp import SmtpBilgileri
from merkez.servisler.kurulum import ilk_kurulumu_yap
from .._yardimci import _metin


def kurulumu_tamamla_butonu(
    smtp_verisi: dict,
    hata: ui.label,
    *,
    sicil: ui.input,
    email: ui.input,
    ad: ui.input,
    soyad: ui.input,
    parola: ui.input,
) -> None:
    async def tikla() -> None:
        hata.text = ""
        if not all(_metin(alan) for alan in (sicil, email, ad, soyad, parola)):
            hata.text = "Yıldızlı (*) tüm alanlar zorunludur."
            return
        eksikler = eksik_parola_kurallari(parola.value or "")
        if eksikler:
            hata.text = "Parola şu kuralları sağlamıyor: " + ", ".join(eksikler) + "."
            return

        buton.props("loading")
        try:
            await ilk_kurulumu_yap(KurulumGirisi(
                sicil=_metin(sicil),
                email=_metin(email),
                ad=_metin(ad),
                soyad=_metin(soyad),
                parola=parola.value or "",
                smtp=SmtpBilgileri(**smtp_verisi),
            ))
        except ValueError as e:
            hata.text = str(e)
            return
        except Exception:
            hata.text = "Bir hata oluştu, tekrar deneyin."
            return
        finally:
            buton.props(remove="loading")

        ui.notify("Kurulum tamamlandı!", type="positive")
        ui.navigate.to("/giris")

    buton = ui.button("Kurulumu Tamamla", icon="check", on_click=tikla).props("color=positive")