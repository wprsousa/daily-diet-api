from flask_sqlalchemy import SQLAlchemy

from src.logger import logger

db = SQLAlchemy()
logger.info(f"{db} configurado com sucesso")
