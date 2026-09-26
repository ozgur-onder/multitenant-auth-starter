from pydantic import BaseModel


class GirisGirisi(BaseModel):
    sicil: str
    parola: str


class GirisCiktisi(BaseModel):
    token: str
    sicil: str