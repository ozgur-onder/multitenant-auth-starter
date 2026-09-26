from datetime import date
from merkez.veritabani import vt_getir

_SIRA_BASAMAK = 4


async def sicil_uret() -> str:
    """Sicil = işe giriş yılı (4 hane) + o yıl içindeki sıra (4 hane). Örn: 20260001, 20260002 ..."""
    yil = str(date.today().year)
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        son_sicil = await db.fetchval(
            "SELECT MAX(sicil) FROM kullanicilar WHERE sicil ~ $1;",
            f"^{yil}[0-9]{{{_SIRA_BASAMAK}}}$",
        )
    sira = int(son_sicil[len(yil):]) + 1 if son_sicil else 1
    if sira >= 10 ** _SIRA_BASAMAK:
        raise ValueError(f"{yil} yılı için sicil numarası kapasitesi doldu.")
    return f"{yil}{sira:0{_SIRA_BASAMAK}d}"