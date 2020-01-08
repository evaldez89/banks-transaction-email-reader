from .base_reader import BaseReader


class BHDLeonHtmlReader(BaseReader):
    def __init__(self, name: str):
        return super().__init__(name, 'alertas@bhdleon.com.do')
