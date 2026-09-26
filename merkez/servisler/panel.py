from dataclasses import dataclass
from merkez.veritabani import vt_getir


@dataclass(frozen=True)
class OturumKullanicisi:
    sicil: str
    ad: str
    soyad: str
    email: str
    firma_adi: str
    rol_adi: str

    @property
    def ad_soyad(self) -> str:
        return f"{self.ad} {self.soyad}"

    @property
    def bas_harfler(self) -> str:
        return (self.ad[:1] + self.soyad[:1]).upper()


async def oturum_kullanicisini_getir(oturum_token: str) -> OturumKullanicisi | None:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        satir = await db.fetchrow(
            """SELECT k.sicil, k.ad, k.soyad, k.email,
                      COALESCE(f.firma_adi, '-') AS firma_adi,
                      COALESCE(r.rol_adi, '-')   AS rol_adi
               FROM kullanici_oturumlari o
               JOIN kullanicilar k             ON k.sicil = o.sicil AND k.durum = TRUE
               LEFT JOIN kullanici_yetkileri ky ON ky.sicil = k.sicil AND ky.durum = TRUE
               LEFT JOIN firma f               ON f.firma_kodu = ky.firma_kodu
               LEFT JOIN roller r              ON r.rol_kodu = ky.rol_kodu
               WHERE o.oturum_token = $1 AND o.durum = 'aktif'
               ORDER BY ky.rol_kodu
               LIMIT 1;""",
            oturum_token,
        )
    return OturumKullanicisi(**dict(satir)) if satir else None


async def ozet_sayilari() -> dict[str, int]:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        satir = await db.fetchrow(
            """SELECT
                 (SELECT COUNT(*) FROM kullanicilar WHERE durum = TRUE) AS kullanici,
                 (SELECT COUNT(*) FROM firma        WHERE durum = TRUE) AS firma,
                 (SELECT COUNT(*) FROM roller       WHERE durum = TRUE) AS rol,
                 (SELECT COUNT(*) FROM kullanici_oturumlari WHERE durum = 'aktif') AS aktif_oturum;"""
        )
    return dict(satir)


async def son_giris_hareketleri(limit: int = 10) -> list[dict]:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        satirlar = await db.fetch(
            """SELECT g.islem_zamani, g.sicil, k.ad || ' ' || k.soyad AS ad_soyad, g.durum,
                      host(g.ip_adresi) AS ip_adresi, g.tarayici
               FROM kullanici_giris_loglari g
               JOIN kullanicilar k ON k.sicil = g.sicil
               ORDER BY g.islem_zamani DESC
               LIMIT $1;""",
            limit,
        )
    return [dict(s) for s in satirlar]


async def kullanicinin_oturumlari(sicil: str, limit: int = 10) -> list[dict]:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        satirlar = await db.fetch(
            """SELECT giris_zamani, cikis_zamani, durum, host(ip_adresi) AS ip_adresi, tarayici
               FROM kullanici_oturumlari
               WHERE sicil = $1
               ORDER BY giris_zamani DESC
               LIMIT $2;""",
            sicil, limit,
        )
    return [dict(s) for s in satirlar]


async def kullanici_listesi() -> list[dict]:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        satirlar = await db.fetch(
            """SELECT k.sicil, k.ad || ' ' || k.soyad AS ad_soyad, k.email, k.durum, k.olusturma_zamani,
                      COALESCE(string_agg(DISTINCT f.firma_adi, ', '), '-') AS firmalar,
                      COALESCE(string_agg(DISTINCT r.rol_adi, ', '), '-')   AS roller
               FROM kullanicilar k
               LEFT JOIN kullanici_yetkileri ky ON ky.sicil = k.sicil AND ky.durum = TRUE
               LEFT JOIN firma f               ON f.firma_kodu = ky.firma_kodu
               LEFT JOIN roller r              ON r.rol_kodu = ky.rol_kodu
               GROUP BY k.id
               ORDER BY k.sicil;"""
        )
    return [dict(s) for s in satirlar]


async def firma_listesi() -> list[dict]:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        satirlar = await db.fetch(
            "SELECT firma_kodu, firma_adi, durum, olusturma_guncelleme_zamani FROM firma ORDER BY id;"
        )
    return [dict(s) for s in satirlar]


async def rol_listesi() -> list[dict]:
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        satirlar = await db.fetch(
            """SELECT r.rol_kodu, r.rol_adi, r.durum,
                      (SELECT COUNT(*) FROM rol_yetkileri ry WHERE ry.rol_kodu = r.rol_kodu) AS yetki_sayisi,
                      (SELECT COUNT(*) FROM kullanici_yetkileri ky WHERE ky.rol_kodu = r.rol_kodu AND ky.durum = TRUE) AS kullanici_sayisi
               FROM roller r
               ORDER BY r.rol_kodu;"""
        )
    return [dict(s) for s in satirlar]


async def yetki_matrisi() -> tuple[list[dict], list[dict]]:
    """(roller, satırlar) döner; her satırda yetki bilgisi ve her rol için 'rol_<kod>': bool bulunur."""
    havuz = await vt_getir()
    async with havuz.acquire() as db:
        roller = [dict(r) for r in await db.fetch(
            "SELECT rol_kodu, rol_adi FROM roller WHERE durum = TRUE ORDER BY rol_kodu;"
        )]
        yetkiler = await db.fetch("SELECT modul, yetki_kodu, yetki_adi FROM yetkiler WHERE durum = TRUE ORDER BY id;")
        atamalar = {(a["rol_kodu"], a["yetki_kodu"]) for a in await db.fetch("SELECT rol_kodu, yetki_kodu FROM rol_yetkileri;")}
    satirlar = []
    for y in yetkiler:
        satir = dict(y)
        for r in roller:
            satir[f"rol_{r['rol_kodu']}"] = (r["rol_kodu"], y["yetki_kodu"]) in atamalar
        satirlar.append(satir)
    return roller, satirlar