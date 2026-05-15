from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user, get_db
from app.models.application import Application
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/applications/{application_id}/notes", response_model=NoteResponse)
def create_note(application_id: int, note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  
  application = db.query(Application).filter(Application.id == application_id, Application.user_id == current_user.id).first()

  if not application:
    raise HTTPException(status_code=404, detail="Application not found")

  db_note = Note(application_id=application_id, content=note.content)

  db.add(db_note)
  db.commit()
  db.refresh(db_note)
  return db_note

@router.get("/applications/{application_id/notes", response_model=list[NoteResponse])
def get_notes(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  application = db.query(Application).filter(Application.id == application_id, Application.user_id == current_user.id).first()

  if not application:
    raise HTTPException(status_code=404, detail="Application not found")
  
  return db.query(Note).filter(Note.application == application_id).all()

@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  note = db.query(Note).join(Application).filter(Note.id == note_id, Application.user_id == current_user.id).first()

  if not note:
    raise HTTPException(status_code=404, detail="Note not found")

  if note_update.content is not None:
    note.content = note_update.content

  db.commit()
  db.refresh(note)

  return note

@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  note = db.query(Note).join(Application).filter(Note.id == note_id, Application.user_id == current_user.id).first()

  if not note:
    raise HTTPException(status_code=404, detail="Note not found")

  db.delete(note)
  db.commit()

  return {"message": "Note deleted"}