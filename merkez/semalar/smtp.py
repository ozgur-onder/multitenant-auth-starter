from pydantic import BaseModel


class SmtpAyarlariGirisi(BaseModel):
    firma_kodu: str
    sunucu: str
    port: int
    kullanici_adi: str
    sifre: str
    gonderici_adi: str
    olusturan_sicil: str