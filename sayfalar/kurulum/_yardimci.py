from nicegui import ui
from merkez.metin_islemleri import turkce_buyuk_harf


def _alan(label: str, placeholder: str = "", password: bool = False, genislik: str = "w-full") -> ui.input:
    inp = ui.input(
        label,
        placeholder=f"Örn: {placeholder}" if placeholder else "",
        password=password,
        password_toggle_button=password,
    ).classes(genislik)
    inp.props("dense")
    return inp


# Dönüşüm tarayıcıda yapılır; sunucuya gidip gelseydi hızlı yazarken harfler kaybolurdu.
_TARAYICIDA_BUYUK_HARF = (
    "const b=this.selectionStart,s=this.selectionEnd,u=this.value.toLocaleUpperCase('tr-TR');"
    "if(u!==this.value){this.value=u;this.setSelectionRange(b,s);}"
)


def _buyuk_harfle_yazdir(alan: ui.input) -> None:
    alan.props(f'oninput="{_TARAYICIDA_BUYUK_HARF}"')
    alan.on("blur", lambda: alan.set_value(turkce_buyuk_harf(alan.value or "")))


def _sayi_alani(label: str, placeholder: str = "", basamak: int = 10, genislik: str = "w-full") -> ui.input:
    # type=number yerine metin alanı + rakam maskesi: tarayıcının yukarı/aşağı okları çıkmaz.
    inp = ui.input(label, placeholder=f"Örn: {placeholder}" if placeholder else "").classes(genislik)
    inp.props(f'dense mask="{"#" * basamak}" inputmode=numeric')
    return inp


def _metin(alan: ui.input) -> str:
    return (alan.value or "").strip()


def _aciklama(metin: str) -> None:
    with ui.row().classes("items-center gap-3 q-px-sm q-py-xs q-mb-xs bg-blue-1 rounded-borders w-full no-wrap"):
        ui.icon("info", color="primary", size="sm")
        ui.label(metin).classes("text-caption text-grey-8")


def _degisince_hatayi_temizle(hata: ui.label, *alanlar: ui.input) -> None:
    for alan in alanlar:
        alan.on_value_change(lambda: hata.set_text(""))