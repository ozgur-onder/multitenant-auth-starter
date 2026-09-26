from nicegui import ui


def _alan(label: str, placeholder: str = "", password: bool = False, genislik: str = "w-full") -> ui.input:
    inp = ui.input(label, placeholder=f"Örn: {placeholder}" if placeholder else "").classes(genislik)
    inp.props("dense")
    if password:
        inp.props("type=password")
    return inp


def _sayi_alani(label: str, placeholder: str = "", basamak: int = 10, genislik: str = "w-full") -> ui.input:
    # type=number yerine metin alanı + rakam maskesi: tarayıcının yukarı/aşağı okları çıkmaz.
    inp = ui.input(label, placeholder=f"Örn: {placeholder}" if placeholder else "").classes(genislik)
    inp.props(f'dense mask="{"#" * basamak}" inputmode=numeric')
    return inp


def _metin(alan: ui.input) -> str:
    return (alan.value or "").strip()


def _aciklama(metin: str) -> None:
    with ui.row().classes("items-start gap-2 q-pa-xs q-mb-xs bg-blue-1 rounded-borders w-full flex-nowrap"):
        ui.icon("info", color="primary").classes("text-base")
        ui.label(metin).classes("text-caption text-grey-8")