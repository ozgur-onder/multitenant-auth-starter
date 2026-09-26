from fastapi import APIRouter, HTTPException, status
from merkez.semalar.kurulum import KurulumGirisi
from merkez.servisler.kurulum import ilk_kurulumu_yap

router = APIRouter(prefix="/api")


@router.post("/kurulum")
async def kurulum_endpoint(veri: KurulumGirisi):
    try:
        await ilk_kurulumu_yap(veri)
    except ValueError as hata:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(hata))
    return {"mesaj": "Kurulum tamamlandı."}