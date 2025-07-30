from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from tech_challenge1.core.security import get_current_user
from tech_challenge1.models.user import User
from tech_challenge1.scripts.scrape import scrape_all_books
import pandas as pd
import os
from pathlib import Path

router = APIRouter()


def write_csv(books_data: list[dict]) -> None:
    """
    Grava a lista de livros em data/livros.csv no projeto.
    """
    df = pd.DataFrame(books_data)
    df.insert(0, "id", range(len(df)))

    # Calcular caminho absoluto de <project_root>/data
    project_root = Path(__file__).resolve().parent.parent.parent
    output_dir = project_root / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "livros.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")


@router.post("/trigger")
def trigger_scraping(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """
    Dispara o scraping de livros em background e retorna imediatamente.
    """
    try:
        # Adiciona a tarefa em background
        background_tasks.add_task(
            write_csv,
            scrape_all_books(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao iniciar o scraping: {e}"
        )
    return {"msg": "Scraping disparado com sucesso. Verifique data/livros.csv em instantes."}
