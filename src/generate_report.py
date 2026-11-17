
import csv
import json
from collections import defaultdict
from pathlib import Path
from logger import setup_logger
import sys

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "processed" / "vendas.csv"
OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "relatorio.json"


def calculate_monthly_revenue(records):
    monthly_revenue = defaultdict(float)

    for record in records:
        month = record["data"][:7]

        monthly_revenue[month] += float(record["valor_total"])

    return {
        month: round(revenue, 2)
        for month, revenue in sorted(monthly_revenue.items())
    }



def calculate_monthly_variation(monthly_revenue):
    months = sorted(monthly_revenue)

    if len(months) < 2:
        return None

    previous_month = monthly_revenue[months[-2]]
    current_month = monthly_revenue[months[-1]]

    if previous_month == 0:
        return None

    variation = (
        (current_month - previous_month) / previous_month
    ) * 100

    return round(variation, 2)



def generate_report(records):
    total_revenue = sum(
        float(record["valor_total"]) for record in records
    )

    total_sales = len(records)

    total_units = sum(
        int(record["quantidade"]) for record in records
    )

    average_ticket = total_revenue / total_sales

    product_quantities = defaultdict(int)

    for record in records:
        product_quantities[record["produto"]] += int(
            record["quantidade"]
        )

    best_selling_product = max(
        product_quantities,
        key=product_quantities.get
    )

    monthly_revenue = calculate_monthly_revenue(records)
    monthly_variation = calculate_monthly_variation(monthly_revenue)

    return {
        "faturamento_total": round(total_revenue, 2),
        "quantidade_vendas": total_sales,
        "unidades_vendidas": total_units,
        "ticket_medio": round(average_ticket, 2),
        "produto_mais_vendido": best_selling_product,
        "quantidade_produto_mais_vendido": (
            product_quantities[best_selling_product]
        ),
        "faturamento_mensal": monthly_revenue,
        "variacao_fat_mensal_percentual": monthly_variation,
    }



def main():
    logger = setup_logger()

    logger.info("Iniciando geração do relatório.")

    if not INPUT_FILE.exists():
        logger.error(
            "Arquivo vendas.csv não encontrado: %s",
            INPUT_FILE
        )
        sys.exit(1)

    try:
        with INPUT_FILE.open(
            "r", newline="", encoding="utf-8"
        ) as file:
            records = list(csv.DictReader(file))

        if not records:
            logger.warning(
                "Não existem vendas válidas para gerar o relatório."
            )
            return

        report = generate_report(records)

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        OUTPUT_FILE.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    except (OSError, ValueError, KeyError) as error:
        logger.error("Falha na geração do relatório: %s", error)
        return

    logger.info("Relatório gerado com sucesso.")
    logger.info("Indicadores calculados para %d vendas.", len(records))
    logger.info("Arquivo gerado: %s", OUTPUT_FILE)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\nRelatório salvo em: {OUTPUT_FILE}")




if __name__ == "__main__":
    main()
