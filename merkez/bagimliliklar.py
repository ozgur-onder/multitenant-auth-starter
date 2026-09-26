from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from merkez.guvenlik import jwt_coz

_bearer = HTTPBearer()


async def giris_zorunlu(
    kimlik: HTTPAuthorizationCredentials = Depends(_bearer),
) -> str:
    sicil = jwt_coz(kimlik.credentials)
    if not sicil:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz veya süresi dolmuş token.",
        )
    return sicil