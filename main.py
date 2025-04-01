from fastapi import FastAPI
from database import Database

app = FastAPI()

db = Database()

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Привет, {name}!"}


@app.get("/code/{code}")
async def check_code(code: str):
    if db.check_code_exists(code):
        db.delete_code(code)
        return {"message": f"True"}
    else:
        return {"message": f"False"}

