
import csv
import json
from pathlib import Path
from logger import setup_logger
from extract_sales import extract_sales
from validation import validate_records
import sys

PROJECT_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "vendas.csv"
REJECTED_FILE = PROJECT_DIR / "data" / "processed" / "rejected_sales.json"


def transform_sales(records):
    return sorted(
        records,
        key=lambda record: (record["data"], record["produto"])
    )



def main():
    logger = setup_logger()

    logger.info("Iniciando transformação das vendas.")

    try:
        records = extract_sales()
        valid_records, rejected_records = validate_records(records)

        processed_records = transform_sales(valid_records)

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        with OUTPUT_FILE.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "data",
                    "produto",
                    "quantidade",
                    "preco_unitario",
                    "valor_total",
                ],
            )

            writer.writeheader()
            writer.writerows(processed_records)

        REJECTED_FILE.write_text(
            json.dumps(
                rejected_records,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8",
        )

    except (FileNotFoundError, ValueError, OSError) as error:
        logger.error("Falha na transformação: %s", error)
        sys.exit(1)

    logger.info("Registros recebidos: %d", len(records))
    logger.info("Registros transformados: %d", len(processed_records))
    logger.warning("Registros rejeitados: %d", len(rejected_records))

    logger.info("Arquivo processado: %s", OUTPUT_FILE)
    logger.info("Arquivo de rejeitados: %s", REJECTED_FILE)

    print(f"Registros recebidos: {len(records)}")
    print(f"Registros processados: {len(processed_records)}")
    print(f"Registros rejeitados: {len(rejected_records)}")
    print(f"Arquivo processado: {OUTPUT_FILE}")
    print(f"Arquivo de rejeitados: {REJECTED_FILE}")



if __name__ == "__main__":
    main()
