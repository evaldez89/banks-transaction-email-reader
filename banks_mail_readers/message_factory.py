from . import vimenca_messages, bhdleon_messages
import importlib


class MessageFactory():
    @staticmethod
    def get_bank_messages(bank_name) -> list:
        message_packages = MessageFactory.__bank_messages(bank_name)

        messages_classess = list()

        for message_info in message_packages:
            message_class = getattr(
                importlib.import_module(message_info.get('module', '')),
                message_info.get('main_class', '')
            )

            messages_classess.append(message_class)

        return messages_classess

    @staticmethod
    def __bank_messages(bank_name: str) -> list:
        from .message import MessageAbs
        messages = list()
        for child in MessageAbs.__subclasses__():
            if child.bank == bank_name:
                messages.append({
                    'main_class': child.__name__,
                    'module': child.__module__
                })
        return messages