import logging
import os

# Garante que a pasta de logs exista
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Configura o logger
logger = logging.getLogger("daily_diet")
logger.setLevel(logging.INFO)

# Formato do log
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")

# Handler para arquivo
file_handler = logging.FileHandler(f"{log_dir}/app.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# Handler para console (opcional)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# Adiciona os handlers (evita duplicados)
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)