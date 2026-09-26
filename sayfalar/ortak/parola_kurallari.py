from typing import Callable
from nicegui import ui
from merkez.parola_kurallari import PAROLA_KURALLARI


def parola_kurallarini_goster(parola_alani: ui.input, tekrar_alani: ui.input) -> None:
    kontroller: list[tuple[str, Callable[[str, str], bool]]] = [
        (ad, lambda p, _t, k=kontrol: k(p)) for ad, kontrol in PAROLA_KURALLARI
    ]
    kontroller.append(("Parolalar eşleşiyor", lambda p, t: bool(p) and p == t))

    gostergeler: list[tuple[ui.icon, ui.label]] = []
    with ui.row().classes("w-full gap-x-3 gap-y-0"):
        for ad, _ in kontroller:
            with ui.row().classes("items-center gap-1 no-wrap"):
                ikon = ui.icon("radio_button_unchecked", color="grey-5", size="xs")
                yazi = ui.label(ad).classes("text-caption text-grey-7")
            gostergeler.append((ikon, yazi))

    def guncelle() -> None:
        parola = parola_alani.value or ""
        tekrar = tekrar_alani.value or ""
        for (_, kontrol), (ikon, yazi) in zip(kontroller, gostergeler):
            saglandi = kontrol(parola, tekrar)
            ikon.name = "check_circle" if saglandi else "radio_button_unchecked"
            ikon.props(f"color={'positive' if saglandi else 'grey-5'}")
            yazi.classes(replace=f"text-caption {'text-positive' if saglandi else 'text-grey-7'}")

    parola_alani.on_value_change(guncelle)
    tekrar_alani.on_value_change(guncelle)