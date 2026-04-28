from sqlmodel import Field, SQLModel, UniqueConstraint


class Label(SQLModel, table=True):
    __tablename__ = "label"
    __table_args__ = (UniqueConstraint("name", "owner_id", name="uq_label_owner"),)

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=50)
    owner_id: int = Field(foreign_key="user.id", index=True)


class NoteLabelLink(SQLModel, table=True):
    __tablename__ = "note_label_link"
    __table_args__ = (UniqueConstraint("note_id", "label_id", name="uq_note_label"),)

    id: int = Field(default=None, primary_key=True)
    note_id: int = Field(foreign_key="note.id", index=True)
    label_id: int = Field(foreign_key="label.id", index=True)


class LabelCreate(SQLModel):
    name: str


class LabelRead(SQLModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
