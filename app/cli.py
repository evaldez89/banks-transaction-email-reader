"""Application CLI entrypoints and argument mapping."""

from app.use_cases.extract_transactions import extract_transactions


def run(bank: str, email: str, days_from: int, output: str) -> None:
    """Invoke the transaction extraction use case.

    This function is intentionally thin and delegates orchestration to use-cases.
    """
    extract_transactions(bank=bank, email=email, days_from=days_from, output=output)
