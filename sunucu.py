from contextlib import asynccontextmanager
from fastapi import FastAPI
from nicegui import ui

from merkez.ayarlar import ENCRYPTION_KEY
from merkez.veritabani import vt_havuzunu_baslat, vt_havuzunu_kapat
from merkez.rotalar.kurulum import router as kurulum_router

# Bu importlar kullanılmıyor gibi görünse de SİLME.
# Her dosyadaki @ui.page("/...") dekoratörü, dosya import edildiği anda
# o adresi sisteme kaydeder. Import edilmezse sayfa 404 verir.
import sayfalar.kurulum          # noqa: F401  →  "/kurulum"  sayfasını kaydeder
import sayfalar.giris            # noqa: F401  →  "/giris"    sayfasını kaydeder
import sayfalar.sifremi_unuttum  # noqa: F401  →  "/sifremi-unuttum" sayfasını kaydeder
import sayfalar.sifre_sifirla    # noqa: F401  →  "/sifre-sifirla" sayfasını kaydeder
import sayfalar.panel            # noqa: F401  →  "/panel"    sayfasını kaydeder


@asynccontextmanager
async def lifespan(app: FastAPI):
    await vt_havuzunu_baslat()
    yield
    await vt_havuzunu_kapat()


app = FastAPI(
    title="İş Zekası Platformu API",
    redoc_url=None,
    lifespan=lifespan,
)

app.include_router(kurulum_router)


@ui.page("/")
async def ana_sayfa():
    from nicegui import app as nicegui_app
    from merkez.servisler import giris as servis_giris

    token = nicegui_app.storage.user.get("oturum_token")

    if token and await servis_giris.oturum_kontrol(token):
        ui.navigate.to("/panel")
        return

    try:
        from merkez.veritabani import vt_getir
        havuz = await vt_getir()
        async with havuz.acquire() as db:
            sayi = await db.fetchval("SELECT COUNT(*) FROM kullanicilar;")
        ui.navigate.to("/giris" if sayi > 0 else "/kurulum")
    except Exception:
        ui.navigate.to("/kurulum")


ui.run_with(app, title="İş Zekası Platformu", storage_secret=ENCRYPTION_KEY)