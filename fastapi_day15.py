from fastapi import FastAPI, Depends , status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
from database import SessionLocal, engine
from openai import OpenAI
from schemas import Question
import os
import models 
import schemas

models.Base.metadata.create_all(bind=engine)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/{user_id}",
         response_model=schemas.UserSingleResponse,
         status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404,detail = 'User not found')
    return {
        "status": "success",
        "message": "User fetched successfully",
        "data": db_user
    }

@app.get("/users",
         response_model = schemas.UserListResponse,
         status_code = status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    db_user = db.query(models.User).all()

    return {
        "status": "success",
        "message": "Users fetched successfully",
        "data": db_user
    }

@app.post("/users",
          response_model=schemas.UserSingleResponse,
          status_code = status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "status": "success",
        "message": "User created",
        "data" : db_user
    }

@app.put('/users/{user_id}',
         response_model=schemas.UserSingleResponse,
         status_code = status.HTTP_200_OK)
def update_user(user_id: int, user:schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code = 404, detail = 'User Not Found')

    db_user.name = user.name
    db_user.email = user.email

    db.commit()
    db.refresh(db_user)

    return {
    "status": "success",
    "message": "User updated successfully",
    "data": db_user
    }

@app.post("/ask-ai")
def ask_ai(data: Question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": data.question}
        ]
    )

    return {
        "answer": response.choices[0].message.content
    }

@app.delete('/users/{user_id}',
            response_model = schemas.MessageResponse,
            status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int,db:Session=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()


    if not db_user:
        raise HTTPException(status_code = 404,detail = 'user Not Found')
    
    db.delete(db_user)
    db.commit()
