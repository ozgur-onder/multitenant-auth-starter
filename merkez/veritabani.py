import asyncpg
from merkez.ayarlar import VERITABANI_URL

_havuz: asyncpg.Pool | None = None


async def vt_havuzunu_baslat() -> None:
    global _havuz
    _havuz = await asyncpg.create_pool(VERITABANI_URL, min_size=2, max_size=10)


async def vt_havuzunu_kapat() -> None:
    global _havuz
    if _havuz:
        await _havuz.close()
        _havuz = None


async def vt_getir() -> asyncpg.Pool:
    if _havuz is None:
        raise RuntimeError("Veritabanı havuzu başlatılmamış.")
    return _havuz