
from datetime import datetime
import math


def validate_records(records):
    if not isinstance(records, list):
        raise ValueError("A entrada precisa ser uma lista.")

    if not records:
        raise ValueError("Não existem vendas para validar.")

    valid_records = []
    rejected_records = []

    required_fields = {
        "data",
        "produto",
        "quantidade",
        "preco_unitario",
        "valor_total",
    }

    for index, record in enumerate(records, start=1):
        errors = []

        if not isinstance(record, dict):
            rejected_records.append({
                "registro": index,
                "dados": record,
                "motivo": ["Formato inválido."]
            })
            continue

        if not required_fields.issubset(record.keys()):
            errors.append("Campo obrigatório ausente.")

        if errors:
            rejected_records.append({
                "registro": index,
                "dados": record,
                "motivo": errors
            })
            continue

        product = str(record["produto"]).strip()

        if not product:
            errors.append("Produto não informado.")

        try:
            sale_date = datetime.strptime(
                record["data"], "%Y-%m-%d"
            ).date()
        except (TypeError, ValueError):
            errors.append("Data inválida.")
            sale_date = None

        try:
            quantity = int(record["quantidade"])
        except (TypeError, ValueError):
            errors.append("Quantidade não numérica.")
            quantity = None

        try:
            unit_price = float(record["preco_unitario"])
        except (TypeError, ValueError):
            errors.append("Preço unitário não numérico.")
            unit_price = None

        try:
            total = float(record["valor_total"])
        except (TypeError, ValueError):
            errors.append("Valor total não numérico.")
            total = None

        if quantity is not None and quantity <= 0:
            errors.append("Quantidade deve ser positiva.")

        if unit_price is not None:
            if not math.isfinite(unit_price) or unit_price <= 0:
                errors.append("Preço unitário inválido.")

        if total is not None:
            if not math.isfinite(total) or total <= 0:
                errors.append("Valor total inválido.")

        if (
            quantity is not None
            and unit_price is not None
            and total is not None
            and math.isfinite(unit_price)
            and math.isfinite(total)
            and quantity > 0
            and unit_price > 0
            and total > 0
        ):
            expected_total = quantity * unit_price

            if not math.isclose(
                total, expected_total, rel_tol=0, abs_tol=0.01
            ):
                errors.append("Valor total inconsistente.")

        if errors:
            rejected_records.append({
                "registro": index,
                "dados": record,
                "motivo": errors
            })
            continue

        valid_records.append({
            "data": sale_date.isoformat(),
            "produto": product,
            "quantidade": quantity,
            "preco_unitario": round(unit_price, 2),
            "valor_total": round(total, 2),
        })

    return valid_records, rejected_records
