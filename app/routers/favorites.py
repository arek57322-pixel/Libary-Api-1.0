from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app import models

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.get("/")
def get_my_favorites(
    user: models.User = Depends(get_current_user),
):
    return [{"id": b.id, "title": b.title} for b in user.favorites]


@router.post("/{book_id}")
def add_favorite(
    book_id: int,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book in user.favorites:
        return {"status": "already in favorites"}

    user.favorites.append(book)
    db.commit()

    return {"status": "added"}


@router.delete("/{book_id}")
def remove_favorite(
    book_id: int,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book not in user.favorites:
        return {"status": "not in favorites"}

    user.favorites.remove(book)
    db.commit()

    return {"status": "removed"}
