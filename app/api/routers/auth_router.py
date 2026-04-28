from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import DBSession
from app.models.user import UserCreate, UserLogin, UserRead
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: DBSession):
    service = AuthService(db)
    return service.register(payload)


@router.post("/login")
def login(user: UserLogin, db: DBSession):
    service = AuthService(db)
    token = service.login(user.email, user.password)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token")
def login(
    db: DBSession, form: OAuth2PasswordRequestForm = Depends()
):  # Endpoint para swagger, que espera un formulario con username y password. Aunque en nuestro caso username es el email, lo dejamos así para cumplir con el estándar de OAuth2.
    service = AuthService(db)
    token = service.login(form.username, form.password)
    return {"access_token": token, "token_type": "bearer"}
