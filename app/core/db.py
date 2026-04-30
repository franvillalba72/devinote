from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args=(
        {"check_same_thread": False}
        if settings.DATABASE_URL.startswith("sqlite")
        else {}
    ),
)


def init_db() -> None:
    if settings.ENVIRONMENT == "dev":
        SQLModel.metadata.create_all(
            engine
        )  # development only, in production use migrations


# Dependencia para obtener una sesión de base de datos. Al usarla en un endpoint, FastAPI se encargará de crear una sesión y cerrarla después de la solicitud gracias al uso de with que es un gestor de contexto. Devuelve un generador que yield la sesión, lo que permite que FastAPI maneje su ciclo de vida automáticamente.
def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
