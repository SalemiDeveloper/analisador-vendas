
from extract_sales import extract_sales
from validation import validate_records
from logger import setup_logger
import sys



def main():
    logger = setup_logger()

    logger.info("Iniciando validação das vendas.")

    try:
        records = extract_sales()
        valid_records, rejected_records = validate_records(records)

    except (FileNotFoundError, ValueError) as error:
        logger.error("Falha na validação: %s", error)
        sys.exit(1)

    logger.info("Registros recebidos: %d", len(records))
    logger.info("Registros válidos: %d", len(valid_records))
    logger.warning("Registros rejeitados: %d", len(rejected_records))

    print("\nResultado da validação")
    print("----------------------")
    print(f"Registros recebidos: {len(records)}")
    print(f"Registros válidos: {len(valid_records)}")
    print(f"Registros rejeitados: {len(rejected_records)}")

    if rejected_records:
        print("\nRegistros rejeitados:")

        for rejected in rejected_records:
            print(f"\nRegistro {rejected['registro']}")
            print(f"Motivos: {', '.join(rejected['motivo'])}")

if __name__ == "__main__":
    main()
