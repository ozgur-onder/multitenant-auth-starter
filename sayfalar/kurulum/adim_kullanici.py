from nicegui import ui
from merkez.servisler.kurulum import ilk_kurulumu_yap
from merkez.servisler.smtp import smtp_ayarlarini_kaydet
from merkez.semalar.kurulum import KurulumGirisi
from merkez.semalar.smtp import SmtpAyarlariGirisi
from ._yardimci import _alan


def kullanici_adimini_olustur(stepper, smtp_verisi: dict) -> None:
    with ui.step("Firma ve Sistem Yöneticisi"):
        with ui.row().classes("w-full gap-2"):
            fk    = _alan("Firma Kodu *", "FIRMA01")
            fa    = _alan("Firma Adı *",  "Örnek A.Ş.")
        ui.separator().classes("q-my-xs")
        sicil  = _alan("Sicil No *",  "10001")
        with ui.row().classes("w-full gap-2"):
            ad    = _alan("Ad *")
            soyad = _alan("Soyad *")
        email  = _alan("E-posta *",  "admin@firma.com")
        parola = _alan("Parola *",   password=True)
        hata   = ui.label("").classes("text-negative text-caption")
        yukl   = ui.spinner(size="sm").classes("hidden")

        async def tamamla():
            hata.text = ""
            if any(not str(v.value or "").strip() for v in [fk, fa, sicil, ad, soyad, email, parola]):
                hata.text = "Yıldızlı (*) tüm alanlar zorunludur."
                return
            yukl.classes(remove="hidden")
            try:
                giris = KurulumGirisi(
                    sicil=sicil.value.strip(), ad=ad.value.strip(), soyad=soyad.value.strip(),
                    email=email.value.strip(), parola=parola.value,
                    firma_kodu=fk.value.strip().upper(), firma_adi=fa.value.strip(),
                )
                await ilk_kurulumu_yap(giris)
                await smtp_ayarlarini_kaydet(SmtpAyarlariGirisi(
                    firma_kodu=giris.firma_kodu, **smtp_verisi, olusturan_sicil=giris.sicil,
                ))
                ui.notify("Kurulum tamamlandı!", type="positive")
                ui.navigate.to("/giris")
            except ValueError as e:
                hata.text = str(e)
            except Exception:
                hata.text = "Bir hata oluştu, tekrar deneyin."
            finally:
                yukl.classes(add="hidden")

        with ui.stepper_navigation():
            ui.button("Geri",             on_click=stepper.previous).props("flat")
            ui.button("Kurulumu Tamamla", on_click=tamamla).props("color=positive")