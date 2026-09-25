from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from merkez.ayarlar import JWT_GIZLI_ANAHTAR, JWT_ALGORITMA, JWT_SURE_DAKIKA

_sifre_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def sifreyi_hashle(sifre: str) -> str:
    return _sifre_context.hash(sifre)


def sifre_dogrula(sifre: str, hashli_sifre: str) -> bool:
    return _sifre_context.verify(sifre, hashli_sifre)


def jwt_olustur(veri: dict) -> str:
    veri_kopya = veri.copy()
    veri_kopya["exp"] = datetime.now(timezone.utc) + timedelta(minutes=JWT_SURE_DAKIKA)
    return jwt.encode(veri_kopya, JWT_GIZLI_ANAHTAR, algorithm=JWT_ALGORITMA)


def jwt_coz(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_GIZLI_ANAHTAR, algorithms=[JWT_ALGORITMA])
    except jwt.PyJWTError:
        return None
