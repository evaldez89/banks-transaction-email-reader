from mail_services.gmail_service import GmailService
import argparse
from banks_mail_readers import get_subscribed_banks
from banks_mail_readers.bank_factory import BankReaderFactory


SUBSCRIBED_BANKS = get_subscribed_banks()


def is_bank_module_name(bank_info: dict, bank_arg: str):
    bank_name = bank_info.get('module', '').split('.')[1][:-7]
    return bank_name == bank_arg


def main(**kwargs):

    bank_arg = kwargs.get('bank')
    days_from = kwargs.get('days_from')
    bank_class_info = [bank for bank in SUBSCRIBED_BANKS
                       if is_bank_module_name(bank, bank_arg)]

    if bank_class_info:
        bank_factory = BankReaderFactory()

        try:
            bank_class = bank_factory.get_bank(bank_class_info[0])
        except Exception as e:
            error_message = f'Undefined Bank "{bank_arg}"'
            raise ValueError(error_message) from e
        else:
            bank = bank_class(name=bank_arg)

            # TODO: Get email service from email parameter
            gmail = GmailService(days_from)
            gmail.authenticate()
            gmail.build_service()
            gmail.read_mail(bank)


if __name__ == '__main__':

    bank_choices = [bank_name.get('module').split('.')[1][:-7]
                    for bank_name in SUBSCRIBED_BANKS]

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        'bank', help='The bank to read the emails from',
        type=str,
        choices=bank_choices
    )

    arg_parser.add_argument(
        'email', help='The email account to read from'
    )

    arg_parser.add_argument(
        '--days_from', help='Days to read from on the mail server',
        default=100
    )

    kwargs = dict()

    for k, v in vars(arg_parser.parse_args()).items():
        if v:
            kwargs[k] = v

    main(**kwargs)
