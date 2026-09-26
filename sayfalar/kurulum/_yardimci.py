from nicegui import ui


def _alan(label: str, placeholder: str = "", password: bool = False):
    inp = ui.input(label, placeholder=placeholder).classes("w-full")
    if password:
        inp.props("type=password")
    return inp