from .base_reader import BaseReader


class VimencaHtmlReader(BaseReader):
    def __init__(self):
        return super().__init__('internetbanking@vimenca.com')

    @property
    def date(self):
        pass

    @property
    def currency(self):
        pass

    @property
    def amount(self):
        pass

    @property
    def merchant(self):
        pass

    @property
    def status(self):
        pass

    @property
    def type(self):
        pass

    @property
    def subjetcs_to_ignore(self):
        pass
