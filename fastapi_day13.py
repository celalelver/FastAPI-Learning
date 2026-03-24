from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class NoteCreate(BaseModel):
    title: str
    content: str

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.put('/users/{user_id}')
def update_user(user_id: int, user:UserCreate, db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code = 404, detail = 'User Not Found')

    db_user.name = user.name
    db_user.email = user.email

    db.commit()
    db.refresh(db_user)

    return db_user

@app.post('/users/{user_id}')
def delete_user(user_id:int,db:Session=Depends(get_db)):
    
    db_user = db.query(models.User).filter(models.User.id == user_id).first()


    if not db_user:
        raise HTTPException(status_code = 404,detail = 'user Not Found')
    
    db.delete(db_user)
    db.commit()

    return {"message": "User deleted"}
