from banks_mail_readers.bhd_messages import GeneralMessage, PINPesoMessage
from infrastructure.parsers.registry import bank_parser_registry

bank_parser_registry.register("bhd", GeneralMessage)
bank_parser_registry.register("bhd", PINPesoMessage)
