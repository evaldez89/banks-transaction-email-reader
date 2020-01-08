from .base_reader import BaseReader
import importlib


class BankReaderFactory():
    @staticmethod
    def get_bank(bank_info: dict):
        bank_class = getattr(
            importlib.import_module(bank_info.get('module', '')),
            bank_info.get('main_class', '')
        )
        return bank_class
