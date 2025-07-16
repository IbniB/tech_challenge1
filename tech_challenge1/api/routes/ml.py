from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any
from tech_challenge1.core.security import get_current_user

router = APIRouter()

class PredictionInput(BaseModel):
    price: float
    rating: float
    category: str
    availability: int

@router.get("/features")
async def get_features(current_user: str = Depends(get_current_user)) -> Dict[str, List[str]]:
    """
    Retorna as features disponíveis para modelos de ML.
    """
    return {"features": ["price", "rating", "category", "availability"]}

@router.get("/training-data")
async def get_training_data(current_user: str = Depends(get_current_user)) -> Dict[str, List[Dict[str, Any]]]:
    """
    Retorna dados simulados para treinamento de modelos ML.
    """
    return {
        "data": [
            {"price": 10.99, "rating": 4.5, "category": "Sci-fi", "availability": 1},
            {"price": 20.50, "rating": 3.8, "category": "Romance", "availability": 0},
            {"price": 15.75, "rating": 4.2, "category": "Drama", "availability": 1}
        ]
    }

@router.post("/predictions")
async def post_predictions(
    payload: PredictionInput,
    current_user: str = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Recebe dados de entrada e retorna uma predição simulada.
    """
    if payload.rating > 4 and payload.availability == 1:
        return {"prediction": "high-demand"}
    return {"prediction": "low-demand"}