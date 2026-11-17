
from database import get_connection


def revenue_by_product():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                produtos.nome,
                SUM(vendas.valor_total_centavos) / 100.0 AS faturamento
            FROM vendas
            INNER JOIN produtos
                ON vendas.produto_id = produtos.id
            GROUP BY produtos.id, produtos.nome
            ORDER BY faturamento DESC
        """)

        return cursor.fetchall()

    finally:
        connection.close()


def units_sold_by_product():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                produtos.nome,
                SUM(vendas.quantidade) AS unidades_vendidas
            FROM vendas
            INNER JOIN produtos
                ON vendas.produto_id = produtos.id
            GROUP BY produtos.id, produtos.nome
            ORDER BY unidades_vendidas DESC
        """)

        return cursor.fetchall()

    finally:
        connection.close()


def monthly_revenue():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                strftime('%Y-%m', data) AS mes,
                SUM(valor_total_centavos) / 100.0 AS faturamento
            FROM vendas
            GROUP BY mes
            ORDER BY mes
        """)

        return cursor.fetchall()

    finally:
        connection.close()


def best_revenue_product():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                produtos.nome,
                SUM(vendas.valor_total_centavos) / 100.0 AS faturamento
            FROM vendas
            INNER JOIN produtos
                ON vendas.produto_id = produtos.id
            GROUP BY produtos.id, produtos.nome
            ORDER BY faturamento DESC
            LIMIT 1
        """)

        return cursor.fetchone()

    finally:
        connection.close()


def revenue_share_by_product():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                produtos.nome,
                SUM(vendas.valor_total_centavos) / 100.0 AS faturamento,
                ROUND(
                    SUM(vendas.valor_total_centavos) * 100.0 /
                    (SELECT SUM(valor_total_centavos) FROM vendas),
                    2
                ) AS participacao_percentual
            FROM vendas
            INNER JOIN produtos
                ON vendas.produto_id = produtos.id
            GROUP BY produtos.id, produtos.nome
            ORDER BY faturamento DESC
        """)

        return cursor.fetchall()

    finally:
        connection.close()


def general_metrics():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) AS quantidade_vendas,
                COALESCE(SUM(quantidade), 0) AS unidades_vendidas,
                COALESCE(SUM(valor_total_centavos), 0) AS faturamento_centavos,
                COALESCE(
                    AVG(valor_total_centavos),
                    0
                ) / 100.0 AS ticket_medio
            FROM vendas
        """)

        sales_count, units, revenue_cents, average_ticket = cursor.fetchone()

        cursor.execute("""
            SELECT COUNT(*)
            FROM produtos
        """)

        product_count = cursor.fetchone()[0]

        return {
            "quantidade_vendas": sales_count,
            "produtos_cadastrados": product_count,
            "unidades_vendidas": units,
            "faturamento_total": revenue_cents / 100,
            "ticket_medio": round(average_ticket, 2)
        }

    finally:
        connection.close()
       


if __name__ == "__main__":
    print("\nFaturamento por produto")
    print("-" * 40)
    for product, revenue in revenue_by_product():
        print(f"{product}: R$ {revenue:.2f}")

    print("\nUnidades vendidas por produto")
    print("-" * 40)
    for product, quantity in units_sold_by_product():
        print(f"{product}: {quantity}")

    print("\nFaturamento mensal")
    print("-" * 40)
    for month, revenue in monthly_revenue():
        print(f"{month}: R$ {revenue:.2f}")

    print("\nProduto com maior faturamento")
    print("-" * 40)
    result = best_revenue_product()

    if result:
        product, revenue = result
        print(f"{product}: R$ {revenue:.2f}")
    else:
        print("Nenhuma venda cadastrada.")

    print("\nParticipação no faturamento")
    print("-" * 40)
    for product, revenue, share in revenue_share_by_product():
        print(f"{product}: {share:.2f}% (R$ {revenue:.2f})")
