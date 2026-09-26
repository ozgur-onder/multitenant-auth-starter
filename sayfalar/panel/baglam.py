from dataclasses import dataclass
from merkez.servisler.panel import OturumKullanicisi


@dataclass(frozen=True)
class PanelBaglami:
    kullanici: OturumKullanicisi
    yetkiler: set[str]