
import unittest

from generate_report import (
    generate_report,
    calculate_monthly_revenue,
    calculate_monthly_variation,
)


class TestSalesReport(unittest.TestCase):

    def setUp(self):
        self.records = [
            {
                "data": "2026-09-02",
                "produto": "Mouse",
                "quantidade": 3,
                "preco_unitario": 59.90,
                "valor_total": 179.70,
            },
            {
                "data": "2026-09-03",
                "produto": "Teclado",
                "quantidade": 2,
                "preco_unitario": 120.00,
                "valor_total": 240.00,
            },
            {
                "data": "2026-10-02",
                "produto": "Mouse",
                "quantidade": 4,
                "preco_unitario": 59.90,
                "valor_total": 239.60,
            },
        ]

    def test_generate_report(self):
        report = generate_report(self.records)

        self.assertEqual(report["faturamento_total"], 659.30)
        self.assertEqual(report["quantidade_vendas"], 3)
        self.assertEqual(report["unidades_vendidas"], 9)
        self.assertEqual(report["ticket_medio"], 219.77)
        self.assertEqual(report["produto_mais_vendido"], "Mouse")

    def test_monthly_revenue(self):
        result = calculate_monthly_revenue(self.records)

        self.assertEqual(result["2026-09"], 419.70)
        self.assertEqual(result["2026-10"], 239.60)

    def test_monthly_variation(self):
        monthly_revenue = {
            "2026-09": 419.70,
            "2026-10": 239.60,
        }

        result = calculate_monthly_variation(monthly_revenue)

        self.assertEqual(result, -42.91)

    def test_insufficient_months(self):
        monthly_revenue = {
            "2026-09": 419.70,
        }

        result = calculate_monthly_variation(monthly_revenue)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
