import csv
import os
from dataclasses import asdict

from domain.models.transaction import Transaction
from domain.ports.transaction_output import TransactionOutputPort


class CsvTransactionWriter(TransactionOutputPort[Transaction]):
    def __init__(self, output_path: str):
        self.output_path = output_path

    def write(self, items: list[Transaction]) -> None:
        transactions = items
        if not transactions:
            return

        needs_header = (
            not os.path.exists(self.output_path)
            or os.path.getsize(self.output_path) == 0
        )

        rows = [asdict(t) for t in transactions]

        with open(self.output_path, "a", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(
                output_file,
                fieldnames=rows[0].keys(),
                delimiter="|",
            )
            if needs_header:
                writer.writeheader()
            writer.writerows(rows)
