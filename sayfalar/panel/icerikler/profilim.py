from nicegui import ui
from merkez.istemci import tarayici_ozeti
from merkez.servisler.panel import kullanicinin_oturumlari
from ..baglam import PanelBaglami
from ..bilesenler import bolum_karti, rozet_sutunu, tarih_bicimle, veri_tablosu


def _bilgi_satiri(ikon: str, etiket: str, deger: str) -> None:
    with ui.item().classes("q-px-none"):
        with ui.item_section().props("avatar"):
            ui.icon(ikon, color="grey-6")
        with ui.item_section():
            ui.item_label(etiket).props("caption")
            ui.item_label(deger)


async def profilim_olustur(baglam: PanelBaglami) -> None:
    k = baglam.kullanici
    with ui.row().classes("w-full gap-4 items-start"):
        with ui.card().classes("q-pa-lg items-center").props("flat bordered"):
            with ui.avatar(color="primary", text_color="white", size="88px", font_size="32px"):
                ui.label(k.bas_harfler).classes("text-weight-medium")
            ui.label(k.ad_soyad).classes("text-h6 text-weight-bold q-mt-sm")
            ui.chip(k.rol_adi, icon="verified_user", color="blue-1", text_color="primary").props("dense")
            with ui.list().classes("w-full q-mt-sm"):
                _bilgi_satiri("badge", "Sicil No", k.sicil)
                _bilgi_satiri("mail", "E-posta", k.email)
                _bilgi_satiri("business", "Firma", k.firma_adi)

        with ui.column().classes("col gap-4"):
            with bolum_karti("Son Oturumlarım", "devices", "Hesabınızla açılan son 10 oturum"):
                satirlar = [
                    {
                        "no": i,
                        "giris": tarih_bicimle(o["giris_zamani"]),
                        "cikis": tarih_bicimle(o["cikis_zamani"]),
                        "durum": "Açık" if o["durum"] == "aktif" else "Kapalı",
                        "renk": "positive" if o["durum"] == "aktif" else "grey-6",
                        "ip": o["ip_adresi"] or "-",
                        "tarayici": tarayici_ozeti(o["tarayici"]),
                    }
                    for i, o in enumerate(await kullanicinin_oturumlari(k.sicil))
                ]
                tablo = veri_tablosu(
                    [("giris", "Giriş"), ("cikis", "Çıkış"), ("durum", "Durum"), ("ip", "IP Adresi"), ("tarayici", "Tarayıcı")],
                    satirlar, "no", arama=False,
                )
                rozet_sutunu(tablo, "durum", "renk")