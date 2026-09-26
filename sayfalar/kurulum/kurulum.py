from nicegui import ui
from merkez.servisler.kurulum import kurulum_yapilmis_mi, varsayilan_firmayi_getir
from .adim_smtp import smtp_adimini_olustur
from .adim_kullanici import kullanici_adimini_olustur


@ui.page("/kurulum")
async def kurulum_sayfasi():
    if await kurulum_yapilmis_mi():
        ui.navigate.to("/giris")
        return

    firma = await varsayilan_firmayi_getir()
    smtp_verisi: dict = {}

    with ui.column().classes("items-center justify-center min-h-screen w-full"):
        with ui.card().classes("w-full max-w-xl q-pa-md"):
            ui.label("Sistem Kurulumu").classes("text-2xl font-bold text-center")
            ui.separator()
            if not firma:
                ui.label(
                    "Sistemde kayıtlı firma bulunamadı. Veritabanı kurulumunu kontrol edin."
                ).classes("text-negative")
                return
            with ui.stepper().classes("w-full") as stepper:
                smtp_adimini_olustur(stepper, smtp_verisi)
                kullanici_adimini_olustur(stepper, smtp_verisi, firma["firma_adi"])