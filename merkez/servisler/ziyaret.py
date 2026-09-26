from merkez.veritabani import vt_getir


async def ziyaret_baslat(sicil: str, sayfa: str, sayfa_basligi: str, oturum_token: str) -> int:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        return await db.fetchval(
            """INSERT INTO sayfa_ziyaret_loglari (sicil, sayfa, sayfa_basligi, oturum_token, giris_zamani, son_guncelleme)
               VALUES ($1, $2, $3, $4, LOCALTIMESTAMP, LOCALTIMESTAMP)
               RETURNING id;""",
            sicil, sayfa, sayfa_basligi, oturum_token,
        )


async def ziyaret_suresini_guncelle(ziyaret_id: int) -> None:
    # Süre veritabanı saatiyle ve mikro saniye hassasiyetle hesaplanıp milisaniyeye yuvarlanır.
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        await db.execute(
            """UPDATE sayfa_ziyaret_loglari
               SET son_guncelleme = LOCALTIMESTAMP,
                   sure_saniye    = ROUND(EXTRACT(EPOCH FROM (LOCALTIMESTAMP - giris_zamani)), 3)
               WHERE id = $1;""",
            ziyaret_id,
        )