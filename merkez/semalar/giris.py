from pydantic import BaseModel


class GirisGirisi(BaseModel):
    sicil_veya_eposta: str
    parola: str


class GirisCiktisi(BaseModel):
    token: str
    sicil: str