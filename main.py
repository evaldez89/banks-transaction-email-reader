import argparse

import infrastructure.parsers.banks  # noqa: F401 — triggers bank self-registration
import mail_services  # noqa: F401 — triggers provider self-registration
from infrastructure.email_providers.registry import email_provider_registry
from infrastructure.output.writer import TransactionWriter
from infrastructure.parsers.registry import bank_parser_registry

SUBSCRIBED_BANKS = bank_parser_registry.get_subscribed_banks()


def main(**kwargs):
    bank_name = kwargs.get("bank", "")
    email = kwargs.get("email", "me")
    days_from = kwargs.get("days_from", 1)
    output = kwargs.get("output")
    output_format = kwargs.get("format", "csv")
    domain = kwargs.get("domain", email.split("@")[-1].split(".")[0])

    provider = email_provider_registry.get_provider(
        domain,
        bank_name=bank_name,
        email_account=email,
        days_from=days_from,
    )
    provider.authenticate()
    provider.build_service()
    transactions = provider.get_transactions()

    writer = TransactionWriter(output_format=output_format, output_path=output)
    writer.write(transactions)


if __name__ == "__main__":
    bank_choices = bank_parser_registry.get_available_bank_codes()

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "bank",
        help="The bank to read the emails from",
        type=str,
        choices=bank_choices,
    )

    arg_parser.add_argument(
        "email",
        help='The email account to read from (e.g. "me" or delegated account)',
    )

    arg_parser.add_argument(
        "--days_from",
        help="Days to read from on the mail server",
        type=int,
        default=366,
    )

    arg_parser.add_argument(
        "--output",
        help="Path to output file. Defaults: transactions.csv or transactions.json",
        default=None,
    )

    arg_parser.add_argument(
        "--format",
        help="Output format",
        choices=["csv", "json"],
        default="csv",
    )

    arg_parser.add_argument(
        "--domain",
        help="Email domain to use for selecting the email provider",
        default=None,
    )

    kwargs = dict()

    for k, v in vars(arg_parser.parse_args()).items():
        if v is not None:
            kwargs[k] = v

    main(**kwargs)
