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

# single-use codes
@app.get("/code-single/{code}")
async def check_code(code: str):
    if db.check_code_exists(code):
        db.delete_code(code)
        return {"message": f"True"}
    else:
        return {"message": f"False"}
    
# multi-use codes
@app.get("/code-multi/{code}/{user_id}")
async def check_code_event(code: str, user_id):
    if db.is_code_valid(code, user_id):
        return {"message": f"True"}
    else:
        return {"message": f"False"}

@app.get("/rewrite_db")
async def rewrite_db():
    db.add_codes_from_csv("codes.csv")
    return {"message": f"Succesfully rewritten db"}


