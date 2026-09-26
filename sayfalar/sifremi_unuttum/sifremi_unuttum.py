from nicegui import ui
from merkez.servisler.sifre import sifirlama_talebi_olustur


@ui.page("/sifremi-unuttum")
async def sifremi_unuttum_sayfasi():
    with ui.column().classes("items-center justify-center min-h-screen w-full"):
        with ui.card().classes("w-full max-w-sm q-pa-md"):
            ui.label("Şifremi Unuttum").classes("text-2xl font-bold text-center")
            ui.separator()
            ui.label("E-posta adresinizi girin, şifre sıfırlama bağlantısı göndereceğiz.").classes("text-caption text-grey-7")

            email = ui.input("E-posta", placeholder="Örn: ornek@firma.com").classes("w-full")
            bilgi  = ui.label("").classes("text-caption")

            async def gonder():
                bilgi.text = ""
                adres = (email.value or "").strip()
                if not adres:
                    bilgi.classes(replace="text-negative text-caption")
                    bilgi.text = "E-posta adresi boş olamaz."
                    return
                await sifirlama_talebi_olustur(adres)
                bilgi.classes(replace="text-positive text-caption")
                bilgi.text = "Eğer bu e-posta kayıtlıysa, sıfırlama bağlantısı gönderildi."

            ui.button("Gönder", on_click=gonder).props("color=primary").classes("w-full")
            ui.link("Giriş sayfasına dön", "/giris").classes("text-caption")