import ipaddress
import re
from dataclasses import dataclass

_TARAYICI_AZAMI_UZUNLUK = 500


@dataclass(frozen=True)
class IstemciBilgisi:
    ip: str | None
    tarayici: str | None


def istemci_bilgisi_olustur(ip: str | None, tarayici: str | None) -> IstemciBilgisi:
    """Veritabanına yazılmadan önce doğrular; geçersiz IP 'inet' sütununda hata vereceği için None olur."""
    try:
        adres = ipaddress.ip_address((ip or "").strip()) if ip else None
    except ValueError:
        adres = None
    # IPv6 açık sunucularda IPv4 istemciler "::ffff:1.2.3.4" biçiminde gelir; düz IPv4 olarak saklanır.
    if isinstance(adres, ipaddress.IPv6Address) and adres.ipv4_mapped:
        adres = adres.ipv4_mapped
    gecerli_ip = str(adres) if adres else None
    temiz_tarayici = (tarayici or "").strip()[:_TARAYICI_AZAMI_UZUNLUK] or None
    return IstemciBilgisi(ip=gecerli_ip, tarayici=temiz_tarayici)


_TARAYICILAR = [
    (r"Edg(?:e|A|iOS)?/(\d+)", "Edge"),
    (r"OPR/(\d+)", "Opera"),
    (r"YaBrowser/(\d+)", "Yandex"),
    (r"Firefox/(\d+)", "Firefox"),
    (r"(?:Headless)?Chrome/(\d+)", "Chrome"),
    (r"Version/(\d+).*Safari", "Safari"),
]
_ISLETIM_SISTEMLERI = [
    ("Windows", "Windows"), ("Android", "Android"), ("iPhone", "iOS"), ("iPad", "iPadOS"),
    ("Mac OS X", "macOS"), ("CrOS", "ChromeOS"), ("Linux", "Linux"),
]


def tarayici_ozeti(tarayici: str | None) -> str:
    """Ham User-Agent metnini ekranda okunabilir kısa hale getirir, örn. 'Chrome 140 · Linux'."""
    if not tarayici:
        return "-"
    ad = next((f"{isim} {m.group(1)}" for desen, isim in _TARAYICILAR if (m := re.search(desen, tarayici))), "Bilinmiyor")
    sistem = next((isim for anahtar, isim in _ISLETIM_SISTEMLERI if anahtar in tarayici), "")
    return f"{ad} · {sistem}" if sistem else ad