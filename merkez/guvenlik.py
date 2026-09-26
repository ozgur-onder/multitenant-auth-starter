from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from merkez.ayarlar import JWT_GIZLI_ANAHTAR, JWT_ALGORITMA, JWT_SURE_DAKIKA

_sifrele = CryptContext(schemes=["bcrypt"], deprecated="auto")


def sifreyi_hashle(sifre: str) -> str:
    return _sifrele.hash(sifre)


def sifre_dogrula(sifre: str, hashli: str) -> bool:
    return _sifrele.verify(sifre, hashli)


def jwt_olustur(sicil: str) -> str:
    bitis = datetime.now(timezone.utc) + timedelta(minutes=JWT_SURE_DAKIKA)
    return jwt.encode({"sub": sicil, "exp": bitis}, JWT_GIZLI_ANAHTAR, algorithm=JWT_ALGORITMA)


def jwt_coz(token: str) -> str | None:
    try:
        veri = jwt.decode(token, JWT_GIZLI_ANAHTAR, algorithms=[JWT_ALGORITMA])
        return veri.get("sub")
    except jwt.PyJWTError:
        return None