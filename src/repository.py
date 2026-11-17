
from database import get_connection
from decimal import Decimal

def to_cents(value):
    return int(Decimal(str(value)) * 100)

def insert_products(products):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        for product in products:
            cursor.execute("""
                INSERT OR IGNORE INTO produtos (nome)
                VALUES (?)
            """, (product,))

        connection.commit()

    finally:
        connection.close()



def get_products():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, nome
            FROM produtos
            ORDER BY id
        """)

        return cursor.fetchall()

    finally:
        connection.close()




def insert_sales(sales):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        for sale in sales:
            cursor.execute("""
                SELECT id
                FROM produtos
                WHERE nome = ?
            """, (sale["produto"],))

            product = cursor.fetchone()

            if product is None:
                raise ValueError(
                    f"Produto não encontrado: {sale['produto']}"
                )

            product_id = product[0]

            unit_price_cents = to_cents(sale["preco_unitario"])
            total_cents = to_cents(sale["valor_total"])

            cursor.execute("""
                INSERT OR IGNORE INTO vendas (
                    data,
                    produto_id,
                    quantidade,
                    preco_unitario_centavos,
                    valor_total_centavos
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                sale["data"],
                product_id,
                sale["quantidade"],
                unit_price_cents,
                total_cents
            ))

        connection.commit()

    finally:
        connection.close()




def get_sales():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                vendas.id,
                vendas.data,
                produtos.nome,
                vendas.quantidade,
                vendas.preco_unitario_centavos,
                vendas.valor_total_centavos
            FROM vendas
            INNER JOIN produtos
                ON vendas.produto_id = produtos.id
            ORDER BY vendas.data
        """)

        return cursor.fetchall()

    finally:
        connection.close()


def sync_products(sales):
    products = {
        sale["produto"]
        for sale in sales
    }

    insert_products(sorted(products))



def get_table_counts():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM produtos")
        product_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM vendas")
        sales_count = cursor.fetchone()[0]

        return product_count, sales_count

    finally:
        connection.close()
