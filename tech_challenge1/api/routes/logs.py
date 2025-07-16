from fastapi import APIRouter, HTTPException
from pathlib import Path
from datetime import date

router = APIRouter(tags=["Logs"])

@router.get("/")
def read_logs():
    # usa o arquivo do dia atual; ajuste o nome se você girar arquivos diferentes
    log_path = Path("logs") / f"app_{date.today().isoformat()}.log"
    if not log_path.exists():
        raise HTTPException(404, "Log não encontrado")
    # lê as últimas 200 linhas
    lines = log_path.read_text(encoding="utf-8").splitlines()[-200:]
    return {"logs": lines}
