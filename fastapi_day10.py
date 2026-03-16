from pydantic import BaseModel , EmailStr , Field
from typing import List
from fastapi import FastAPI

class User(BaseModel):
    name : str
    email : EmailStr

app = FastAPI()

@app.get('/')
def home():
    return {'message' : 'Hello'}

@app.post('/users')

def create_user(user:User):
    return {
        "status": "success",
        "user": user
    }
------------------------------------------------------------

app = FastAPI()
class Person(BaseModel):
    name : str
    age : int = Field(gt = 0 , lt = 120)

app.get('/')
def home():
    return {'message' : 'Hello World'}

app.post('/person')

def create_person(person : Person):
    return person
  ----------------------------------------------------
app = FastAPI()
class Product(BaseModel):
    name: str
    price: float

@app.post("/product")
def create_product(product: Product):
    return product
----------------------------------------------------
app = FastAPI()
class Items(BaseModel):
    items: list[str]
@app.post("/items")
def count_items(data: Items):
    return {"count": len(data.items)}
-----------------------------------------------------
