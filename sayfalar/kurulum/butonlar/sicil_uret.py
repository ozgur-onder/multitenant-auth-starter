from nicegui import ui
from merkez.servisler.sicil import sicil_uret


def sicil_uret_butonu(sicil_alani: ui.input, hata: ui.label) -> None:
    async def tikla() -> None:
        hata.text = ""
        buton.props("loading")
        try:
            sicil_alani.value = await sicil_uret()
        except ValueError as e:
            hata.text = str(e)
        finally:
            buton.props(remove="loading")

    with sicil_alani.add_slot("append"):
        buton = ui.button("Üret", icon="autorenew", on_click=tikla).props("flat dense no-caps size=sm color=primary")
        buton.tooltip("Sicil No Üret")