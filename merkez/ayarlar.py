import os
from dotenv import load_dotenv

load_dotenv()


def _zorunlu(anahtar: str) -> str:
    """Ortam değişkeni yoksa uygulamayı başlatmadan hata fırlatır."""
    deger = os.environ.get(anahtar, "").strip()
    if not deger:
        raise EnvironmentError(
            f"Zorunlu ortam değişkeni tanımlı değil: '{anahtar}'\n"
            f"Lütfen .env dosyanıza ekleyin veya sunucu ortam değişkenlerini kontrol edin."
        )
    return deger


# ── Zorunlu (eksikse uygulama başlamaz) ─────────────────────────────────────
VERITABANI_URL: str = _zorunlu("VERITABANI_URL")
JWT_GIZLI_ANAHTAR: str = _zorunlu("JWT_GIZLI_ANAHTAR")
ENCRYPTION_KEY: str = _zorunlu("ENCRYPTION_KEY")

# ── İsteğe bağlı (güvenli varsayılanlar) ────────────────────────────────────
JWT_ALGORITMA: str = "HS256"
JWT_SURE_DAKIKA: int = int(os.environ.get("JWT_SURE_DAKIKA", "480"))  # 8 saat
