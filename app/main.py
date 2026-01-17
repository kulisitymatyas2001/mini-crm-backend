from fastapi import FastAPI
from app.routers import clients

app = FastAPI()

app.include_router(clients.router, prefix="/clients", tags=["clients"])

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}