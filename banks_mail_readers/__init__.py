from . import vimenca_reader, bhdleon_reader
# TODO: Posiblemente hacer los imports de los bancos
# ya no sea necesario debido a que se esta haciendo
# dinamicamente


def get_subscribed_banks() -> list:
    from .base_reader import BaseReader
    banks = list()
    for child in BaseReader.__subclasses__():
        banks.append({
            'main_class': child.__name__,
            'module': child.__module__
        })
    return banks
