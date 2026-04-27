from fastapi import HTTPException
from sqlmodel import Session

from app.models.share import LabelShare, NoteShare, ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class ShareService:
    def __init__(self, db: Session):
        self.note_repo = NoteRepository(db)
        self.label_repo = LabelRepository(db)
        self.shared_repo = ShareRepository(db)

    def share_note(
        self, owner_id: int, note_id: int, target_user_id: int, role: ShareRole
    ) -> NoteShare:
        note = self.note_repo.get_by_id(note_id)
        if not note or note.owner_id != owner_id:
            raise HTTPException(
                status_code=404, detail="Nota no encontrada o no autorizada"
            )

        share = self.shared_repo.upsert_note_share(
            note_id=note_id,
            user_id=target_user_id,
            role=role.value if hasattr(role, "value") else role,
        )

        return share

    def unshare_note(self, owner_id: int, note_id: int, target_user_id: int):
        note = self.note_repo.get_by_id(note_id)
        if not note or note.owner_id != owner_id:
            raise HTTPException(
                status_code=404, detail="Nota no encontrada o no autorizada"
            )

        self.shared_repo.remove_note_share(note_id=note_id, user_id=target_user_id)

    def share_label(
        self, owner_id: int, label_id: int, target_user_id: int, role: ShareRole
    ) -> LabelShare:
        label = self.label_repo.get_by_id(label_id)
        if not label or label.owner_id != owner_id:
            raise HTTPException(
                status_code=404, detail="Etiqueta no encontrada o no autorizada"
            )

        share = self.shared_repo.upsert_label_share(
            label_id=label_id,
            user_id=target_user_id,
            role=role.value if hasattr(role, "value") else role,
        )

        return share

    def unshare_label(self, owner_id: int, label_id: int, target_user_id: int):
        label = self.label_repo.get_by_id(label_id)
        if not label or label.owner_id != owner_id:
            raise HTTPException(
                status_code=404, detail="Etiqueta no encontrada o no autorizada"
            )

        self.shared_repo.remove_label_share(label_id=label_id, user_id=target_user_id)
