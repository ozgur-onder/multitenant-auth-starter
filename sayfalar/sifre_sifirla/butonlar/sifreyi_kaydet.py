from nicegui import ui
from merkez.parola_kurallari import eksik_parola_kurallari
from merkez.servisler.sifre import sifreyi_sifirla
from sayfalar.ortak.bilesenler import MesajKutusu
from sayfalar.ortak.kimlik_iskeleti import sonuc_ekrani


def sifreyi_kaydet_butonu(
    icerik: ui.column,
    mesaj: MesajKutusu,
    token: str,
    *,
    parola: ui.input,
    parola_tekrar: ui.input,
) -> None:
    async def tikla() -> None:
        mesaj.temizle()
        yeni = parola.value or ""
        eksikler = eksik_parola_kurallari(yeni)
        if eksikler:
            mesaj.hata("Parola şu kuralları sağlamıyor: " + ", ".join(eksikler) + ".")
            return
        if yeni != parola_tekrar.value:
            mesaj.hata("Parolalar eşleşmiyor.")
            return

        buton.props("loading")
        try:
            await sifreyi_sifirla(token, yeni)
        except ValueError as e:
            mesaj.hata(str(e))
            return
        except Exception:
            mesaj.hata("Bir hata oluştu, tekrar deneyin.")
            return
        finally:
            buton.props(remove="loading")

        sonuc_ekrani(
            icerik, "verified_user", "positive", "Şifreniz güncellendi",
            "Yeni şifrenizle giriş yapabilirsiniz. Güvenliğiniz için açık olan tüm oturumlarınız kapatıldı.",
        )
        with icerik:
            ui.button("Giriş Yap", icon="login", on_click=lambda: ui.navigate.to("/giris")) \
                .props("unelevated no-caps color=primary").classes("w-full")

    buton = ui.button("Şifreyi Kaydet", icon="save", on_click=tikla) \
        .props("unelevated no-caps color=primary").classes("w-full")
    parola_tekrar.on("keydown.enter", tikla)