from fastapi import APIRouter, HTTPException, Query
from tech_challenge1.utils.logging import get_log_lines

router = APIRouter(tags=["Logs"])

@router.get("/")
def read_logs(limit: int = Query(200, ge=1, le=2000)):
    """
    Retorna as últimas `limit` linhas de log do buffer em memória.
    Compatível com Render (stdout/stderr), sem uso de arquivos.
    """
    logs = get_log_lines(limit)
    if not logs:
        # Pode ocorrer logo após o start, antes de qualquer log
        raise HTTPException(status_code=404, detail="Nenhum log disponível no buffer")
    return {"logs": logs}
