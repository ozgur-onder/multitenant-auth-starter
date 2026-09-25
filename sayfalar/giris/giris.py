from nicegui import ui, app as nicegui_app


@ui.page("/giris")
async def giris_sayfasi():
    # Zaten oturum açıksa panele yönlendir
    token = nicegui_app.storage.user.get("oturum_token")
    if token:
        from merkez.servisler import giris as servis_giris
        if await servis_giris.oturum_kontrol(token):
            ui.navigate.to("/panel")
            return

    # ── Sayfa düzeni ────────────────────────────────────────────────────────
    with ui.column().classes("w-full min-h-screen items-center justify-center bg-gray-50"):
        with ui.card().classes("w-96 shadow-lg"):
            with ui.column().classes("w-full gap-5 p-8"):

                # Başlık
                ui.label("Giriş Yap").classes("text-3xl font-bold text-center text-gray-800")
                ui.separator()

                # Form alanları
                sicil_input = ui.input(
                    label="Sicil Numarası",
                    placeholder="Sicil numaranızı giriniz",
                ).props("outlined dense").classes("w-full")

                parola_input = ui.input(
                    label="Şifre",
                    placeholder="Şifrenizi giriniz",
                    password=True,
                    password_toggle_button=True,
                ).props("outlined dense").classes("w-full")

                hata_etiketi = ui.label("").classes("text-red-500 text-sm min-h-4")

                # ── Giriş işlemi ─────────────────────────────────────────────
                async def giris_islemi():
                    hata_etiketi.set_text("")
                    if not sicil_input.value.strip() or not parola_input.value:
                        hata_etiketi.set_text("Sicil numarası ve şifre zorunludur.")
                        return

                    from merkez.servisler import giris as servis_giris

                    sonuc = await servis_giris.giris_yap(
                        sicil=sicil_input.value.strip(),
                        parola=parola_input.value,
                    )

                    if sonuc:
                        nicegui_app.storage.user["oturum_token"] = sonuc["token"]
                        nicegui_app.storage.user["sicil"] = sonuc["sicil"]
                        nicegui_app.storage.user["ad"] = sonuc["ad"]
                        nicegui_app.storage.user["soyad"] = sonuc["soyad"]
                        ui.navigate.to("/panel")
                    else:
                        hata_etiketi.set_text("Sicil numarası veya şifre hatalı.")
                        parola_input.set_value("")

                ui.button(
                    "Giriş Yap",
                    on_click=giris_islemi,
                ).props("color=primary unelevated").classes("w-full")

                # Enter tuşuyla da gönderilebilsin
                parola_input.on("keydown.enter", giris_islemi)
                sicil_input.on("keydown.enter", lambda: parola_input.run_method("focus"))

                ui.separator()

                with ui.row().classes("w-full justify-center"):
                    ui.link("Şifremi Unuttum", "/sifremi-unuttum").classes("text-sm text-blue-600")
