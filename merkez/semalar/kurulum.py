from pydantic import BaseModel


class KurulumGirisi(BaseModel):
    sicil: str
    ad: str
    soyad: str
    email: str
    parola: str
    firma_kodu: str
    firma_adi: str
