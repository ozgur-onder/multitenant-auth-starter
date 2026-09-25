from nicegui import ui


@ui.page("/sifremi-unuttum")
async def sifremi_unuttum_sayfasi():
    with ui.column().classes("w-full min-h-screen items-center justify-center bg-gray-50"):
        with ui.card().classes("w-96 shadow-lg"):
            with ui.column().classes("w-full gap-5 p-8"):

                ui.label("Şifremi Unuttum").classes("text-3xl font-bold text-center text-gray-800")
                ui.label("E-posta adresinizi girin, şifre sıfırlama bağlantısı gönderilsin.") \
                    .classes("text-center text-gray-500 text-sm")
                ui.separator()

                email_input = ui.input(
                    label="E-Posta Adresi",
                    placeholder="ornek@firma.com",
                ).props("outlined dense").classes("w-full")

                bilgi_etiketi = ui.label("").classes("text-sm min-h-4")
                hata_etiketi = ui.label("").classes("text-red-500 text-sm min-h-4")

                async def talep_olustur():
                    bilgi_etiketi.set_text("")
                    hata_etiketi.set_text("")
                    email = email_input.value.strip()

                    if not email:
                        hata_etiketi.set_text("E-posta adresi zorunludur.")
                        return

                    from merkez.servisler.sifre import sifirlama_talebi_olustur

                    token = await sifirlama_talebi_olustur(email=email)

                    # Güvenlik gereği: kayıtlı olup olmadığını açıklama
                    bilgi_etiketi.set_text(
                        "Kayıtlı bir hesap varsa sıfırlama bağlantısı gönderilecektir."
                    ).classes("text-green-600")

                    if token:
                        # SMTP entegrasyonu hazır olduğunda buraya e-posta gönderimi eklenecek
                        # from merkez.servisler.smtp import sifirlama_maili_gonder
                        # await sifirlama_maili_gonder(email=email, token=token)
                        pass

                ui.button(
                    "Sıfırlama Bağlantısı Gönder",
                    on_click=talep_olustur,
                ).props("color=primary unelevated").classes("w-full")

                email_input.on("keydown.enter", talep_olustur)

                ui.separator()

                with ui.row().classes("w-full justify-center"):
                    ui.link("Giriş Sayfasına Dön", "/giris").classes("text-sm text-blue-600")
