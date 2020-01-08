from .base_reader import BaseReader


class VimencaHtmlReader(BaseReader):
    def __init__(self, name: str):
        return super().__init__(name, 'internetbanking@vimenca.com')
