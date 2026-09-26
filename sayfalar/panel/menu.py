from dataclasses import dataclass
from typing import Awaitable, Callable
from .baglam import PanelBaglami
from .icerikler.anasayfa import anasayfa_olustur
from .icerikler.sistem_yonetimi import sistem_yonetimi_olustur
from .icerikler.kullanici_yonetimi import kullanici_yonetimi_olustur
from .icerikler.profilim import profilim_olustur


@dataclass(frozen=True)
class MenuOgesi:
    anahtar: str
    baslik: str
    ikon: str
    yetki_kodu: str
    olustur: Callable[[PanelBaglami], Awaitable[None]]
    kapatilabilir: bool = True


# Yetki kodları psql/yetkiler/kurulum_insert.sql içindeki "SAYFA YÖNETİMİ" yetkileridir.
MENU_OGELERI: list[MenuOgesi] = [
    MenuOgesi("anasayfa", "Anasayfa", "space_dashboard", "sayfa_anasayfa", anasayfa_olustur, kapatilabilir=False),
    MenuOgesi("sistem", "Sistem Yönetimi", "settings", "sayfa_sistem", sistem_yonetimi_olustur),
    MenuOgesi("kullanici", "Kullanıcı Yönetimi", "group", "sayfa_kullanici", kullanici_yonetimi_olustur),
    MenuOgesi("profil", "Profilim", "account_circle", "sayfa_profil", profilim_olustur),
]


def izinli_menu_ogeleri(yetkiler: set[str]) -> list[MenuOgesi]:
    return [oge for oge in MENU_OGELERI if oge.yetki_kodu in yetkiler]