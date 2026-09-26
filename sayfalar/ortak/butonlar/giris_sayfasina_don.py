from nicegui import ui


def giris_sayfasina_don_butonu() -> None:
    ui.button("Giriş sayfasına dön", icon="arrow_back", on_click=lambda: ui.navigate.to("/giris")) \
        .props("flat no-caps color=primary").classes("self-center")