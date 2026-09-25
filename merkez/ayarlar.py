import os
from dotenv import load_dotenv

load_dotenv()

VERITABANI_URL: str = os.environ.get("VERITABANI_URL", "")
JWT_GIZLI_ANAHTAR: str = os.environ.get("JWT_GIZLI_ANAHTAR", "gizli_anahtar_degistir")
JWT_ALGORITMA: str = "HS256"
JWT_SURE_DAKIKA: int = int(os.environ.get("JWT_SURE_DAKIKA", "480"))
ENCRYPTION_KEY: str = os.environ.get("ENCRYPTION_KEY", "gelistirme_anahtari")
