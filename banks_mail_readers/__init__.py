# Add all module to be dinamically import
from . import vimenca_reader, bhdleon_reader


def get_subscribed_banks() -> list:
    from .base_reader import BaseReader
    banks = list()
    for child in BaseReader.__subclasses__():
        banks.append({
            'main_class': child.__name__,
            'module': child.__module__
        })
    return banks
