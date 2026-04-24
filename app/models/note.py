from enum import auto
from typing import Optional

from sqlmodel import Field, SQLModel


# Model
class Note(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, auto_increment=True)
    title: str
    content: str = ""
    color: Optional[str] = None
    owner_id: int = Field(foreign_key="user.id", index=True)


# DTOs
class NoteCreate(SQLModel):
    title: str
    content: str = ""
    color: Optional[str] = None
    label_ids: Optional[list[int]] = None


class NoteUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    color: Optional[str] = None
    label_ids: Optional[list[int]] = None


class NoteRead(SQLModel):
    id: int
    title: str
    content: str
    color: Optional[str] = None

    model_config = {"from_attributes": True}
