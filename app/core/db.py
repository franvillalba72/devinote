import os
from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings

# Cambios para despliegue en Render.com, que proporciona la URL de la base de datos a través de la variable de entorno DATABASE_URL. Se ajusta el formato de la URL para que sea compatible con SQLAlchemy y se crea el motor de base de datos en función de esta URL.
raw_url = os.environ["DATABASE_URL"]
url = raw_url

if url.startswith("postgres://"):
    url = "postgresql+psycopg://" + url[len("postgres://") :]
    # url = url.replace("postgres://", "postgresql+psycopg://", 1)
elif url.startswith("postgresql://") and "+psycopg" not in url:
    url = "postgresql+psycopg://" + url[len("postgresql://") :]

engine = create_engine(url, pool_pre_ping=True)

# Este es el engine que se usaba en desarrollo local.
# engine = create_engine(
#     settings.DATABASE_URL,
#     echo=True,
#     connect_args=(
#         {"check_same_thread": False}
#         if settings.DATABASE_URL.startswith("sqlite")
#         else {}
#     ),
# )


def init_db() -> None:
    if settings.ENVIRONMENT == "dev":
        SQLModel.metadata.create_all(
            engine
        )  # development only, in production use migrations


# Dependencia para obtener una sesión de base de datos. Al usarla en un endpoint, FastAPI se encargará de crear una sesión y cerrarla después de la solicitud gracias al uso de with que es un gestor de contexto. Devuelve un generador que yield la sesión, lo que permite que FastAPI maneje su ciclo de vida automáticamente.
def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
