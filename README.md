# Bank Transaction Email Reader
The intention is of this project is to read emails comming from a bank regarding information of a transaction.

The ouput right now is an csv file delimited by pipes ("|") but the goal is to return a json with all the information so you can be able to use this on your mobile, desktop or web applications.

> Output Example:

    date|currency|amount|merchant|status|type|
    21/12/19 23:40|RD|91.12|None|Reversada|Compra
    21/12/19 23:40|RD|91.12|UBR* PENDING.UBER.COM|Aprobada|Compra
    21/12/19 20:32|RD|125.53|UBR* PENDING.UBER.COM|Aprobada|Compra


## The current supported banks are:
  - Banco BHD León (Dominican Republic)
  - Banco Vimenca (Dominican Republic) `(in progress)`

## The current supported email services are:
  - Gmail: Using the Google api with readonly permission


## Known TODO's:
  1. When running the main file, one parameter should be the user email to determine which mail service to use
  1. Rigth now it's only expecting multipart emails (threads) not single messages
  1. How to hanlde email credentials?
  1. How to handle email authentication token?
  1. Add Outlook Email service

## Known Issues:
  - Gmail autentication redirections says it's unsafe

## How to Execute:
  - You, as a developer, need a `credential.json` file provided by Gmail with the `readonly gmail api` activated. The file should be placed along side the `main.py` file. You can find instructions on how to get it from this [Quickstart Guide](https://developers.google.com/gmail/api/quickstart/python). It looks something like this:
  ```json
  {
    "installed": {
        "client_id": "the_cliente_id",
        "project_id": "the_project_id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "the_client_secret",
        "redirect_uris": [
            "urn:ietf:wg:oauth:2.0:oob",
            "http://localhost"
        ]
    }
  }
  ```
  - After having that, all you need is run:
    - `python main.py bhdleon example@gmail.com`


## How to contribute:
  - ### Add a new Bank
    Guided by the current implementations (`./banks_mail_readers/bhdleon_reader.py`), there are some things to consider:
      - The file with the code must be named with the prefix of the expected argument you want it to be called from main, conbine with `_reader`.
        > Example: __bhdleon__ is `bhdleon_reader.py` and from the main the argument it is called with is `bhdleon`.
      - The bank reader class must call the super class with the email the bank uses to send the transactions details.
        > Example:
        ```python
        class VimencaHtmlReader(BaseReader):
            def __init__(self):
            return super().__init__('internetbanking@vimenca.com')

        ```
      - Override the property methods with the logic of how to read the html email of the desired bank. The BaseReader class already has methods like: `get_element_by_class` and `get_elements_by_tag`.
        > Example:
        ```python
        # ... There might be other property method before and after
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

