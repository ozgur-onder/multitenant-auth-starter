from fastapi import APIRouter
from merkez.semalar.kurulum import KurulumGirisi
from merkez.servisler.kurulum import ilk_kurulumu_yap

router = APIRouter(prefix="/api")


@router.post("/kurulum")
async def kurulum_endpoint(veri: KurulumGirisi):
    await ilk_kurulumu_yap(veri)
    return {"mesaj": "Kurulum tamamlandı."}