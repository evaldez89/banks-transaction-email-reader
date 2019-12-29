from mail_services.gmail_service import GmailService
import argparse
from banks_mail_readers import get_subscribed_banks
from banks_mail_readers.bank_factory import BankReaderFactory


SUBSCRIBED_BANKS = get_subscribed_banks()


def is_bank_module_name(bank_info: dict, bank_arg: str):
    bank_name = bank_info.get('module').split('.')[1][:-7]
    return bank_name == bank_arg


def main(**kwargs):

    arguments = kwargs.get('arguments')
    bank_class_info = [bank for bank in SUBSCRIBED_BANKS
                       if is_bank_module_name(bank, arguments.get('bank'))]

    bank_factory = BankReaderFactory()
    bank = None

    if bank_class_info:
        bank_class = bank_factory.get_bank(bank_class_info[0])
        bank = bank_class()

    if bank is not None:
        gmail = GmailService(100)
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

    kwargs = dict()

    for k, v in vars(arg_parser.parse_args()).items():
        if v:
            kwargs[k] = v

    main(arguments=kwargs)
