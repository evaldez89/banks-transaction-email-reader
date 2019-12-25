from .base_reader import BaseReader


class VimencaHtmlReader(BaseReader):
    def __init__(self, days_to_read, raw_html):
        self._query = ''
        return super().__init__('internetbanking@vimenca.com', days_to_read, raw_html)
