from fastapi import APIRouter, HTTPException, status
from merkez.semalar.kurulum import KurulumGirisi
from merkez.servisler.kurulum import ilk_kurulumu_yap

router = APIRouter(prefix="/api", tags=["Kurulum"])


@router.post("/kurulum", status_code=status.HTTP_201_CREATED)
async def ilk_kurulum_endpoint(veri: KurulumGirisi):
    """İlk sistem kurulumunu gerçekleştirir. Yalnızca hiç kullanıcı yokken çalışır."""
    try:
        await ilk_kurulumu_yap(veri)
        return {"mesaj": "Kurulum başarıyla tamamlandı."}
    except ValueError as hata:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(hata))
