import importlib

from . import bhdleon_messages, vimenca_messages
from .message_abs import MessageAbs


class MessageFactory():

    _available_messages_modules: list = list()

    def __init__(self):
        for child in MessageAbs.__subclasses__():
            self._available_messages_modules.append({
                'main_class': child.__name__,
                'module': child.__module__
            })

        super().__init__()

    @staticmethod
    def get_bank_messages(bank_name) -> list:
        messages_module_info = MessageFactory.__bank_messages_module_info(bank_name)

        messages_classess = list()

        for message_info in messages_module_info:
            message_class = getattr(
                importlib.import_module(message_info.get('module', '')),
                message_info.get('main_class', '')
            )

            messages_classess.append(message_class)

        return messages_classess

    @staticmethod
    def __bank_messages_module_info(bank_name: str) -> list:
        messages = list()
        for modules_info in MessageFactory._available_messages_modules:
            module_path = modules_info.get('module', False)
            if bank_name == MessageFactory.extract_bank_name(module_path):
                messages.append(modules_info)
        return messages

    @staticmethod
    def extract_bank_name(module_path):
        if module_path:
            module_path = module_path.split('.')
            module_path = module_path[1] if len(module_path) == 2 else module_path
            module_path = module_path.split('_')[0]

        return module_path

    @staticmethod
    def get_subscribed_banks():
        return MessageFactory._available_messages_modules
