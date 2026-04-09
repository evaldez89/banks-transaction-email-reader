# Bank Transaction Email Reader

Reads transaction notification emails from bank accounts and exports them as structured data (CSV or JSON).

## Supported Banks

- Banco BHD León (Dominican Republic) ✅
- Banco Vimenca (Dominican Republic) ✅

## Supported Email Providers

- Gmail (Google API, read-only scope) ✅

## Architecture

The project follows a clean architecture layered structure:

```
domain/              # Pure business models and port contracts (no dependencies)
  models/            #   Transaction, BankEmail, EmailSearchCriteria
  ports/             #   EmailProvider, BankEmailParser, TransactionOutputPort

infrastructure/      # Concrete implementations of domain ports
  parsers/           #   Bank-specific HTML email parsers + BankParserRegistry
    banks/
      bhd/           #     BHD parser registration
      vimenca/       #     Vimenca parser registration
  email_providers/   #   EmailProviderRegistry
  output/            #   CsvTransactionWriter, JsonTransactionWriter

mail_services/       # Email provider implementations
  gmail/             #   GmailEmailProvider + OAuth2 auth

banks_mail_readers/  # Bank-specific email parser implementations
```

Adding a new bank or email provider requires no changes to existing code — see the guides below.

## Requirements

- Python 3.12+
- A Gmail API `credentials.json` file with read-only scope

### Install runtime dependencies

```bash
pip install -r requirements.txt
```

### Install development dependencies (tests + linting)

```bash
pip install -r requirements-dev.txt
```

## Configuration

Configure via environment variables:

| Variable | Description | Default |
|---|---|---|
| `EMAIL_CREDENTIALS_FILE` | Path to Gmail OAuth2 credentials file | `credentials.json` |
| `EMAIL_TOKEN_FILE` | Path to the generated OAuth2 token file | `token.json` |
| `SUBJECT_MATCH_STRATEGY` | Subject matching strategy: `exact` or `regex` | `exact` |

## How to Execute

```bash
python main.py <bank> <email> [--days_from N] [--format csv|json] [--output PATH] [--domain DOMAIN]
```

**Examples:**

```bash
# Read BHD emails from the last 7 days, output as CSV (default)
python main.py bhd me --days_from 7

# Read Vimenca emails and export as JSON
python main.py vimenca me --format json --output transactions.json

# Specify a delegated Gmail account
python main.py bhd delegate@company.com --days_from 30
```

**Arguments:**

| Argument | Description | Default |
|---|---|---|
| `bank` | Bank code: `bhd` or `vimenca` | required |
| `email` | Gmail account (`me` or delegated address) | required |
| `--days_from` | Number of days to look back | `366` |
| `--format` | Output format: `csv` or `json` | `csv` |
| `--output` | Output file path | `transactions.csv` / `transactions.json` |
| `--domain` | Email provider domain override (e.g. `gmail`) | derived from `email` |

## Output

### CSV

```
date,currency,amount,merchant,status,type,bank,source_subject
21/12/19 23:40,RD,91.12,UBR* PENDING.UBER.COM,Aprobada,Compra,bhd,BHD Notificación de Transacciones
```

### JSON

```json
[
  {
    "date": "21/12/19 23:40",
    "currency": "RD",
    "amount": 91.12,
    "merchant": "UBR* PENDING.UBER.COM",
    "status": "Aprobada",
    "type": "Compra",
    "bank": "bhd",
    "source_subject": "BHD Notificación de Transacciones"
  }
]
```

## Running Tests

```bash
pytest
```

Tests are organized as:

```
tests/
  unit/
    parsers/          # Parser tests per bank with HTML fixtures
    test_bank_parser_registry.py
  integration/
    test_gmail_provider.py  # Gmail provider with mocked Google API
```

## Gmail Credentials Setup

You need a `credentials.json` file from the Google Cloud Console with the Gmail read-only scope:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Gmail API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download the credentials file
5. Set `EMAIL_CREDENTIALS_FILE` to its path, or place it as `credentials.json` in the project root

On first run the app will open a browser window to complete OAuth2 authorization and save a `token.json` file for subsequent runs. See the [Gmail API Quickstart](https://developers.google.com/gmail/api/quickstart/python) for full details.

## Adding a New Bank

1. Create a parser class in `banks_mail_readers/` that extends `BankEmailParser`:

   ```python
   # banks_mail_readers/mybank_messages.py
   from .bank_email_parser import BankEmailParser

   class MyBankParser(BankEmailParser):
       @classmethod
       def bank_name(cls) -> str: return "mybank"

       @classmethod
       def bank_email(cls) -> str: return "alerts@mybank.com"

       @classmethod
       def get_subjects(cls) -> list[str]:
           return ["MyBank: Transaction Notification"]

       # implement date, currency, amount, merchant, status, type properties
   ```

2. Create a registration module at `infrastructure/parsers/banks/mybank/parsers.py`:

   ```python
   from banks_mail_readers.mybank_messages import MyBankParser
   from infrastructure.parsers.registry import bank_parser_registry

   bank_parser_registry.register("mybank", MyBankParser)
   ```

3. Add one import line to `infrastructure/parsers/banks/__init__.py`:

   ```python
   from infrastructure.parsers.banks.mybank import parsers as _mybank  # noqa: F401
   ```

That's all. No existing code needs to change.

## Adding a New Email Provider

1. Implement `EmailProvider[TRawMessage, TTransaction]` from `domain/ports/email_provider.py`.

2. Create a folder under `mail_services/` and register the provider in its `__init__.py`:

   ```python
   # mail_services/myprovider/__init__.py
   from infrastructure.email_providers.registry import email_provider_registry
   from .myprovider_email_provider import MyEmailProvider

   email_provider_registry.register("myprovider", MyEmailProvider)
   ```

3. Add one import line to `mail_services/__init__.py`:

   ```python
   from mail_services import myprovider  # noqa: F401
   ```

The provider key is matched against the domain extracted from the `email` argument (or the `--domain` flag).

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
