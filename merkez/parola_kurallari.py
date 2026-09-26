from typing import Callable

PAROLA_EN_AZ_UZUNLUK = 12

PAROLA_KURALLARI: list[tuple[str, Callable[[str], bool]]] = [
    (f"En az {PAROLA_EN_AZ_UZUNLUK} karakter", lambda p: len(p) >= PAROLA_EN_AZ_UZUNLUK),
    ("Büyük harf",    lambda p: any(k.isupper() for k in p)),
    ("Küçük harf",    lambda p: any(k.islower() for k in p)),
    ("Rakam",         lambda p: any(k.isdigit() for k in p)),
    ("Özel karakter", lambda p: any(not k.isalnum() and not k.isspace() for k in p)),
]


def eksik_parola_kurallari(parola: str) -> list[str]:
    return [ad for ad, kontrol in PAROLA_KURALLARI if not kontrol(parola)]