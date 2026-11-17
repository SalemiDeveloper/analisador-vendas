
import csv
from pathlib import Path

from repository import get_connection, to_cents


PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "processed" / "vendas.csv"


def get_source_totals():
    with open(INPUT_FILE, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        sales = list(reader)

    return {
        "vendas": len(sales),
        "produtos": len({sale["produto"] for sale in sales}),
        "unidades": sum(int(sale["quantidade"]) for sale in sales),
        "faturamento_centavos": sum(
            to_cents(sale["valor_total"]) for sale in sales
        )
    }


def get_database_totals():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(quantidade), 0),
                COALESCE(SUM(valor_total_centavos), 0)
            FROM vendas
        """)

        sales_count, units, revenue = cursor.fetchone()

        cursor.execute("""
            SELECT COUNT(*)
            FROM produtos
        """)

        product_count = cursor.fetchone()[0]

        return {
            "vendas": sales_count,
            "produtos": product_count,
            "unidades": units,
            "faturamento_centavos": revenue
        }

    finally:
        connection.close()


def check_integrity():
    source = get_source_totals()
    database = get_database_totals()

    print("\nVerificação de integridade dos dados")
    print("-" * 45)

    for metric in source:
        expected = source[metric]
        actual = database[metric]

        status = "OK" if expected == actual else "DIVERGÊNCIA"

        print(f"{metric}: {status} (CSV: {expected} | SQLite: {actual})")

    if source != database:
        raise ValueError("Foram encontradas divergências nos dados.")

    print("\nIntegridade dos dados confirmada!")


if __name__ == "__main__":
    check_integrity()
