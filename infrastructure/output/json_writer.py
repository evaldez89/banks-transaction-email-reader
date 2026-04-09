import json
from dataclasses import asdict

from domain.models.transaction import Transaction
from domain.ports.transaction_output import TransactionOutputPort


class JsonTransactionWriter(TransactionOutputPort[Transaction]):
    def __init__(self, output_path: str):
        self.output_path = output_path

    def write(self, items: list[Transaction]) -> None:
        payload = [asdict(t) for t in items]
        with open(self.output_path, "w", encoding="utf-8") as output_file:
            json.dump(payload, output_file, ensure_ascii=False, indent=2)
