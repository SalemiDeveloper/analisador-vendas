
import json
from pathlib import Path

from analytics import (
    general_metrics,
    revenue_by_product,
    units_sold_by_product,
    monthly_revenue,
    best_revenue_product,
    revenue_share_by_product
)


PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "relatorio_analitico.json"


def generate_analytics_report():
    best_product = best_revenue_product()

    report = {
        "indicadores_gerai": general_metrics(),
        "faturamento_por_produto": [
            {
                "produto": product,
                "faturamento": round(revenue, 2)
            }
            for product, revenue in revenue_by_product()
        ],
        "unidades_por_produto": [
            {
                "produto": product,
                "unidades_vendidas": quantity
            }
            for product, quantity in units_sold_by_product()
        ],
        "faturamento_mensal": [
            {
                "mes": month,
                "faturamento": round(revenue, 2)
            }
            for month, revenue in monthly_revenue()
        ],
        "produto_maior_faturamento": {
            "produto": best_product[0],
            "faturamento": round(best_product[1], 2)
        },
        "participacao_por_produto": [
            {
                "produto": product,
                "faturamento": round(revenue, 2),
                "participacao_percentual": share
            }
            for product, revenue, share in revenue_share_by_product()
        ]
    }

    return report


def main():
    report = generate_analytics_report()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=4)

    print("Relatório analítico gerado com sucesso!")
    print(f"Arquivo: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
