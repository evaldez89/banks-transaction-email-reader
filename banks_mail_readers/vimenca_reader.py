from .base_reader import BaseReader


class VimencaHtmlReader(BaseReader):
    def __init__(self):
        return super().__init__('internetbanking@vimenca.com')
