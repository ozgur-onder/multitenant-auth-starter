from nicegui import ui
from merkez.servisler.kurulum import ilk_kurulumu_yap
from merkez.servisler.smtp import smtp_ayarlarini_kaydet
from merkez.semalar.kurulum import KurulumGirisi
from merkez.semalar.smtp import SmtpAyarlariGirisi
from ._yardimci import _alan, _metin, _aciklama


def kullanici_adimini_olustur(stepper, smtp_verisi: dict) -> None:
    with ui.step("Firma ve Sistem Yöneticisi"):
        _aciklama(
            "Firmanızı ve sisteme ilk giriş yapacak yönetici hesabını oluşturun. "
            "Bu kullanıcı, en yüksek yetkiye sahip Sistem Yöneticisi rolüyle oluşturulur."
        )
        with ui.row().classes("w-full gap-2 flex-nowrap"):
            fk = _alan("Firma Kodu *", "FIRMA01",         genislik="w-32")
            fa = _alan("Firma Adı *",  "ABC Holding A.Ş.", genislik="flex-1")
        with ui.row().classes("w-full gap-2 flex-nowrap"):
            sicil = _alan("Sicil No *", "10001",           genislik="w-32")
            email = _alan("E-posta *",  "admin@firma.com", genislik="flex-1")
        with ui.row().classes("w-full gap-2 flex-nowrap"):
            ad     = _alan("Ad *",     genislik="flex-1")
            soyad  = _alan("Soyad *",  genislik="flex-1")
            parola = _alan("Parola *", password=True, genislik="flex-1")
        hata = ui.label("").classes("text-negative text-caption")
        yukl = ui.spinner(size="sm").classes("hidden")

        async def tamamla():
            hata.text = ""
            if any(not _metin(v) for v in [fk, fa, sicil, ad, soyad, email, parola]):
                hata.text = "Yıldızlı (*) tüm alanlar zorunludur."
                return
            yukl.classes(remove="hidden")
            try:
                giris = KurulumGirisi(
                    sicil=_metin(sicil), ad=_metin(ad), soyad=_metin(soyad),
                    email=_metin(email), parola=parola.value or "",
                    firma_kodu=_metin(fk).upper(), firma_adi=_metin(fa),
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