from typing import Optional

from infrastructure.output.csv_writer import CsvTransactionWriter
from infrastructure.output.json_writer import JsonTransactionWriter


class TransactionWriter:
    def __init__(self, output_format: str, output_path: Optional[str] = None):
        self.output_format = output_format
        self.output_path = output_path or (
            "transactions.json" if output_format == "json" else "transactions.csv"
        )

    def write(self, transactions: list) -> None:
        if self.output_format == "json":
            writer = JsonTransactionWriter(self.output_path)
        else:
            writer = CsvTransactionWriter(self.output_path)
        writer.write(transactions)
