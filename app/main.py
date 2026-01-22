from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.routers import auth, users, books, favorites

app = FastAPI(title="Online Library API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(favorites.router)


@app.get("/")
def root():
    return {"message": "Library API is working"}


@app.get("/db-test")
def db_test():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
    return {"db": "ok", "result": result}
