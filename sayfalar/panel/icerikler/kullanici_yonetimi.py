from merkez.servisler.panel import kullanici_listesi
from ..baglam import PanelBaglami
from ..bilesenler import bolum_karti, rozet_sutunu, tarih_bicimle, veri_tablosu


async def kullanici_yonetimi_olustur(baglam: PanelBaglami) -> None:
    with bolum_karti("Kullanıcılar", "group", "Sistemdeki tüm kullanıcılar, firmaları ve rolleri"):
        satirlar = [
            {
                "sicil": k["sicil"],
                "ad_soyad": k["ad_soyad"],
                "email": k["email"],
                "firmalar": k["firmalar"],
                "roller": k["roller"],
                "durum": "Aktif" if k["durum"] else "Pasif",
                "renk": "positive" if k["durum"] else "grey-6",
                "olusturma": tarih_bicimle(k["olusturma_zamani"]),
            }
            for k in await kullanici_listesi()
        ]
        tablo = veri_tablosu(
            [("sicil", "Sicil"), ("ad_soyad", "Ad Soyad"), ("email", "E-posta"), ("firmalar", "Firma"),
             ("roller", "Rol"), ("durum", "Durum"), ("olusturma", "Oluşturma")],
            satirlar, "sicil",
        )
        rozet_sutunu(tablo, "durum", "renk")