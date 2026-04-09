import pytest

from banks_mail_readers.bank_email_parser import BankEmailParser
from infrastructure.parsers.registry import BankParserRegistry


class _FakeParser(BankEmailParser):
    """Minimal concrete parser for testing the registry in isolation."""

    @classmethod
    def bank_name(cls) -> str:
        return "testbank"

    @classmethod
    def bank_email(cls) -> str:
        return "test@testbank.com"

    @classmethod
    def get_subjects(cls) -> list[str]:
        return ["Test Subject"]

    @property
    def date(self) -> str:
        return ""

    @property
    def currency(self) -> str:
        return ""

    @property
    def amount(self) -> float:
        return 0.0

    @property
    def merchant(self) -> str:
        return ""

    @property
    def status(self) -> str:
        return ""

    @property
    def type(self) -> str:
        return ""


class _AnotherParser(_FakeParser):
    @classmethod
    def bank_name(cls) -> str:
        return "otherbank"

    @classmethod
    def get_subjects(cls) -> list[str]:
        return ["Other Subject"]


@pytest.fixture
def registry() -> BankParserRegistry:
    return BankParserRegistry()


class TestBankParserRegistryRegistration:
    def test_empty_registry_has_no_banks(self, registry):
        assert registry.get_available_bank_codes() == []

    def test_register_adds_bank(self, registry):
        registry.register("testbank", _FakeParser)
        assert "testbank" in registry.get_available_bank_codes()

    def test_register_multiple_parsers_same_bank(self, registry):
        registry.register("testbank", _FakeParser)
        registry.register("testbank", _AnotherParser)
        parsers = registry.get_bank_messages("testbank")
        assert len(parsers) == 2

    def test_register_multiple_banks(self, registry):
        registry.register("testbank", _FakeParser)
        registry.register("otherbank", _AnotherParser)
        codes = registry.get_available_bank_codes()
        assert "testbank" in codes
        assert "otherbank" in codes

    def test_available_bank_codes_are_sorted(self, registry):
        registry.register("zebra", _FakeParser)
        registry.register("alpha", _AnotherParser)
        codes = registry.get_available_bank_codes()
        assert codes == sorted(codes)


class TestBankParserRegistryLookup:
    def test_get_bank_messages_returns_registered_parsers(self, registry):
        registry.register("testbank", _FakeParser)
        assert _FakeParser in registry.get_bank_messages("testbank")

    def test_get_bank_messages_unknown_bank_returns_empty(self, registry):
        assert registry.get_bank_messages("nonexistent") == []

    def test_get_bank_messages_normalizes_case(self, registry):
        registry.register("testbank", _FakeParser)
        assert _FakeParser in registry.get_bank_messages("TESTBANK")

    def test_get_parser_for_subject_exact_match(self, registry):
        registry.register("testbank", _FakeParser)
        result = registry.get_parser_for_subject("testbank", "Test Subject")
        assert result is _FakeParser

    def test_get_parser_for_subject_no_match_returns_none(self, registry):
        registry.register("testbank", _FakeParser)
        result = registry.get_parser_for_subject("testbank", "Unknown Subject")
        assert result is None

    def test_get_parser_for_unknown_bank_returns_none(self, registry):
        result = registry.get_parser_for_subject("nonexistent", "Test Subject")
        assert result is None

    def test_exact_strategy_does_not_allow_partial_match(self, registry):
        registry.register("testbank", _FakeParser)
        result = registry.get_parser_for_subject("testbank", "Test Subject Extra")
        assert result is None


class TestBankParserRegistrySubjectStrategies:
    def test_regex_strategy_allows_partial_match(self):
        registry = BankParserRegistry(subject_match_strategy="regex")
        registry.register("testbank", _FakeParser)
        result = registry.get_parser_for_subject("testbank", "Test Subject Extra Content")
        assert result is _FakeParser

    def test_regex_strategy_uses_pattern_matching(self):
        registry = BankParserRegistry(subject_match_strategy="regex")
        registry.register("testbank", _FakeParser)
        result = registry.get_parser_for_subject("testbank", "No Match Here")
        assert result is None

    def test_default_strategy_is_exact(self, registry):
        registry.register("testbank", _FakeParser)
        assert registry.subject_match_strategy == "exact"
