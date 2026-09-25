from fastapi import Header, HTTPException, status
from merkez.servisler import giris as servis_giris


async def giris_zorunlu(authorization: str = Header(...)) -> str:
    """FastAPI endpoint'leri için JWT doğrulama bağımlılığı."""
    token = authorization.removeprefix("Bearer ").strip()
    if not token or not await servis_giris.oturum_kontrol(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Oturum geçersiz veya süresi dolmuş.",
        )
    return token
