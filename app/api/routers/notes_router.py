from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DBSession
from app.models.note import NoteCreate, NoteRead, NoteUpdate
from app.services.note_service import NoteService


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model=list[NoteRead])
def list_notes(db: DBSession, current_user: CurrentUser):
    return NoteService(db).list_visible(current_user.id)


@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, db: DBSession, current_user: CurrentUser):
    return NoteService(db).create(current_user.id, payload)


@router.patch("/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int, payload: NoteUpdate, db: DBSession, current_user: CurrentUser
):
    return NoteService(db).update(current_user.id, note_id, payload)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: DBSession, current_user: CurrentUser):
    NoteService(db).delete(current_user.id, note_id)

    return None
