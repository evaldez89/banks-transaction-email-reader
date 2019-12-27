from mail_services.gmail_service import GmailService
from banks_mail_readers.bhdleon_reader import BHDLeonHtmlReader


def main():

    # TODO; Un argumento debe ser el correo, y en base a este
    # determinar que servicio de correo usar

    bank = BHDLeonHtmlReader()

    gmail = GmailService(100)
    gmail.authenticate()
    gmail.build_service()
    gmail.read_mail(bank)


if __name__ == '__main__':
    main()
