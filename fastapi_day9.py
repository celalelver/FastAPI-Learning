from pydantic import BaseModel
from fastapi import FastAPI
from typing import List
class User(BaseModel):
    name:str
    email:str

app = FastAPI()

@app.get('/')
def home():
    return {'message': 'Hello'}

@app.post('/users')
def create_user(user:User):
    return user 

class Login(BaseModel):
    email:str
    password:str
----------------------------------------
app = FastAPI()

@app.post('/login')
def login(data:Login):
    if data.email == 'admin@mail.com' and data.password == '1234':
        return {'Message':'Login Successful'}
    
    return {'Message': 'İnvalid Credentials'} 
---------------------------------------
app = FastAPI()

class Age(BaseModel):
    age : int

@app.post('/dayAGE')

def calculate_age(data:Age):
    return {'age_next_year' : data.age + 1} 
---------------------------------------
app = FastAPI()

class Itemlist(BaseModel):
    items : List[str]

@app.post('/items')
def count_items(data:Itemlist):
    return {'item_count' : len(data.items)}
---------------------------------------
