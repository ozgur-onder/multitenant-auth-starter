from nicegui import ui, app as nicegui_app
from merkez.servisler.panel import oturum_kullanicisini_getir
from merkez.servisler.yetki import kullanicinin_yetki_kodlari
from .baglam import PanelBaglami
from .menu import izinli_menu_ogeleri
from .sekme_yoneticisi import SekmeYoneticisi
from .sol_menu import sol_menu_olustur
from .ust_bar import ust_bar_olustur


@ui.page("/panel")
async def panel_sayfasi():
    token = nicegui_app.storage.user.get("oturum_token")
    kullanici = await oturum_kullanicisini_getir(token) if token else None
    if not token or not kullanici:
        ui.navigate.to("/giris")
        return

    baglam = PanelBaglami(kullanici=kullanici, yetkiler=await kullanicinin_yetki_kodlari(kullanici.sicil))
    ogeler = izinli_menu_ogeleri(baglam.yetkiler)

    ui.query("body").classes("bg-grey-1")
    yonetici = SekmeYoneticisi(baglam, token)
    cekmece = sol_menu_olustur(baglam, ogeler, yonetici)
    ust_bar_olustur(baglam, ogeler, yonetici, cekmece)

    with ui.column().classes("w-full q-pa-md"):
        yonetici.panel_alani_olustur()
        if not ogeler:
            ui.label("Hesabınıza tanımlı bir sayfa yetkisi bulunmuyor. Sistem yöneticinizle görüşün.") \
                .classes("text-grey-7")
            return
    await yonetici.ac(ogeler[0])