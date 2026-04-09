from banks_mail_readers.vimenca_messages import (
    GeneralMessage,
    PaymentReceiptMessage,
    TransactionNotificationMessage,
)
from infrastructure.parsers.registry import bank_parser_registry

bank_parser_registry.register("vimenca", GeneralMessage)
bank_parser_registry.register("vimenca", PaymentReceiptMessage)
bank_parser_registry.register("vimenca", TransactionNotificationMessage)
