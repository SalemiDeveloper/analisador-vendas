
import csv
from pathlib import Path
from logger import setup_logger

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "raw" / "vendas.csv"


def extract_sales():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo de vendas não encontrado: {INPUT_FILE}"
        )

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=",") # lendo cada linha do CSV e transformando em dicionário.
        records = list(reader)

    if not records:
        raise ValueError("O arquivo de vendas está vazio.")

    return records


def main():
    logger = setup_logger()

    logger.info("Iniciando extração de vendas.")

    try:
        records = extract_sales()
        logger.info("Extração concluída. Registros extraídos: %d", len(records))

    except(FileNotFoundError, ValueError) as error:
        logger.error("Falha na extração: %s", error)
        return


if __name__ == "__main__":
    main()
