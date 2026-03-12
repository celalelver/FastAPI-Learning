from datetime import datetime
from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/")
def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/square")
def square(number: int):
    return {"result": number * number}

@app.get("/add")
def add_numbers(a: int, b: int):
    return {"result": a + b}

@app.get("/time")
def get_time():
    return {"time": datetime.now().isoformat()}

@app.get("/random-number")
def generate_random_number():
    return {"number": random.randint(1, 999)}
