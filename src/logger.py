# loggin.INFO     - Registra acontecimentos normais
# logging.warning - Registra situações que merecem atenção
# logging.ERROR   - Registra erros
# FileHandler     - Salva logs em arquivos
# StreamHandler   - Exibe os logs no terminal
# basicConfig     - Configura o sistema de logging 


import logging
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_DIR / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"


def setup_logger():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )

    return logging.getLogger("sales_pipeline")