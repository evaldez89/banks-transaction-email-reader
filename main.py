from mail_services.gmail_service import GmailService
import argparse
from banks_mail_readers.message_factory import MessageFactory


messages_factory = MessageFactory()
SUBSCRIBED_BANKS = messages_factory.get_subscribed_banks()


def main(**kwargs):

    bank_name = kwargs.get('bank')
    days_from = kwargs.get('days_from')

    gmail = GmailService(bank_name, days_from)
    gmail.authenticate()
    gmail.build_service()
    gmail.read_mail()


if __name__ == '__main__':

    bank_choices = [messages_factory.extract_bank_name(bank_name.get('module'))
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
        default=366
    )

    kwargs = dict()

    for k, v in vars(arg_parser.parse_args()).items():
        if v:
            kwargs[k] = v

    main(**kwargs)
