
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from repository import (
    insert_products,
    get_products,
    insert_sales,
    get_sales,
    sync_products,
    get_table_counts,
    to_cents
)


class TestRepository(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_file = Path(self.temp_dir.name) / "test.db"

        self.connection_patcher = patch(
            "repository.get_connection",
            side_effect=self.create_connection
        )
        self.connection_patcher.start()

        self.create_test_tables()

    def tearDown(self):
        self.connection_patcher.stop()
        self.temp_dir.cleanup()

    def create_connection(self):
        return sqlite3.connect(self.database_file)

    def create_test_tables(self):
        connection = self.create_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE vendas (
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
        connection.close()

    def test_insert_products(self):
        insert_products(["Mouse", "Teclado"])

        products = get_products()

        self.assertEqual(len(products), 2)

    def test_products_do_not_duplicate(self):
        insert_products(["Mouse", "Mouse"])

        products = get_products()

        self.assertEqual(len(products), 1)

    def test_insert_sales(self):
        insert_products(["Mouse"])

        sales = [{
            "data": "2026-10-10",
            "produto": "Mouse",
            "quantidade": 2,
            "preco_unitario": "59.90",
            "valor_total": "119.80"
        }]

        insert_sales(sales)

        registered_sales = get_sales()

        self.assertEqual(len(registered_sales), 1)
        self.assertEqual(registered_sales[0][2], "Mouse")

    def test_sales_do_not_duplicate(self):
        insert_products(["Mouse"])

        sales = [{
            "data": "2026-10-10",
            "produto": "Mouse",
            "quantidade": 2,
            "preco_unitario": "59.90",
            "valor_total": "119.80"
        }]

        insert_sales(sales)
        insert_sales(sales)

        self.assertEqual(len(get_sales()), 1)

    def test_sync_products(self):
        sales = [
            {"produto": "Mouse"},
            {"produto": "Teclado"},
            {"produto": "Mouse"}
        ]

        sync_products(sales)

        self.assertEqual(len(get_products()), 2)

    def test_table_counts(self):
        insert_products(["Mouse", "Teclado"])

        product_count, sales_count = get_table_counts()

        self.assertEqual(product_count, 2)
        self.assertEqual(sales_count, 0)

    def test_to_cents(self):
        self.assertEqual(to_cents("59.90"), 5990)
        self.assertEqual(to_cents("180.00"), 18000)
        self.assertEqual(to_cents("1250.75"), 125075)


if __name__ == "__main__":
    unittest.main()
