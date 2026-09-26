from nicegui import ui
from merkez.istemci import IstemciBilgisi, istemci_bilgisi_olustur


def istemci_bilgisi() -> IstemciBilgisi:
    """Sayfayı açan isteğin IP adresini ve tarayıcı bilgisini (User-Agent) verir.

    IP, uvicorn tarafından belirlenir: istek güvenilir bir vekil sunucudan (FORWARDED_ALLOW_IPS)
    geliyorsa X-Forwarded-For başlığındaki gerçek istemci IP'si, gelmiyorsa bağlantının IP'si kullanılır.
    """
    istek = ui.context.client.request
    return istemci_bilgisi_olustur(
        istek.client.host if istek.client else None,
        istek.headers.get("user-agent"),
    )