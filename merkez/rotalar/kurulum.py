from fastapi import APIRouter, HTTPException, status
from merkez.semalar.kurulum import KurulumGirisi
from merkez.servisler.kurulum import ilk_kurulumu_yap, kurulum_yapilmis_mi
from merkez.servisler.smtp import smtp_baglantisini_test_et

router = APIRouter(prefix="/api")


@router.post("/kurulum")
async def kurulum_endpoint(veri: KurulumGirisi):
    if await kurulum_yapilmis_mi():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Kurulum zaten yapılmış.")
    try:
        await smtp_baglantisini_test_et(veri.smtp)
        await ilk_kurulumu_yap(veri)
    except ValueError as hata:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(hata))
    return {"mesaj": "Kurulum tamamlandı."}