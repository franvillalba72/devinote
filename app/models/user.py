from enum import auto

from sqlmodel import Field, SQLModel


# Clase para el modelo
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, auto_increment=True)
    email: str = Field(index=True, nullable=False, unique=True)
    full_name: str = Field(default="")
    hashed_password: str


# Clases para validaciones
class UserCreate(SQLModel):
    email: str
    full_name: str = ""
    password: str


class UserRead(SQLModel):
    id: int
    email: str
    full_name: str
    model_config = {
        "from_attributes": True
    }  # Permite crear un UserRead a partir de un User
