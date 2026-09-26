from nicegui import ui
from merkez.veritabani import vt_getir
from .adim_smtp import smtp_adimini_olustur
from .adim_kullanici import kullanici_adimini_olustur


async def _kurulum_yapilmis_mi() -> bool:
    try:
        havuz = await vt_getir()
        async with havuz.acquire() as db:
            sayi = await db.fetchval(
                "SELECT COUNT(*) FROM kullanici_yetkileri ky "
                "JOIN roller r ON ky.rol_id = r.id WHERE r.rol_kodu = 1"
            )
        return (sayi or 0) > 0
    except Exception:
        return False


@ui.page("/kurulum")
async def kurulum_sayfasi():
    if await _kurulum_yapilmis_mi():
        ui.navigate.to("/giris")
        return

    smtp_verisi: dict = {}

    with ui.column().classes("items-center justify-center min-h-screen w-full"):
        with ui.card().classes("w-full max-w-xl q-pa-md"):
            ui.label("Sistem Kurulumu").classes("text-2xl font-bold text-center")
            ui.separator()
            with ui.stepper().classes("w-full") as stepper:
                smtp_adimini_olustur(stepper, smtp_verisi)
                kullanici_adimini_olustur(stepper, smtp_verisi)