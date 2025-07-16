from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, format="{time} | {level} | {message}", level="INFO")

logger.add(
  "logs/app_{time:YYYY-MM-DD}.log",
  rotation="00:00",
  retention="7 days",
  level="INFO",
  format="{time} | {level} | {message}"
)