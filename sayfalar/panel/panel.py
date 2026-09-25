from nicegui import ui, app as nicegui_app


@ui.page("/panel")
async def panel_sayfasi():
    # Oturum kontrolü
    token = nicegui_app.storage.user.get("oturum_token")
    if not token:
        ui.navigate.to("/giris")
        return

    from merkez.servisler import giris as servis_giris
    if not await servis_giris.oturum_kontrol(token):
        nicegui_app.storage.user.clear()
        ui.navigate.to("/giris")
        return

    ad = nicegui_app.storage.user.get("ad", "")
    soyad = nicegui_app.storage.user.get("soyad", "")
    sicil = nicegui_app.storage.user.get("sicil", "")

    # ── Sayfa ziyaret logu ───────────────────────────────────────────────────
    try:
        from merkez.veritabani import vt_getir
        from datetime import datetime, timezone
        havuz = await vt_getir()
        async with havuz.acquire() as db:
            await db.execute(
                """INSERT INTO sayfa_ziyaret_loglari (sicil, sayfa, sayfa_basligi, oturum_token)
                   VALUES ($1, '/panel', 'Panel', $2)
                   ON CONFLICT DO NOTHING;""",
                sicil, token,
            )
    except Exception:
        pass

    # ── Header ──────────────────────────────────────────────────────────────
    with ui.column().classes("w-full min-h-screen bg-gray-50"):
        with ui.row().classes("w-full bg-blue-700 px-6 py-4 items-center justify-between shadow"):
            ui.label("İş Zekası Platformu").classes("text-white text-xl font-bold")

            with ui.row().classes("items-center gap-4"):
                ui.icon("person").classes("text-white")
                ui.label(f"{ad} {soyad}  ·  {sicil}").classes("text-white text-sm")

                async def cikis_islemi():
                    await servis_giris.cikis_yap(token)
                    nicegui_app.storage.user.clear()
                    ui.navigate.to("/giris")

                ui.button("Çıkış Yap", on_click=cikis_islemi) \
                    .props("flat color=white icon=logout")

        # ── İçerik ──────────────────────────────────────────────────────────
        with ui.column().classes("w-full p-8 gap-6"):
            ui.label(f"Hoş geldiniz, {ad} {soyad}!").classes("text-2xl font-bold text-gray-800")

            with ui.row().classes("w-full gap-4 flex-wrap"):
                _ozet_karti(icon="business", baslik="Firma Yönetimi", renk="blue")
                _ozet_karti(icon="manage_accounts", baslik="Kullanıcı Yönetimi", renk="green")
                _ozet_karti(icon="admin_panel_settings", baslik="Rol & Yetki Matrisi", renk="purple")
                _ozet_karti(icon="settings", baslik="Sistem Ayarları", renk="orange")


def _ozet_karti(icon: str, baslik: str, renk: str):
    with ui.card().classes("w-52 h-32 cursor-pointer hover:shadow-lg transition-shadow"):
        with ui.column().classes("w-full h-full items-center justify-center gap-2"):
            ui.icon(icon).classes(f"text-{renk}-600 text-4xl")
            ui.label(baslik).classes("text-gray-700 text-sm font-medium text-center")
