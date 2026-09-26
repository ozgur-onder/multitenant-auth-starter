from nicegui import ui
from merkez.parola_kurallari import eksik_parola_kurallari
from merkez.semalar.kurulum import KurulumGirisi
from merkez.semalar.smtp import SmtpBilgileri
from merkez.servisler.kurulum import ilk_kurulumu_yap
from sayfalar.ortak.bilesenler import alan_degeri


def kurulumu_tamamla_butonu(
    smtp_verisi: dict,
    hata: ui.label,
    *,
    sicil: ui.input,
    email: ui.input,
    ad: ui.input,
    soyad: ui.input,
    parola: ui.input,
    parola_tekrar: ui.input,
) -> None:
    async def tikla() -> None:
        hata.text = ""
        if not all(alan_degeri(girdi) for girdi in (sicil, email, ad, soyad, parola, parola_tekrar)):
            hata.text = "Yıldızlı (*) tüm alanlar zorunludur."
            return
        eksikler = eksik_parola_kurallari(parola.value or "")
        if eksikler:
            hata.text = "Parola şu kuralları sağlamıyor: " + ", ".join(eksikler) + "."
            return
        if parola.value != parola_tekrar.value:
            hata.text = "Parolalar eşleşmiyor."
            return

        buton.props("loading")
        try:
            await ilk_kurulumu_yap(KurulumGirisi(
                sicil=alan_degeri(sicil),
                email=alan_degeri(email),
                ad=alan_degeri(ad),
                soyad=alan_degeri(soyad),
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