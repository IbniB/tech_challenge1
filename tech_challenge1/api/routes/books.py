from fastapi import APIRouter, HTTPException, Query, Depends
from tech_challenge1.models.book_model import Book
import pandas as pd
import os
from typing import Optional
from tech_challenge1.core.security import get_current_user
from tech_challenge1.models.user import User

router = APIRouter()

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "livros.csv")


def load_books():
    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=404, detail="Arquivo livros.csv não encontrado.")

    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    return df.to_dict(orient="records")


@router.get("", response_model=list[Book])
def get_books(current_user: User = Depends(get_current_user)):
    return load_books()

@router.get("/search", response_model=list[Book])
def search_books(
    title: Optional[str] = Query(None, description="Parte do título"),
    category: Optional[str] = Query(None, description="Nome da categoria")
):
    books = load_books()

    results = books
    if title:
        results = [b for b in results if title.lower() in b["title"].lower()]
    if category:
        results = [b for b in results if category.lower() in b["category"].lower()]
    return results

@router.get("/{book_id}", response_model=Book)
def get_book_by_id(book_id: int):
    books = load_books()
    if book_id < 0 or book_id >= len(books):
        raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado.")
    return books[book_id]


@router.get("/categories", response_model=list[str])
def get_categories():
    books = load_books()
    categories = sorted(set(b["category"] for b in books))
    return categories
