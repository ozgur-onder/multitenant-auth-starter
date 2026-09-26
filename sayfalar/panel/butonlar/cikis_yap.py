from nicegui import ui, app as nicegui_app
from merkez.servisler import giris as servis_giris


def cikis_yap_ogesi() -> None:
    async def tikla() -> None:
        token = nicegui_app.storage.user.pop("oturum_token", None)
        if token:
            await servis_giris.cikis_yap(token)
        ui.navigate.to("/giris")

    with ui.item(on_click=tikla).props("clickable v-close-popup").classes("text-negative"):
        with ui.item_section().props("avatar"):
            ui.icon("logout", color="negative")
        with ui.item_section():
            ui.item_label("Çıkış Yap")