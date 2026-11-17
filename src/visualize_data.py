
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path

from analytics import revenue_by_product, monthly_revenue


PROJECT_DIR = Path(__file__).resolve().parent.parent
CHARTS_DIR = PROJECT_DIR / "data" / "processed" / "charts"


def plot_revenue_by_product():
    results = revenue_by_product()

    products = [item[0] for item in results]
    revenues = [item[1] for item in results]

    plt.figure(figsize=(10, 6))
    plt.bar(products, revenues)

    plt.title("Faturamento por Produto")
    plt.xlabel("Produto")
    plt.ylabel("Faturamento (R$)")
    plt.grid(axis="y", alpha=0.3)

    for index, revenue in enumerate(revenues):
        plt.text(index, revenue, f"R$ {revenue:.2f}", ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "faturamento_por_produto.png", dpi=150)
    plt.close()


def plot_monthly_revenue():
    results = monthly_revenue()

    months = [item[0] for item in results]
    revenues = [item[1] for item in results]

    plt.figure(figsize=(10, 6))
    plt.plot(months, revenues, marker="o")

    plt.title("Evolução do Faturamento Mensal")
    plt.xlabel("Mês")
    plt.ylabel("Faturamento (R$)")
    plt.grid(True, alpha=0.3)

    for month, revenue in zip(months, revenues):
        plt.annotate(
            f"R$ {revenue:.2f}",
            (month, revenue),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center"
        )

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "faturamento_mensal.png", dpi=150)
    plt.close()


def generate_charts():
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    plot_revenue_by_product()
    plot_monthly_revenue()

    print("Gráficos gerados com sucesso!")
    print(f"Diretório: {CHARTS_DIR}")


if __name__ == "__main__":
    generate_charts()
