from nicegui import ui
from merkez.parola_kurallari import PAROLA_KURALLARI


def parola_kurallarini_goster(parola_alani: ui.input) -> None:
    gostergeler: list[tuple[ui.icon, ui.label]] = []
    with ui.row().classes("w-full gap-x-3 gap-y-0"):
        for ad, _ in PAROLA_KURALLARI:
            with ui.row().classes("items-center gap-1 no-wrap"):
                ikon  = ui.icon("radio_button_unchecked", color="grey-5", size="xs")
                yazi  = ui.label(ad).classes("text-caption text-grey-7")
            gostergeler.append((ikon, yazi))

    def guncelle() -> None:
        parola = parola_alani.value or ""
        for (_, kontrol), (ikon, yazi) in zip(PAROLA_KURALLARI, gostergeler):
            saglandi = kontrol(parola)
            ikon.name = "check_circle" if saglandi else "radio_button_unchecked"
            ikon.props(f"color={'positive' if saglandi else 'grey-5'}")
            yazi.classes(replace=f"text-caption {'text-positive' if saglandi else 'text-grey-7'}")

    parola_alani.on_value_change(guncelle)