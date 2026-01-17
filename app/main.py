from fastapi import FastAPI
from app.database import engine
from app import models

print("Starting FastAPI application...")

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

print("Importing routers...")

try:
    from app.routers import clients
    print("✓ Clients router imported successfully")
    app.include_router(clients.router, prefix="/clients", tags=["clients"])
    print("✓ Clients router included")
except Exception as e:
    print(f"✗ Error with clients router: {e}")

try:
    from app.routers import auth
    print("✓ Auth router imported successfully")
    app.include_router(auth.router, prefix="/auth", tags=["authentication"])
    print("✓ Auth router included")
except Exception as e:
    print(f"✗ Error with auth router: {e}")
    import traceback
    traceback.print_exc()

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

print("FastAPI application setup complete")