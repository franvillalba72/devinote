from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DBSession
from app.models.share import NoteShare, ShareRequest
from app.services.share_service import ShareService


router = APIRouter(prefix="/shares", tags=["Shares"])


@router.post("/notes/{note_id}", status_code=status.HTTP_201_CREATED)
def share_note(
    note_id: int, payload: ShareRequest, db: DBSession, current_user: CurrentUser
):
    share = ShareService(db).share_note(
        current_user.id, note_id, payload.target_user_id, payload.role
    )
    return {
        "id": share.id,
        "note_id": note_id,
        "user_target_id": payload.target_user_id,
        "role": share.role,
    }


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def unshare_note(
    note_id: int, target_user_id: int, db: DBSession, current_user: CurrentUser
):
    ShareService(db).unshare_note(current_user.id, note_id, target_user_id)
    return None


@router.post("/labels/{label_id}", status_code=status.HTTP_201_CREATED)
def share_label(
    label_id: int, payload: ShareRequest, db: DBSession, current_user: CurrentUser
):
    share = ShareService(db).share_label(
        current_user.id, label_id, payload.target_user_id, payload.role
    )
    return {
        "id": share.id,
        "label_id": label_id,
        "user_target_id": payload.target_user_id,
        "role": share.role,
    }


@router.delete("/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def unshare_label(
    label_id: int, target_user_id: int, db: DBSession, current_user: CurrentUser
):
    ShareService(db).unshare_label(current_user.id, label_id, target_user_id)
    return None
