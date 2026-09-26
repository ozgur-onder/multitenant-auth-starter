from datetime import datetime
from nicegui import ui
from merkez.istemci import tarayici_ozeti
from merkez.servisler.panel import ozet_sayilari, son_giris_hareketleri
from ..baglam import PanelBaglami
from ..bilesenler import bolum_karti, istatistik_karti, rozet_sutunu, tarih_bicimle, uzun_tarih, veri_tablosu


def _selamlama(saat: int) -> str:
    if 5 <= saat < 12:
        return "Günaydın"
    if 12 <= saat < 18:
        return "İyi günler"
    return "İyi akşamlar"


async def anasayfa_olustur(baglam: PanelBaglami) -> None:
    ozet = await ozet_sayilari()
    hareketler = await son_giris_hareketleri(10)
    simdi = datetime.now()

    with ui.column().classes("w-full gap-0"):
        ui.label(f"{_selamlama(simdi.hour)}, {baglam.kullanici.ad}").classes("text-h5 text-weight-bold text-grey-9")
        ui.label(uzun_tarih(simdi)).classes("text-body2 text-grey-7")

    with ui.grid().classes("w-full gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4"):
        istatistik_karti("Aktif Kullanıcı", ozet["kullanici"], "group", "blue")
        istatistik_karti("Firma", ozet["firma"], "business", "teal")
        istatistik_karti("Rol", ozet["rol"], "admin_panel_settings", "deep-purple")
        istatistik_karti("Açık Oturum", ozet["aktif_oturum"], "devices", "orange")

    with bolum_karti("Son Giriş Hareketleri", "history", "Sisteme yapılan son 10 giriş denemesi"):
        satirlar = [
            {
                "no": i,
                "zaman": tarih_bicimle(h["islem_zamani"]),
                "kullanici": f"{h['ad_soyad']} ({h['sicil']})",
                "durum": "Başarılı" if h["durum"] == "basarili" else "Başarısız",
                "renk": "positive" if h["durum"] == "basarili" else "negative",
                "ip": h["ip_adresi"] or "-",
                "tarayici": tarayici_ozeti(h["tarayici"]),
            }
            for i, h in enumerate(hareketler)
        ]
        tablo = veri_tablosu(
            [("zaman", "Zaman"), ("kullanici", "Kullanıcı"), ("durum", "Durum"), ("ip", "IP Adresi"), ("tarayici", "Tarayıcı")],
            satirlar, "no", arama=False,
        )
        rozet_sutunu(tablo, "durum", "renk")