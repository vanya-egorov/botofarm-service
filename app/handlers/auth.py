from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = HTTPBearer()

ADMIN_TOKEN = "admin-secret"


async def verify_admin_token(
    credentials: HTTPAuthorizationCredentials = Depends(router)
) -> bool:
    if credentials.credentials != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
