from fastapi import FastAPI

app = FastAPI()
"test commit"
@app.get("/")
def root():
    return {"message": "Hello FastAPI"}