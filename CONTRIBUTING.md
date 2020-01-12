# How to contribute

  ## Add a new Bank

  - Guided by the current implementations (`./banks_mail_readers/bhdleon_messages.py`), there are some things to consider:
      - The file with the code must be named with the prefix of the expected argument you want it to be called from main, conbine with `_messages`.
        > Example: __bhdleon__ is `bhdleon_messages.py` and from the main the argument it is called with is `bhdleon`.
      - This class is to hold all the different messages identified by the subjects:
        > Example:
        ```python
        # class 1
        class GeneralMessage(MessageAbs):

        @property
        def subjects(self):
            return [
                'Notificación de Transacción',
                'Aviso Retiro de efectivo'
            ]
        # ------------------------------------- #
        # class 2
        class PaymenReceiptMessage(MessageAbs):

        @property
        def subjects(self):
            return [
                'Comprobante de Pago',
                '-Comprobante de pago beneficiario'
            ]
        ```
      - Class property `subjects` contains all the subject to be read. In case you want to ignore a particular subject that migth be similiar in subject but different in body structure, you can append a `'-'` at the begining to ignore it (just for Gmail).
        > Example:
          ```python
          @property
          def subjects(self):
              return [
                  'Comprobante de Pago', # subject to look for
                  '-Comprobante de pago beneficiario' # subject to ignore
              ]
          ```
      - The bank messages class must override, among other properties, these two:
        > Example:
        ```python
        @classmethod
        def bank_name(cls):
            return 'vimenca'

        @classmethod
        def bank_email(cls):
            return 'internetbanking@vimenca.com'
        ```
      - Override the properties methods with the logic of how to read the html email of the desired bank. The MessageAbs class already has methods like: `get_element_by_class` and `get_elements_by_tag`.
        > Example:
        ```python
        # ... There are others properties method before and after
        @property
        def currency(self):
            return self.get_element_by_class('td', 'class', 't_moneda').text

        @property
        def amount(self):
            return self.get_element_by_class('td', 'class', 't_monto').text

        @property
        def merchant(self):
            merchant_name = self.get_element_by_class('td', 'class', 't_comercio')
            merchant_name = merchant_name.text if merchant_name else 'None'
            return merchant_name
        ```
    That is all, from `main.py` and base on the argument passed when running the file y will find all suscribed banks.

  ### Add a new Email Service
  Currently only Gmail is supported. Stay tunned for intructions on how to add a new service.
