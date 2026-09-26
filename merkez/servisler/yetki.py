from merkez.veritabani import vt_getir


async def kullanicinin_yetki_kodlari(sicil: str) -> set[str]:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        satirlar = await db.fetch(
            """SELECT DISTINCT y.yetki_kodu
               FROM kullanici_yetkileri ky
               JOIN roller r         ON r.rol_kodu = ky.rol_kodu AND r.durum = TRUE
               JOIN rol_yetkileri ry ON ry.rol_kodu = ky.rol_kodu
               JOIN yetkiler y       ON y.yetki_kodu = ry.yetki_kodu AND y.durum = TRUE
               WHERE ky.sicil = $1 AND ky.durum = TRUE;""",
            sicil,
        )
    return {s["yetki_kodu"] for s in satirlar}