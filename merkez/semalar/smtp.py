from pydantic import BaseModel


class SmtpBilgileri(BaseModel):
    sunucu: str
    port: int
    kullanici_adi: str
    sifre: str
    gonderici_adi: str