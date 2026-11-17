
from database import get_connection


def create_tables():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        """)

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario_centavos INTEGER NOT NULL,
                valor_total_centavos INTEGER NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos(id),
                UNIQUE (
                    data,
                    produto_id,
                    quantidade,
                    preco_unitario_centavos,
                    valor_total_centavos
                )
            )
        """)


        connection.commit()

    finally:
        connection.close()


def list_tables():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)

        tables = cursor.fetchall()

        for table in tables:
            print(table[0])

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()
    print("Tabelas criadas com sucesso!")

    print("\nTabelas disponíveis:")
    list_tables()
