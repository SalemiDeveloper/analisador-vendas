# subprocess.run() - executa outro programa ou script Python
# sys.executable   - utiliza o mesmo interpretador Python que está executando o orquestrador.
# check=True       - gera uma exceção caso um script termine com código de erro 
# PIPELINE_STEPS   - define a ordem de execução das etapas


import subprocess
import sys
from pathlib import Path

from logger import setup_logger

PROJECT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_DIR / "src"

PIPELINE_STEPS = [
    "extract_sales.py",
    "validate_sales.py",
    "transform_sales.py",
    "load_database.py",
    "integrity_check.py",
    "generate_report.py",
    "generate_analytics_report.py",
    "visualize_data.py"
]


def main():
    logger = setup_logger()

    logger.info("====================================")
    logger.info("Iniciando execução do pipeline.")
    logger.info("====================================")

    try:
        for step in PIPELINE_STEPS:
            logger.info("Executando etapa: %s", step)

            subprocess.run(
                [sys.executable, str(SRC_DIR / step)],
                cwd=PROJECT_DIR,
                check=True,
            )

            logger.info("Etapa concluída: %s", step)

    except subprocess.CalledProcessError as error:
        logger.error(
            "Pipeline interrompido. Falha na etapa: %s",
            error.cmd[-1],
        )
        return

    logger.info("====================================")
    logger.info("Pipeline executado com sucesso.")
    logger.info("====================================")


if __name__ == "__main__":
    main()
