from sqlmodel import Session, delete, select

from app.models.label import NoteLabelLink
from app.models.note import Note
from app.models.share import NoteShare


class NoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_owned(self, owner_id: int) -> list[Note]:
        return self.db.exec(
            select(Note).where(Note.owner_id == owner_id).order_by(Note.id.desc())
        ).all()

    def get_by_id(self, note_id: int) -> Note | None:
        return self.db.get(Note, note_id)

    def create(self, note: Note) -> Note:
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update(self, note: Note) -> Note:
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete(self, note: Note) -> None:
        self.db.exec(delete(NoteLabelLink).where(NoteLabelLink.note_id == note.id))
        self.db.exec(delete(NoteShare).where(NoteShare.note_id == note.id))
        self.db.delete(note)
        self.db.commit()

    def replace_labels(self, owner_id: int, note_id: int, label_ids: list[int]) -> None:
        # Elimina los enlaces existentes
        self.db.exec(delete(NoteLabelLink).where(NoteLabelLink.note_id == note_id))
        # Crea nuevos enlaces
        for label_id in set(label_ids or []):  # Evita duplicados y maneja None
            link = NoteLabelLink(note_id=note_id, label_id=label_id)
            self.db.add(link)
        self.db.commit()

    def list_by_ids(self, note_ids: list[int]) -> list[Note]:
        if not note_ids:
            return []
        return self.db.exec(select(Note).where(Note.id.in_(set(note_ids)))).all()
