from nicegui import ui, app as nicegui_app
from merkez.servisler import giris as servis_giris
from merkez.semalar.giris import GirisGirisi


@ui.page("/giris")
async def giris_sayfasi():
    token = nicegui_app.storage.user.get("oturum_token")
    if token and await servis_giris.oturum_kontrol(token):
        ui.navigate.to("/panel")
        return

    with ui.column().classes("items-center justify-center min-h-screen w-full"):
        with ui.card().classes("w-full max-w-sm q-pa-md"):
            ui.label("Giriş Yap").classes("text-2xl font-bold text-center")
            ui.separator()

            sicil  = ui.input("Sicil No", placeholder="Örn: 10001").classes("w-full")
            parola = ui.input("Parola").props("type=password").classes("w-full")
            hata   = ui.label("").classes("text-negative text-caption")

            async def giris_yap():
                hata.text = ""
                sicil_no = (sicil.value or "").strip()
                if not sicil_no or not parola.value:
                    hata.text = "Sicil ve parola boş olamaz."
                    return
                try:
                    sonuc = await servis_giris.giris_yap(
                        GirisGirisi(sicil=sicil_no, parola=parola.value)
                    )
                    nicegui_app.storage.user["oturum_token"] = sonuc.token
                    ui.navigate.to("/panel")
                except ValueError as e:
                    hata.text = str(e)
                except Exception:
                    hata.text = "Giriş sırasında bir hata oluştu."

            sicil.on("keydown.enter",  giris_yap)
            parola.on("keydown.enter", giris_yap)

            ui.button("Giriş Yap", on_click=giris_yap).props("color=primary").classes("w-full")
            ui.link("Şifremi Unuttum", "/sifremi-unuttum").classes("text-caption")