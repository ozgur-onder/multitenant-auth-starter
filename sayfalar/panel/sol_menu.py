from functools import partial
from nicegui import ui
from .baglam import PanelBaglami
from .menu import MenuOgesi
from .sekme_yoneticisi import SekmeYoneticisi


def sol_menu_olustur(baglam: PanelBaglami, ogeler: list[MenuOgesi], yonetici: SekmeYoneticisi) -> ui.left_drawer:
    with ui.left_drawer(value=True, bordered=True).props("width=250 breakpoint=900").classes("bg-white column no-wrap") as cekmece:
        ui.label("MENÜ").classes("text-caption text-weight-medium text-grey-6 q-px-md q-pt-md q-pb-xs")
        menu_ogeleri: dict[str, ui.item] = {}
        with ui.list().props("padding").classes("w-full q-px-sm"):
            for oge in ogeler:
                with ui.item(on_click=partial(yonetici.ac, oge)) \
                        .props('clickable v-ripple active-class="bg-blue-1 text-primary text-weight-medium"') \
                        .classes("rounded-borders q-mb-xs") as satir:
                    with ui.item_section().props("avatar"):
                        ui.icon(oge.ikon)
                    with ui.item_section():
                        ui.item_label(oge.baslik)
                menu_ogeleri[oge.anahtar] = satir

        ui.space()
        ui.separator()
        with ui.row().classes("items-center no-wrap q-pa-md gap-3"):
            ui.icon("business", color="grey-6")
            with ui.column().classes("gap-0"):
                ui.label("Firma").classes("text-caption text-grey-6")
                ui.label(baglam.kullanici.firma_adi).classes("text-body2 text-weight-medium")

    def aktif_isaretle(anahtar: str | None) -> None:
        for oge_anahtari, satir in menu_ogeleri.items():
            satir.props(add="active") if oge_anahtari == anahtar else satir.props(remove="active")

    yonetici.degisince(aktif_isaretle)
    return cekmece