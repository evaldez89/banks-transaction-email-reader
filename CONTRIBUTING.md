# How to contribute
  
  ## Add a new Bank
  
  - Guided by the current implementations (`./banks_mail_readers/bhdleon_reader.py`), there are some things to consider:
      - The file with the code must be named with the prefix of the expected argument you want it to be called from main, conbine with `_reader`.
        > Example: __bhdleon__ is `bhdleon_reader.py` and from the main the argument it is called with is `bhdleon`.
      - The bank reader class must call the super class with the email the bank uses to send the transactions details.
        > Example:
        ```python
        class VimencaHtmlReader(BaseReader):
            def __init__(self):
            return super().__init__('ebanking@bank.com')

        ```
      - Override the properties methods with the logic of how to read the html email of the desired bank. The BaseReader class already has methods like: `get_element_by_class` and `get_elements_by_tag`.
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
