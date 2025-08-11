import logging
import sys
from collections import deque
from typing import List


class LogBufferHandler(logging.Handler):
    """
    Handler que mantém um buffer circular (ring buffer) das últimas N mensagens.
    Útil para expor logs via endpoint sem depender de arquivos.
    """
    def __init__(self, maxlen: int = 5000):
        super().__init__()
        self._buffer = deque(maxlen=maxlen)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self._buffer.append(msg)
        except Exception:  # noqa: BLE001
            self.handleError(record)

    def tail(self, n: int = 200) -> List[str]:
        if n <= 0:
            return []
        return list(self._buffer)[-n:]


# Singleton do buffer de logs
log_buffer_handler = LogBufferHandler(maxlen=5000)


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configura logging para stdout e anexa o buffer em memória.
    Chame isso no startup da aplicação (ex.: api/main.py), antes de criar a app.
    """
    root = logging.getLogger()
    root.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    # Stream para stdout (Render consome isso automaticamente)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Evita duplicar handlers em hot reload
    existing_types = {type(h) for h in root.handlers}
    if logging.StreamHandler not in existing_types:
        root.addHandler(stream_handler)

    # Buffer em memória
    log_buffer_handler.setFormatter(formatter)
    if LogBufferHandler not in existing_types:
        root.addHandler(log_buffer_handler)

    # Garanta que loggers do uvicorn/fastapi também alimentem o buffer
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        lg = logging.getLogger(name)
        lg.setLevel(level)
        if not any(isinstance(h, LogBufferHandler) for h in lg.handlers):
            lg.addHandler(log_buffer_handler)


def get_log_lines(last: int = 200) -> List[str]:
    """
    Retorna as últimas N linhas de log do buffer.
    """
    return log_buffer_handler.tail(last)
