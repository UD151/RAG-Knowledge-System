from fastapi import APIRouter
from app.db.db_manager import (
    create_new_session,
    get_all_sessions,
    get_session_messages,
    delete_session_and_messages
)

router = APIRouter(prefix="/api/sessions")


@router.post("")
def create_session():
    return {"session_id": create_new_session()}


@router.get("")
def list_sessions():
    return get_all_sessions()


@router.get("/{session_id}/messages")
def get_messages(session_id: str):
    return get_session_messages(session_id)


@router.delete("/{session_id}")
def delete_session(session_id: str):
    delete_session_and_messages(session_id)
    return {"msg": "deleted"}