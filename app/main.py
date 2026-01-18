from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import clients, auth
from app.database import engine
from app import models

# Adatbázis táblák létrehozása
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware hozzáadása - FONTOS mobilhoz!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Minden origin engedélyezése (development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerek
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}