from pydantic import BaseModel
from merkez.semalar.smtp import SmtpBilgileri


class KurulumGirisi(BaseModel):
    sicil: str
    ad: str
    soyad: str
    email: str
    parola: str
    smtp: SmtpBilgileri