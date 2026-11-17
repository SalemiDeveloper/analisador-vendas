
import csv
from pathlib import Path

from repository import sync_products, insert_sales, get_table_counts
from logger import setup_logger



PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "processed" / "vendas.csv"


def load_sales():
    logger = setup_logger()

    logger.info("Iniciando carga dos dados no SQLite.")

    try:
        with open(INPUT_FILE, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            sales = list(reader)

        if not sales:
            raise ValueError("Não existem vendas para carregar.")

        for sale in sales:
            sale["quantidade"] = int(sale["quantidade"])

        sync_products(sales)
        insert_sales(sales)

        product_count, sales_count = get_table_counts()

        logger.info("Produtos cadastrados no banco: %d", product_count)
        logger.info("Total de vendas no banco: %d", sales_count)

        logger.info(
            "Carga concluída. Vendas processadas: %d",
            len(sales)
        )

    except (OSError, ValueError, KeyError) as error:
        logger.error("Falha na carga dos dados: %s", error)
        raise


if __name__ == "__main__":
    load_sales()
    print("Carga no SQLite realizada com sucesso!")
