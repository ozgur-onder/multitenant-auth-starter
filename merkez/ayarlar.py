import os
from dotenv import load_dotenv

load_dotenv()


def _zorunlu(anahtar: str) -> str:
    deger = os.environ.get(anahtar, "").strip()
    if not deger:
        raise EnvironmentError(
            f"Zorunlu ortam değişkeni tanımlı değil: '{anahtar}'. "
            f"Lütfen .env dosyasını kontrol edin."
        )
    return deger


VERITABANI_URL:    str = _zorunlu("VERITABANI_URL")
JWT_GIZLI_ANAHTAR: str = _zorunlu("JWT_GIZLI_ANAHTAR")
ENCRYPTION_KEY:    str = _zorunlu("ENCRYPTION_KEY")

JWT_ALGORITMA:   str = "HS256"
JWT_SURE_DAKIKA: int = int(os.environ.get("JWT_SURE_DAKIKA", "480"))

# E-postalardaki bağlantılar bu adrese göre oluşturulur (örn. şifre sıfırlama).
UYGULAMA_ADRESI: str = os.environ.get("UYGULAMA_ADRESI", "http://localhost:8000").rstrip("/")