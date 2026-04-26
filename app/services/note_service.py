from fastapi import HTTPException
from sqlmodel import Session

from app.models import note
from app.models.note import Note, NoteCreate, NoteUpdate
from app.models.share import ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class NoteService:
    def __init__(self, db: Session):
        self.db = db
        self.note_repo = NoteRepository(db)
        self.label_repo = LabelRepository(db)
        self.shared_repo = ShareRepository(db)

    # Permisos
    def user_can_read(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True

        if self.shared_repo.has_note_share(note_id=note.id, user_id=user_id):
            return True

        label_ids = self.label_repo.list_label_ids_for_note(note.id)
        return self.shared_repo.has_any_label_share(
            label_ids=label_ids, user_id=user_id
        )

    def user_can_edit(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True

        if self.shared_repo.has_note_share(
            note_id=note.id, user_id=user_id, role=ShareRole.EDIT
        ):
            return True

        label_ids = self.label_repo.list_label_ids_for_note(note.id)
        return self.shared_repo.has_any_label_share(
            label_ids=label_ids, user_id=user_id, role=ShareRole.EDIT
        )

    # Operaciones
    def list_visible(self, user_id: int) -> list[Note]:
        owned = self.note_repo.list_owned(user_id)

        direct_ids = self.shared_repo.list_note_ids_shared_directly(user_id)

        shared_label_ids = self.shared_repo.list_label_ids_shared_directly(user_id)
        ids_by_label = self.label_repo.list_note_ids_by_label_ids(shared_label_ids)

        combined_ids = list({*direct_ids, *ids_by_label})
        shared = self.note_repo.list_by_ids(combined_ids)

        combined = {note.id: note for note in owned}
        for note in shared:
            combined.setdefault(note.id, note)

        return sorted(combined.values(), key=lambda note: note.id, reverse=True)

    def create(self, owner_id: int, payload: NoteCreate) -> Note:
        note = self.note_repo.create(
            Note(owner_id=owner_id, **payload.model_dump(exclude={"label_ids"}))
        )
        if payload.label_ids:
            self._set_labels(owner_id, note.id, payload.label_ids)
        return note

    def update(self, user_id: int, note_id: int, payload: NoteUpdate) -> Note:
        note = self.note_repo.get_by_id(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Nota no encontrada")
        if not self.user_can_edit(user_id, note):
            raise HTTPException(status_code=403, detail="Permiso denegado")

        updates = payload.model_dump(exclude_none=True)
        label_ids = updates.pop("label_ids", None)

        for key, value in updates.items():
            setattr(note, key, value)

        updated_note = self.note_repo.update(note)

        if label_ids is not None:
            if note.owner_id != user_id:
                raise HTTPException(
                    status_code=404,
                    detail="Solo el propietario puede modificar etiquetas",
                )
            self._set_labels(user_id, updated_note.id, label_ids)

        return updated_note

    def delete(self, user_id: int, note_id: int) -> None:
        note = self.note_repo.get_by_id(note_id)
        if not note or note.owner_id != user_id:
            raise HTTPException(
                status_code=404, detail="Nota no encontrada o no autorizado"
            )
        if not self.user_can_edit(user_id, note):
            raise HTTPException(status_code=403, detail="Permiso denegado")

        self.note_repo.delete(note)

    # Helper para asignar etiquetas a una nota
    def _set_labels(self, owner_id: int, note_id: int, label_ids: list[int]) -> None:
        valid_ids = self.label_repo.list_ids_for_owner_subset(owner_id, label_ids or [])
        self.note_repo.replace_labels(owner_id, note_id, valid_ids)
