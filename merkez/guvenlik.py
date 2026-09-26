from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from merkez.ayarlar import JWT_GIZLI_ANAHTAR, JWT_ALGORITMA, JWT_SURE_DAKIKA

# bcrypt 72 bayttan uzun parolaları kabul etmez.
_BCRYPT_AZAMI_BAYT = 72


def sifreyi_hashle(sifre: str) -> str:
    sifre_bayt = sifre.encode("utf-8")
    if len(sifre_bayt) > _BCRYPT_AZAMI_BAYT:
        raise ValueError("Parola çok uzun (en fazla 72 bayt).")
    return bcrypt.hashpw(sifre_bayt, bcrypt.gensalt()).decode("utf-8")


def sifre_dogrula(sifre: str, hashli: str) -> bool:
    sifre_bayt = sifre.encode("utf-8")
    if len(sifre_bayt) > _BCRYPT_AZAMI_BAYT:
        return False
    return bcrypt.checkpw(sifre_bayt, hashli.encode("utf-8"))


def jwt_olustur(sicil: str) -> str:
    bitis = datetime.now(timezone.utc) + timedelta(minutes=JWT_SURE_DAKIKA)
    return jwt.encode({"sub": sicil, "exp": bitis}, JWT_GIZLI_ANAHTAR, algorithm=JWT_ALGORITMA)


def jwt_coz(token: str) -> str | None:
    try:
        veri = jwt.decode(token, JWT_GIZLI_ANAHTAR, algorithms=[JWT_ALGORITMA])
        return veri.get("sub")
    except jwt.PyJWTError:
        return None