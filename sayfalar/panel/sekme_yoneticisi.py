from functools import partial
from typing import Callable
from nicegui import ui
from merkez.servisler.giris import oturum_kontrol
from merkez.servisler.ziyaret import ziyaret_baslat, ziyaret_suresini_guncelle
from .baglam import PanelBaglami
from .menu import MenuOgesi

_NABIZ_SANIYE = 30


class SekmeYoneticisi:
    """Sol menüden açılan sayfaları sekme olarak yönetir ve her sekmenin ziyaret süresini loglar."""

    def __init__(self, baglam: PanelBaglami, oturum_token: str) -> None:
        self._baglam = baglam
        self._token = oturum_token
        self._ogeler: dict[str, MenuOgesi] = {}
        self._acik: dict[str, tuple[ui.tab, ui.tab_panel]] = {}
        self._acilis_sirasi: list[str] = []
        self._degisim_dinleyicileri: list[Callable[[str | None], None]] = []
        self._ziyaret_id: int | None = None
        self.sekmeler: ui.tabs
        self.paneller: ui.tab_panels

    def sekme_cubugu_olustur(self) -> None:
        self.sekmeler = ui.tabs(on_change=self._sekme_degisti) \
            .props("dense no-caps inline-label align=left outside-arrows mobile-arrows "
                   "active-color=primary indicator-color=primary") \
            .classes("w-full text-grey-7")

    def panel_alani_olustur(self) -> None:
        self.paneller = ui.tab_panels(self.sekmeler).props("animated").classes("w-full bg-transparent")
        ui.timer(_NABIZ_SANIYE, self._nabiz)
        ui.context.client.on_disconnect(self._ziyareti_guncelle)

    @property
    def _aktif_anahtar(self) -> str | None:
        deger = self.sekmeler.value
        return deger if isinstance(deger, str) else None

    def degisince(self, dinleyici: Callable[[str | None], None]) -> None:
        self._degisim_dinleyicileri.append(dinleyici)

    async def ac(self, oge: MenuOgesi) -> None:
        if oge.anahtar not in self._acik:
            self._ogeler[oge.anahtar] = oge
            with self.sekmeler:
                with ui.tab(oge.anahtar, label=oge.baslik, icon=oge.ikon) as sekme:
                    if oge.kapatilabilir:
                        ui.button(icon="close").props("flat round dense size=xs color=grey-6") \
                            .classes("q-ml-xs").on("click.stop", partial(self.kapat, oge.anahtar))
            with self.paneller:
                with ui.tab_panel(sekme).classes("q-pa-none") as panel:
                    with ui.column().classes("w-full gap-4"):
                        await oge.olustur(self._baglam)
            self._acik[oge.anahtar] = (sekme, panel)
            self._acilis_sirasi.append(oge.anahtar)
        self.sekmeler.set_value(oge.anahtar)

    def kapat(self, anahtar: str) -> None:
        if anahtar not in self._acik:
            return
        sekme, panel = self._acik.pop(anahtar)
        self._acilis_sirasi.remove(anahtar)
        if self._aktif_anahtar == anahtar:
            self.sekmeler.set_value(self._acilis_sirasi[-1] if self._acilis_sirasi else None)
        sekme.delete()
        panel.delete()

    async def _sekme_degisti(self) -> None:
        await self._ziyareti_guncelle()
        self._ziyaret_id = None
        anahtar = self._aktif_anahtar
        if anahtar in self._ogeler:
            oge = self._ogeler[anahtar]
            self._ziyaret_id = await ziyaret_baslat(
                self._baglam.kullanici.sicil, f"/panel/{oge.anahtar}", oge.baslik, self._token,
            )
        for dinleyici in self._degisim_dinleyicileri:
            dinleyici(anahtar)

    async def _ziyareti_guncelle(self) -> None:
        if self._ziyaret_id is not None:
            await ziyaret_suresini_guncelle(self._ziyaret_id)

    async def _nabiz(self) -> None:
        # Tarayıcı çökse bile süre en fazla nabız aralığı kadar eksik kalır; kapanmış oturumda sayfa girişe döner.
        await self._ziyareti_guncelle()
        if not await oturum_kontrol(self._token):
            ui.navigate.to("/giris")