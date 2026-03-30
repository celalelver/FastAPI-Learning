from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from openai import OpenAI
from dotenv import load_dotenv
from schemas import AIResponse, Question, TextRequest, SummaryResponse
import os
import models
import schemas

models.Base.metadata.create_all(bind=engine)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/users/{user_id}",
    response_model=schemas.UserSingleResponse,
    status_code=status.HTTP_200_OK
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "status": "success",
        "message": "User fetched successfully",
        "data": db_user
    }


@app.get(
    "/users",
    response_model=schemas.UserListResponse,
    status_code=status.HTTP_200_OK
)
def get_users(db: Session = Depends(get_db)):
    db_user = db.query(models.User).all()

    return {
        "status": "success",
        "message": "Users fetched successfully",
        "data": db_user
    }


@app.post(
    "/users",
    response_model=schemas.UserSingleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "status": "success",
        "message": "User created",
        "data": db_user
    }


@app.put(
    "/users/{user_id}",
    response_model=schemas.UserSingleResponse,
    status_code=status.HTTP_200_OK
)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")

    db_user.name = user.name
    db_user.email = user.email

    db.commit()
    db.refresh(db_user)

    return {
        "status": "success",
        "message": "User updated successfully",
        "data": db_user
    }


@app.post(
    "/summarize",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK
)
def summarize(data: TextRequest):
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": "Summarize the text in 2 sentences."
                },
                {
                    "role": "user",
                    "content": data.text
                }
            ]
        )

        summary = str(response.output_text or "")

        return {
            "status": "success",
            "message": "Summary generated successfully",
            "data": {
                "summary": summary
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Summarize request failed: {str(e)}"
        )


@app.post(
    "/summarize-short",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK
)
def summarize_short(data: TextRequest):
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": "Summarize the text very briefly in 1 short sentence."
                },
                {
                    "role": "user",
                    "content": data.text
                }
            ]
        )

        summary = str(response.output_text or "")

        return {
            "status": "success",
            "message": "Short summary generated successfully",
            "data": {
                "summary": summary
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Short summarize request failed: {str(e)}"
        )


@app.post(
    "/summarize-detailed",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK
)
def summarize_detailed(data: TextRequest):
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": "Summarize the text in a detailed, clear, and well-structured way. Include the important points."
                },
                {
                    "role": "user",
                    "content": data.text
                }
            ]
        )

        summary = str(response.output_text or "")

        return {
            "status": "success",
            "message": "Detailed summary generated successfully",
            "data": {
                "summary": summary
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Detailed summarize request failed: {str(e)}"
        )


@app.post(
    "/ask-ai",
    response_model=AIResponse,
    status_code=status.HTTP_200_OK
)
def ask_ai(data: Question):
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": "Türkçe cevap ver."
                },
                {
                    "role": "user",
                    "content": data.question
                }
            ]
        )

        answer = str(response.output_text or "")

        return {
            "status": "success",
            "message": "AI response generated successfully",
            "data": {
                "answer": answer,
                "model": "gpt-4o-mini"
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI request failed: {str(e)}"
        )


@app.delete(
    "/users/{user_id}",
    response_model=schemas.MessageResponse,
    status_code=status.HTTP_200_OK
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="user Not Found")

    db.delete(db_user)
    db.commit()

    return {
        "status": "success",
        "message": "User deleted successfully"
    }
