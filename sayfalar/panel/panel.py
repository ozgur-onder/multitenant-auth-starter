from nicegui import ui, app as nicegui_app
from merkez.servisler import giris as servis_giris


@ui.page("/panel")
async def panel_sayfasi():
    token = nicegui_app.storage.user.get("oturum_token")
    if not token or not await servis_giris.oturum_kontrol(token):
        ui.navigate.to("/giris")
        return

    try:
        from merkez.veritabani import vt_getir
        havuz = await vt_getir()
        async with havuz.acquire() as db:
            kayit = await db.fetchrow(
                "SELECT sicil FROM kullanici_oturumlari WHERE oturum_token = $1;", token
            )
            if kayit:
                await db.execute(
                    """INSERT INTO sayfa_ziyaret_loglari (sicil, sayfa, sayfa_basligi, oturum_token)
                       VALUES ($1, '/panel', 'Panel', $2);""",
                    kayit["sicil"], token,
                )
    except Exception:
        pass

    async def cikis_yap():
        t = nicegui_app.storage.user.pop("oturum_token", None)
        if t:
            await servis_giris.cikis_yap(t)
        ui.navigate.to("/giris")

    with ui.column().classes("w-full"):
        with ui.row().classes("w-full items-center justify-between q-pa-md bg-primary text-white"):
            ui.label("İş Zekası Platformu").classes("text-h6")
            ui.button("Çıkış Yap", on_click=cikis_yap).props("flat color=white")

        with ui.column().classes("q-pa-md w-full"):
            ui.label("Hoş Geldiniz").classes("text-h5 q-mb-md")
            with ui.row().classes("w-full gap-4 flex-wrap"):
                for baslik, ikon in [
                    ("Kullanıcılar", "people"),
                    ("Firmalar", "business"),
                    ("Roller", "admin_panel_settings"),
                    ("Yetkiler", "lock"),
                ]:
                    with ui.card().classes("flex-1 min-w-36"):
                        with ui.row().classes("items-center gap-2"):
                            ui.icon(ikon).classes("text-primary text-2xl")
                            ui.label(baslik).classes("text-subtitle1")