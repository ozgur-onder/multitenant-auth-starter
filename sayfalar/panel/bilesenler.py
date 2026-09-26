from contextlib import contextmanager
from datetime import datetime
from typing import Iterator
from nicegui import ui

_AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
          "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
_GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]


def tarih_bicimle(zaman: datetime | None) -> str:
    return zaman.strftime("%d.%m.%Y %H:%M") if zaman else "-"


def uzun_tarih(zaman: datetime) -> str:
    return f"{zaman.day} {_AYLAR[zaman.month - 1]} {zaman.year}, {_GUNLER[zaman.weekday()]}"


def istatistik_karti(baslik: str, deger: int | str, ikon: str, renk: str) -> None:
    with ui.card().classes("q-pa-md").props("flat bordered"):
        with ui.row().classes("items-center no-wrap gap-4"):
            ui.avatar(ikon, color=f"{renk}-1", text_color=f"{renk}-8", size="52px").props("rounded")
            with ui.column().classes("gap-0"):
                ui.label(str(deger)).classes("text-h5 text-weight-bold text-grey-9")
                ui.label(baslik).classes("text-body2 text-grey-7")


@contextmanager
def bolum_karti(baslik: str, ikon: str, aciklama: str = "") -> Iterator[ui.column]:
    with ui.card().classes("w-full q-pa-none").props("flat bordered"):
        with ui.row().classes("w-full items-center no-wrap q-px-md q-py-sm gap-2"):
            ui.icon(ikon, color="primary", size="sm")
            with ui.column().classes("gap-0"):
                ui.label(baslik).classes("text-subtitle1 text-weight-medium")
                if aciklama:
                    ui.label(aciklama).classes("text-caption text-grey-6")
        ui.separator()
        with ui.column().classes("w-full q-pa-md gap-3") as icerik:
            yield icerik


def veri_tablosu(
    sutunlar: list[tuple[str, str]],
    satirlar: list[dict],
    satir_anahtari: str,
    *,
    arama: bool = True,
    sayfa_basi: int = 10,
) -> ui.table:
    kolonlar = [{"name": ad, "label": etiket, "field": ad, "align": "left", "sortable": True} for ad, etiket in sutunlar]
    ara: ui.input | None = None
    if arama:
        ara = ui.input(placeholder="Tabloda ara...").props("dense outlined clearable").classes("w-72")
        with ara.add_slot("prepend"):
            ui.icon("search", size="xs")
    tablo = ui.table(columns=kolonlar, rows=satirlar, row_key=satir_anahtari, pagination=sayfa_basi) \
        .props("flat bordered wrap-cells no-data-label='Kayıt bulunamadı' "
               "no-results-label='Aramaya uyan kayıt bulunamadı' rows-per-page-label='Sayfa başı' "
               ":pagination-label='(ilk, son, toplam) => `${ilk}-${son} / ${toplam}`'") \
        .classes("w-full")
    if ara is not None:
        ara.bind_value(tablo, "filter")
    return tablo


def rozet_sutunu(tablo: ui.table, sutun: str, renk_alani: str) -> None:
    """Sütundaki değeri satırdaki `renk_alani` renginde bir rozet olarak gösterir."""
    tablo.add_slot(
        f"body-cell-{sutun}",
        f'<q-td :props="props"><q-badge rounded :color="props.row.{renk_alani}" :label="props.value" /></q-td>',
    )


def onay_sutunu(tablo: ui.table, sutun: str) -> None:
    """Mantıksal (True/False) değeri onay ikonu olarak gösterir."""
    tablo.add_slot(
        f"body-cell-{sutun}",
        '<q-td :props="props" class="text-center">'
        '<q-icon size="sm" :name="props.value ? \'check_circle\' : \'radio_button_unchecked\'"'
        ' :color="props.value ? \'positive\' : \'grey-4\'" /></q-td>',
    )