from fastapi import APIRouter, Query, HTTPException, Depends
import pandas as pd
import os
from tech_challenge1.core.security import get_current_user
from tech_challenge1.models.user import User

router = APIRouter(prefix="/api/v1", tags=["Stats"])

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "livros.csv")

def load_df():
    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=404, detail="CSV não encontrado.")
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    df["numeric_price"] = df["price"].str.replace("£", "").astype(float)
    return df

@router.get("/stats/overview")
def stats_overview(current_user: User=Depends(get_current_user)):
    df = load_df()
    total = len(df)
    avg_price = round(df["numeric_price"].mean(), 2)
    rating_dist = df["rating"].value_counts().to_dict()
    return {
        "total_books": total,
        "average_price": avg_price,
        "ratings_distribution": rating_dist
    }

@router.get("/stats/categories")
def stats_by_category():
    df = load_df()
    grouped = df.groupby("category").agg(
        count=("title", "count"),
        avg_price=("numeric_price", "mean")
    ).round(2).reset_index()
    return grouped.to_dict(orient="records")

@router.get("/stats/top-rated")
def top_rated_books():
    df = load_df()
    # Rating textual para ranking
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    df["rating_score"] = df["rating"].map(rating_map)
    top_rating = df["rating_score"].max()
    top_books = df[df["rating_score"] == top_rating]
    return top_books.drop(columns=["rating_score", "numeric_price"]).to_dict(orient="records")

@router.get("/stats/price-range")
def books_in_price_range(min: float = Query(0), max: float = Query(1000)):
    df = load_df()
    filtered = df[(df["numeric_price"] >= min) & (df["numeric_price"] <= max)]
    return filtered.drop(columns=["numeric_price"]).to_dict(orient="records")
