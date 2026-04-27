from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.db import get_session
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_db() -> Session:
    return next(
        get_session()
    )  # next se encarga de coger el primer valor de un generador, en este caso la sesión que se crea en get_session. Esto es necesario porque FastAPI espera una función que devuelva un valor, no un generador. Al usar next, obtenemos la sesión directamente para usarla en los endpoints.


DBSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: DBSession
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
        repo = UserRepository(db)
        user = repo.get_by_id(user_id)
        if not user:
            raise credentials_exc
    except Exception:
        raise credentials_exc

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
