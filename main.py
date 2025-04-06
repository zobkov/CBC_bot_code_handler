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
    validation_result = db.is_code_valid(code, user_id)
    if validation_result == "valid":
        return {"message": "Valid"}
    elif validation_result == "expired":
        return {"message": "Expired"}
    else:
        return {"message": "Invalid"}

@app.get("/rewrite_db")
async def rewrite_db():
    db.add_codes_from_csv("codes.csv")
    return {"message": f"Succesfully rewritten db"}


