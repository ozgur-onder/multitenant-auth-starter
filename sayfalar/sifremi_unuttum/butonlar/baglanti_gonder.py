from nicegui import ui
from merkez.servisler.sifre import SIFIRLAMA_GECERLILIK_DAKIKA, sifirlama_baglantisi_gonder
from sayfalar.ortak.bilesenler import alan_degeri, MesajKutusu
from sayfalar.ortak.istemci import istemci_bilgisi
from sayfalar.ortak.kimlik_iskeleti import sonuc_ekrani
from sayfalar.ortak.butonlar.giris_sayfasina_don import giris_sayfasina_don_butonu


def baglanti_gonder_butonu(icerik: ui.column, mesaj: MesajKutusu, *, sicil: ui.input, email: ui.input) -> None:
    async def tikla() -> None:
        mesaj.temizle()
        if not alan_degeri(sicil) or not alan_degeri(email):
            mesaj.hata("Sicil numarası ve e-posta adresi boş olamaz.")
            return

        adres = alan_degeri(email)
        buton.props("loading")
        try:
            await sifirlama_baglantisi_gonder(alan_degeri(sicil), adres, ip=istemci_bilgisi().ip)
        except ValueError as e:
            mesaj.hata(str(e))
            return
        except Exception:
            mesaj.hata("Bir hata oluştu, tekrar deneyin.")
            return
        finally:
            buton.props(remove="loading")

        sonuc_ekrani(
            icerik, "mark_email_read", "positive", "Bağlantı gönderildi",
            f"Şifre sıfırlama bağlantısı {adres} adresine gönderildi. "
            f"Bağlantı {SIFIRLAMA_GECERLILIK_DAKIKA} dakika geçerlidir.",
        )
        with icerik:
            giris_sayfasina_don_butonu()

    buton = ui.button("Sıfırlama Bağlantısı Gönder", icon="send", on_click=tikla) \
        .props("unelevated no-caps color=primary").classes("w-full")
    sicil.on("keydown.enter", tikla)
    email.on("keydown.enter", tikla)