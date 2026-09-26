from functools import partial
from nicegui import ui
from merkez.sabitler import UYGULAMA_ADI
from .baglam import PanelBaglami
from .menu import MenuOgesi
from .sekme_yoneticisi import SekmeYoneticisi
from .butonlar.cikis_yap import cikis_yap_ogesi


def _kullanici_menusu(baglam: PanelBaglami, profil: MenuOgesi | None, yonetici: SekmeYoneticisi) -> None:
    k = baglam.kullanici
    with ui.button().props("flat no-caps color=grey-9").classes("q-px-sm"):
        with ui.row().classes("items-center no-wrap gap-2"):
            with ui.avatar(color="primary", text_color="white", size="34px", font_size="14px"):
                ui.label(k.bas_harfler).classes("text-weight-medium")
            with ui.column().classes("gap-0 items-start gt-xs"):
                ui.label(k.ad_soyad).classes("text-body2 text-weight-medium")
                ui.label(k.rol_adi).classes("text-caption text-grey-6")
            ui.icon("expand_more", color="grey-6")
        with ui.menu().props("anchor='bottom right' self='top right'").classes("q-mt-xs"):
            with ui.list().classes("q-py-sm"):
                with ui.item():
                    with ui.item_section():
                        ui.item_label(k.ad_soyad).classes("text-weight-medium")
                        ui.item_label(f"{k.sicil} · {k.email}").props("caption")
                ui.separator()
                if profil:
                    with ui.item(on_click=partial(yonetici.ac, profil)).props("clickable v-close-popup"):
                        with ui.item_section().props("avatar"):
                            ui.icon(profil.ikon, color="grey-7")
                        with ui.item_section():
                            ui.item_label(profil.baslik)
                cikis_yap_ogesi()


def ust_bar_olustur(
    baglam: PanelBaglami,
    ogeler: list[MenuOgesi],
    yonetici: SekmeYoneticisi,
    cekmece: ui.left_drawer,
) -> None:
    profil = next((oge for oge in ogeler if oge.anahtar == "profil"), None)
    with ui.header(elevated=False).classes("bg-white text-grey-9 column q-pa-none").props("bordered"):
        with ui.row().classes("w-full items-center no-wrap q-px-md q-py-xs gap-2"):
            ui.button(icon="menu", on_click=cekmece.toggle).props("flat round dense color=grey-8")
            ui.icon("insights", color="primary", size="md")
            ui.label(UYGULAMA_ADI).classes("text-h6 text-weight-medium")
            ui.space()
            _kullanici_menusu(baglam, profil, yonetici)
        ui.separator()
        with ui.row().classes("w-full q-px-sm"):
            yonetici.sekme_cubugu_olustur()