from nicegui import ui, app as nicegui_app
from merkez.semalar.giris import GirisGirisi
from merkez.servisler import giris as servis_giris
from sayfalar.ortak.bilesenler import alan_degeri, MesajKutusu
from sayfalar.ortak.istemci import istemci_bilgisi


def giris_yap_butonu(mesaj: MesajKutusu, *, kimlik: ui.input, parola: ui.input) -> None:
    async def tikla() -> None:
        mesaj.temizle()
        if not alan_degeri(kimlik) or not parola.value:
            mesaj.hata("Sicil / e-posta ve parola boş olamaz.")
            return

        istemci = istemci_bilgisi()
        buton.props("loading")
        try:
            sonuc = await servis_giris.giris_yap(
                GirisGirisi(sicil_veya_eposta=alan_degeri(kimlik), parola=parola.value),
                ip=istemci.ip,
                tarayici=istemci.tarayici,
            )
        except ValueError as e:
            mesaj.hata(str(e))
            return
        except Exception:
            mesaj.hata("Giriş sırasında bir hata oluştu, tekrar deneyin.")
            return
        finally:
            buton.props(remove="loading")

        nicegui_app.storage.user["oturum_token"] = sonuc.token
        ui.navigate.to("/panel")

    buton = ui.button("Giriş Yap", icon="login", on_click=tikla) \
        .props("unelevated no-caps color=primary").classes("w-full")
    kimlik.on("keydown.enter", tikla)
    parola.on("keydown.enter", tikla)