
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from analytics import (
    revenue_by_product,
    units_sold_by_product,
    monthly_revenue,
    best_revenue_product,
    revenue_share_by_product
)


class TestAnalytics(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_file = Path(self.temp_dir.name) / "test.db"

        self.connection_patcher = patch(
            "analytics.get_connection",
            side_effect=self.create_connection
        )
        self.connection_patcher.start()

        self.create_test_data()

    def tearDown(self):
        self.connection_patcher.stop()
        self.temp_dir.cleanup()

    def create_connection(self):
        return sqlite3.connect(self.database_file)

    def create_test_data(self):
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
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        """)

        cursor.executemany("""
            INSERT INTO produtos (nome)
            VALUES (?)
        """, [
            ("Mouse",),
            ("Teclado",)
        ])

        cursor.executemany("""
            INSERT INTO vendas (
                data,
                produto_id,
                quantidade,
                preco_unitario_centavos,
                valor_total_centavos
            )
            VALUES (?, ?, ?, ?, ?)
        """, [
            ("2026-09-10", 1, 2, 5000, 10000),
            ("2026-09-15", 1, 1, 5000, 5000),
            ("2026-10-05", 2, 1, 20000, 20000)
        ])

        connection.commit()
        connection.close()

    def test_revenue_by_product(self):
        result = revenue_by_product()

        self.assertEqual(result[0][0], "Teclado")
        self.assertAlmostEqual(result[0][1], 200.00)
        self.assertEqual(result[1][0], "Mouse")
        self.assertAlmostEqual(result[1][1], 150.00)

    def test_units_sold_by_product(self):
        result = units_sold_by_product()

        self.assertEqual(result[0], ("Mouse", 3))
        self.assertEqual(result[1], ("Teclado", 1))

    def test_monthly_revenue(self):
        result = monthly_revenue()

        self.assertEqual(result, [
            ("2026-09", 150.00),
            ("2026-10", 200.00)
        ])

    def test_best_revenue_product(self):
        result = best_revenue_product()

        self.assertEqual(result[0], "Teclado")
        self.assertAlmostEqual(result[1], 200.00)

    def test_revenue_share_by_product(self):
        result = revenue_share_by_product()

        self.assertEqual(result[0][0], "Teclado")
        self.assertAlmostEqual(result[0][2], 57.14)

        self.assertEqual(result[1][0], "Mouse")
        self.assertAlmostEqual(result[1][2], 42.86)


if __name__ == "__main__":
    unittest.main()
