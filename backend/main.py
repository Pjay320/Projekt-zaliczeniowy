from fastapi import FastAPI

app = FastAPI(title="NBP Currency API")

@app.get("/")
def read_root():
    return {"message": "Backend API dziala!"}