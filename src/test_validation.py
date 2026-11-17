
import unittest

from validation import validate_records


class TestValidation(unittest.TestCase):

    def setUp(self):
        self.valid_record = {
            "data": "2026-09-02",
            "produto": "Mouse",
            "quantidade": "3",
            "preco_unitario": "59.90",
            "valor_total": "179.70",
        }

    def test_valid_records(self):
        valid, rejected = validate_records([self.valid_record])

        self.assertEqual(len(valid), 1)
        self.assertEqual(len(rejected), 0)
        self.assertEqual(valid[0]["produto"], "Mouse")

    def test_invalid_quantity(self):
        record = self.valid_record.copy()
        record["quantidade"] = "-2"

        valid, rejected = validate_records([record])

        self.assertEqual(len(valid), 0)
        self.assertEqual(len(rejected), 1)
        self.assertIn(
            "Quantidade deve ser positiva.",
            rejected[0]["motivo"]
        )

    def test_missing_product(self):
        record = self.valid_record.copy()
        record["produto"] = ""

        valid, rejected = validate_records([record])

        self.assertEqual(len(valid), 0)
        self.assertIn(
            "Produto não informado.",
            rejected[0]["motivo"]
        )

    def test_non_numeric_quantity(self):
        record = self.valid_record.copy()
        record["quantidade"] = "abc"

        valid, rejected = validate_records([record])

        self.assertEqual(len(valid), 0)
        self.assertIn(
            "Quantidade não numérica.",
            rejected[0]["motivo"]
        )

    def test_mixed_records(self):
        invalid_record = self.valid_record.copy()
        invalid_record["quantidade"] = "-2"

        valid, rejected = validate_records([
            self.valid_record,
            invalid_record,
        ])

        self.assertEqual(len(valid), 1)
        self.assertEqual(len(rejected), 1)

    def test_preserve_original_data(self):
        invalid_record = self.valid_record.copy()
        invalid_record["quantidade"] = "-2"

        valid, rejected = validate_records([invalid_record])

        self.assertEqual(
            rejected[0]["dados"],
            invalid_record
        )

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            validate_records([])

    def test_invalid_input_type(self):
        with self.assertRaises(ValueError):
            validate_records("invalid")


if __name__ == "__main__":
    unittest.main()
