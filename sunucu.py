# sunucu.py — Uygulamanın başlangıç noktası. Sunucu buradan ayağa kalkar.

from contextlib import asynccontextmanager
from fastapi import FastAPI  # API iskeleti
from nicegui import ui       # Web arayüzü (sayfa, buton, form vb.)
from merkez.ayarlar import ENCRYPTION_KEY

# Veritabanı bağlantı havuzunu başlatan ve kapatan fonksiyonlar
from merkez.veritabani import vt_havuzunu_baslat, vt_havuzunu_kapat

# Kurulum işlemlerine ait API endpoint'lerini içeren router
from merkez.rotalar.kurulum import router as kurulum_router

# Bu importlar kullanılmıyor gibi görünse de SİLME.
# Her dosyadaki @ui.page("/...") dekoratörü, dosya import edildiği anda
# o adresi sisteme kaydeder. Import edilmezse sayfa 404 verir.
import sayfalar.kurulum          # noqa: F401  →  "/kurulum"  sayfasını kaydeder
import sayfalar.giris            # noqa: F401  →  "/giris"    sayfasını kaydeder
import sayfalar.sifremi_unuttum  # noqa: F401  →  "/sifremi-unuttum" sayfasını kaydeder
import sayfalar.panel            # noqa: F401  →  "/panel"    sayfasını kaydeder


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Sunucu açılırken (yield öncesi) ve kapanırken (yield sonrası) çalışır.
    Veritabanı bağlantı havuzunu burada kurup temiz şekilde kapatıyoruz.
    """
    await vt_havuzunu_baslat()  # Sunucu açılırken: havuzu kur
    yield
    await vt_havuzunu_kapat()   # Sunucu kapanırken: bağlantıları kapat


# FastAPI uygulamasını oluştur
app = FastAPI(
    title="İş Zekası Platformu API",  # /docs sayfasında görünecek başlık
    redoc_url=None,                   # /redoc dokümantasyon sayfasını kapat
    lifespan=lifespan,                # Açılış/kapanış fonksiyonunu bağla
)

# Kurulum router'ındaki endpoint'leri uygulamaya ekle
app.include_router(kurulum_router)


@ui.page("/")
async def ana_sayfa():
    """
    Kök adrese ("/") gelen kullanıcıyı doğru sayfaya yönlendirir.
    Hiçbir şey göstermez, sadece yönlendirme yapar.
    """
    # Fonksiyon içinde import: üstte FastAPI'nin app'i var,
    # isim çakışmasını önlemek için nicegui_app adıyla alıyoruz.
    from nicegui import app as nicegui_app
    from merkez.servisler import giris as servis_giris

    # Tarayıcıda kayıtlı oturum token'ı var mı kontrol et
    token = nicegui_app.storage.user.get("oturum_token")

    # Token varsa ve geçerliyse doğrudan panele gönder
    if token and await servis_giris.oturum_kontrol(token):
        ui.navigate.to("/panel")
        return

    # Oturum yoksa: veritabanında hiç kullanıcı var mı bak
    try:
        from merkez.veritabani import vt_getir
        havuz = await vt_getir()
        async with havuz.acquire() as db:
            sayi = await db.fetchval("SELECT COUNT(*) FROM kullanicilar;")

        # Kullanıcı varsa → giriş sayfası, yoksa → ilk kurulum sayfası
        ui.navigate.to("/giris" if sayi > 0 else "/kurulum")

    except Exception:
        # Hata olursa (tablo yok, bağlantı kopuk vb.) kuruluma düş
        ui.navigate.to("/kurulum")


# NiceGUI'yi mevcut FastAPI uygulamasına bağlayarak sunucuyu başlat.
# ui.run() değil ui.run_with() — çünkü app'i biz oluşturduk, o sadece ekleniyor.
# storage_secret olmazsa nicegui_app.storage.user çalışmaz.
ui.run_with(app, title="İş Zekası Platformu", storage_secret=ENCRYPTION_KEY)