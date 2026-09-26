from nicegui import ui
from merkez.metin_islemleri import turkce_buyuk_harf


def alan(
    label: str,
    placeholder: str = "",
    password: bool = False,
    genislik: str = "w-full",
    ikon: str | None = None,
) -> ui.input:
    girdi = ui.input(
        label,
        placeholder=f"Örn: {placeholder}" if placeholder else "",
        password=password,
        password_toggle_button=password,
    ).classes(genislik)
    girdi.props("dense")
    if ikon:
        with girdi.add_slot("prepend"):
            ui.icon(ikon, size="xs")
    return girdi


def sayi_alani(label: str, placeholder: str = "", basamak: int = 10, genislik: str = "w-full") -> ui.input:
    # type=number yerine metin alanı + rakam maskesi: tarayıcının yukarı/aşağı okları çıkmaz.
    girdi = ui.input(label, placeholder=f"Örn: {placeholder}" if placeholder else "").classes(genislik)
    girdi.props(f'dense mask="{"#" * basamak}" inputmode=numeric')
    return girdi


def alan_degeri(girdi: ui.input) -> str:
    return (girdi.value or "").strip()


# Dönüşüm tarayıcıda yapılır; sunucuya gidip gelseydi hızlı yazarken harfler kaybolurdu.
_TARAYICIDA_BUYUK_HARF = (
    "const b=this.selectionStart,s=this.selectionEnd,u=this.value.toLocaleUpperCase('tr-TR');"
    "if(u!==this.value){this.value=u;this.setSelectionRange(b,s);}"
)


def buyuk_harfle_yazdir(girdi: ui.input) -> None:
    girdi.props(f'oninput="{_TARAYICIDA_BUYUK_HARF}"')
    girdi.on("blur", lambda: girdi.set_value(turkce_buyuk_harf(girdi.value or "")))


def aciklama(metin: str) -> None:
    with ui.row().classes("items-center gap-3 q-px-sm q-py-xs q-mb-xs bg-blue-1 rounded-borders w-full no-wrap"):
        ui.icon("info", color="primary", size="sm")
        ui.label(metin).classes("text-caption text-grey-8")


def degisince_hatayi_temizle(hata: ui.label, *girdiler: ui.input) -> None:
    for girdi in girdiler:
        girdi.on_value_change(lambda: hata.set_text(""))


class MesajKutusu:
    """Başlangıçta gizli; hata veya başarı mesajını ikonlu, renkli bir kutuda gösterir."""

    def __init__(self) -> None:
        with ui.row().classes("items-center gap-2 q-px-sm q-py-xs rounded-borders w-full no-wrap") as self._kutu:
            self._ikon = ui.icon("error", size="sm")
            self._yazi = ui.label("").classes("text-body2")
        self._kutu.set_visibility(False)

    def hata(self, metin: str) -> None:
        self._goster(metin, ikon="error", renk="negative", arka_plan="bg-red-1")

    def basari(self, metin: str) -> None:
        self._goster(metin, ikon="check_circle", renk="positive", arka_plan="bg-green-1")

    def temizle(self) -> None:
        self._kutu.set_visibility(False)

    def _goster(self, metin: str, *, ikon: str, renk: str, arka_plan: str) -> None:
        # "replace" kullanılmaz; NiceGUI'nin satıra eklediği kendi düzen sınıfını da silerdi.
        self._ikon.name = ikon
        self._ikon.props(f"color={renk}")
        self._yazi.classes(remove="text-negative text-positive", add=f"text-{renk}")
        self._kutu.classes(remove="bg-red-1 bg-green-1", add=arka_plan)
        self._yazi.text = metin
        self._kutu.set_visibility(True)