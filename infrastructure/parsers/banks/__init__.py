"""Importing bank modules triggers their self-registration into bank_parser_registry."""

from infrastructure.parsers.banks.bhd import parsers as _bhd  # noqa: F401
from infrastructure.parsers.banks.vimenca import parsers as _vimenca  # noqa: F401
