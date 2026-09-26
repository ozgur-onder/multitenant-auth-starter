from contextlib import contextmanager
from datetime import date
from typing import Iterator
from nicegui import ui

UYGULAMA_ADI = "İş Zekası Platformu"


@contextmanager
def kimlik_iskeleti(baslik: str, alt_baslik: str, ikon: str) -> Iterator[ui.column]:
    """Giriş, şifremi unuttum ve şifre sıfırlama sayfalarının ortak görünümü."""
    ui.query("body").classes("bg-grey-2")
    with ui.column().classes("w-full min-h-screen items-center justify-center q-pa-md gap-4"):
        with ui.row().classes("items-center gap-2"):
            ui.icon("insights", color="primary", size="md")
            ui.label(UYGULAMA_ADI).classes("text-h6 text-weight-medium text-grey-9")

        with ui.card().classes("w-full max-w-sm q-pa-lg").props("flat bordered"):
            with ui.column().classes("w-full items-center gap-1 q-mb-sm"):
                ui.avatar(ikon, color="primary", text_color="white", size="56px")
                ui.label(baslik).classes("text-h5 text-weight-bold q-mt-sm")
                ui.label(alt_baslik).classes("text-body2 text-grey-7 text-center")
            with ui.column().classes("w-full gap-3") as icerik:
                yield icerik

        ui.label(f"© {date.today().year} {UYGULAMA_ADI}").classes("text-caption text-grey-6")


def sonuc_ekrani(icerik: ui.column, ikon: str, renk: str, baslik: str, metin: str) -> None:
    """Kartın içindeki formu kaldırıp yerine işlemin sonucunu gösterir."""
    icerik.clear()
    with icerik:
        with ui.column().classes("w-full items-center gap-2 q-py-sm"):
            ui.icon(ikon, color=renk, size="xl")
            ui.label(baslik).classes("text-subtitle1 text-weight-medium text-center")
            ui.label(metin).classes("text-body2 text-grey-7 text-center")