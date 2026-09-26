from nicegui import ui
from merkez.servisler.panel import firma_listesi, rol_listesi, yetki_matrisi
from ..baglam import PanelBaglami
from ..bilesenler import bolum_karti, onay_sutunu, rozet_sutunu, tarih_bicimle, veri_tablosu


def _durum(aktif: bool) -> dict:
    return {"durum": "Aktif" if aktif else "Pasif", "renk": "positive" if aktif else "grey-6"}


async def _firma_karti() -> None:
    with bolum_karti("Firma Yönetimi", "business", "Sistemde tanımlı firmalar"):
        satirlar = [
            {"firma_kodu": f["firma_kodu"], "firma_adi": f["firma_adi"],
             "zaman": tarih_bicimle(f["olusturma_guncelleme_zamani"]), **_durum(f["durum"])}
            for f in await firma_listesi()
        ]
        tablo = veri_tablosu(
            [("firma_kodu", "Firma Kodu"), ("firma_adi", "Firma Adı"), ("durum", "Durum"), ("zaman", "Son Güncelleme")],
            satirlar, "firma_kodu",
        )
        rozet_sutunu(tablo, "durum", "renk")


async def _rol_karti() -> None:
    with bolum_karti("Rol Yönetimi", "admin_panel_settings", "Roller ve kapsadıkları yetki / kullanıcı sayıları"):
        satirlar = [
            {"rol_kodu": r["rol_kodu"], "rol_adi": r["rol_adi"], "yetki_sayisi": r["yetki_sayisi"],
             "kullanici_sayisi": r["kullanici_sayisi"], **_durum(r["durum"])}
            for r in await rol_listesi()
        ]
        tablo = veri_tablosu(
            [("rol_kodu", "Rol Kodu"), ("rol_adi", "Rol Adı"), ("yetki_sayisi", "Yetki Sayısı"),
             ("kullanici_sayisi", "Kullanıcı Sayısı"), ("durum", "Durum")],
            satirlar, "rol_kodu",
        )
        rozet_sutunu(tablo, "durum", "renk")


async def _yetki_matrisi_karti() -> None:
    roller, satirlar = await yetki_matrisi()
    with bolum_karti("Rol & Yetki Matrisi", "grid_on", "Hangi rolün hangi yetkiye sahip olduğu"):
        sutunlar = [("modul", "Modül"), ("yetki_adi", "Yetki")] + [(f"rol_{r['rol_kodu']}", r["rol_adi"]) for r in roller]
        tablo = veri_tablosu(sutunlar, satirlar, "yetki_kodu", sayfa_basi=20)
        for r in roller:
            onay_sutunu(tablo, f"rol_{r['rol_kodu']}")


async def sistem_yonetimi_olustur(baglam: PanelBaglami) -> None:
    kartlar = [
        ("kart_firma", _firma_karti),
        ("kart_rol", _rol_karti),
        ("kart_yetki_matrisi", _yetki_matrisi_karti),
    ]
    izinli = [olustur for yetki, olustur in kartlar if yetki in baglam.yetkiler]
    if not izinli:
        ui.label("Bu bölümde görüntüleme yetkiniz olan bir kart bulunmuyor.").classes("text-grey-7")
        return
    for olustur in izinli:
        await olustur()