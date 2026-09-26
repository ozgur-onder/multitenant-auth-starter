from nicegui import ui


def sifremi_unuttum_butonu() -> None:
    ui.button("Şifremi unuttum", icon="help_outline", on_click=lambda: ui.navigate.to("/sifremi-unuttum")) \
        .props("flat no-caps color=primary").classes("self-center")