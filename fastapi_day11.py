from fastapi import FastAPI
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
from pydantic import BaseModel , EmailStr

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name: str
    email: EmailStr

@app.get('/')
def say_hello(name: str):
    return {'message': f'Hello {name}'}

@app.post('/users')
def create_user(user: UserCreate):
    db: Session = SessionLocal()

    db_user = models.User(
        name=user.name,
        email=user.email
    )

    db.add(db_user)
    db.commit()

    return {'message': 'user added'}
