from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models
from app.schemas import BookCreate, BookOut
from app.deps import require_admin

from fastapi.responses import StreamingResponse
import csv
from io import StringIO

router = APIRouter(prefix="/books", tags=["Books"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[BookOut])
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


# ✅ export ДОЛЖЕН БЫТЬ ВЫШЕ чем /{book_id}
@router.get("/export/csv", dependencies=[Depends(require_admin)])
def export_books_csv(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "title"])

    for b in books:
        writer.writerow([b.id, b.title])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=books.csv"},
    )


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookOut)
def create_book(
    data: BookCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    book = models.Book(title=data.title)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"status": "deleted"}
