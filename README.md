# Bank Transaction Email Reader

The intention of this project is to read emails coming from a bank regarding information of a transaction.

The output right now is an csv file delimited by pipes ("|") but the goal is to return a json with all the information so you can be able to use this on your mobile, desktop or web applications.

Output Example:

    date|currency|amount|merchant|status|type|
    21/12/19 23:40|RD|91.12|None|Reversada|Compra
    21/12/19 23:40|RD|91.12|UBR* PENDING.UBER.COM|Aprobada|Compra
    21/12/19 20:32|RD|125.53|UBR* PENDING.UBER.COM|Aprobada|Compra

## Task Legend

:construction: Work in progress

:white_check_mark: When task is done

:alarm_clock: Pending

### Bancos del Estado

- [ ] BanReservas :alarm_clock:

### Bancos Comerciales

- [ ] Banco Vimenca (Dominican Republic) :construction:
- [ ] Banco Popular Dominicano :alarm_clock:
- [ ] Banco BHD León :white_check_mark:
- [ ] Banco del Progreso :alarm_clock:
- [ ] Banco Santa Cruz :alarm_clock:
- [ ] Banco Caribe :alarm_clock:
- [ ] Banco BDI :alarm_clock:
- [ ] Banco López de Haro :alarm_clock:
- [ ] Banco Ademi :alarm_clock:
- [ ] Banco BELLBANK :alarm_clock:
- [ ] Banco Múltiple Activo Dominicana :alarm_clock:

### Bancos Extranjeros

- [ ] Scotiabank :alarm_clock:
- [ ] Citibank :alarm_clock:
- [ ] Banco Promerica :alarm_clock:
- [ ] Banesco :alarm_clock:
- [ ] Bancamerica :alarm_clock:
  
### Bancos de Ahorro y Crédito

- [ ] Banco Atlántico :alarm_clock:
- [ ] Banco Bancotui :alarm_clock:
- [ ] Banco BDA :alarm_clock:
- [ ] Banco Adopem :alarm_clock:
- [ ] Banco Agrícola De La República Dominicana :alarm_clock:
- [ ] Banco Pyme Bhd :alarm_clock:
- [ ] Banco Capital :alarm_clock:
- [ ] Banco Confisa :alarm_clock:
- [ ] Banco Empire :alarm_clock:
- [ ] Banco Motor Crédito :alarm_clock:
- [ ] Banco Rio :alarm_clock:
- [ ] Banco Providencial :alarm_clock:
- [ ] Banco Del Caribe :alarm_clock:
- [ ] Banco Inmobiliario (Banaci) :alarm_clock:
- [ ] Banco Gruficorp :alarm_clock:
- [ ] Banco Cofaci :alarm_clock:
- [ ] Banco Atlas :alarm_clock:
- [ ] Banco Bonanza :alarm_clock:
- [ ] Banco Fihogar :alarm_clock:
- [ ] Banco Federal :alarm_clock:
- [ ] Banco Micro :alarm_clock:
- [ ] Banco Union :alarm_clock:

### Asociaciones de Ahorro y Préstamo

- [ ] Asociación Popular :alarm_clock:
- [ ] Asociación Popular de Ahorros y Préstamos :alarm_clock:
- [ ] Asociación Cibao :alarm_clock:
- [ ] Asociación Nortena :alarm_clock:
- [ ] Asociación Peravia :alarm_clock:
- [ ] Asociación Romana :alarm_clock:
- [ ] Asociación Higuamo :alarm_clock:
- [ ] Asociación La Vega Real :alarm_clock:
- [ ] Asociación Duarte :alarm_clock:
- [ ] Asociación Barahona :alarm_clock:
- [ ] Asociación Maguana :alarm_clock:
- [ ] Asociación Mocana :alarm_clock:
- [ ] Asociación Bonao :alarm_clock:
- [ ] Asociación La Nacional :alarm_clock:
- [ ] Asociación Noroestana :alarm_clock:

## The current supported email services are

  - Gmail: Using the Google api with readonly permission

## Known Major Tasks TODO

  1. When running the main file, one parameter should be the user email to determine which mail service to use
  2. Right now it's only expecting multipart emails (threads) not single messages
  3. How to handle email credentials?
  4. How to handle email authentication token?
  5. Add Outlook Email service
  6. Add a new Email Service 
     1. Currently only Gmail is supported. Stay tunned for instructions on how to add a new service. 

## Known Issues

  - Gmail autentication redirections says it's unsafe

## How to Execute

  - Python versions that I can assure this work with: 
    >3.6.9
    
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
  - Install requirements: `python -m pip install -r requirements.txt`
  - After having that, all you need is run:
    - `python main.py bhdleon example@gmail.com`

## How to contribute

  - ### Add a new Bank

    Guided by the current implementations (`./banks_mail_readers/bhdleon_reader.py`), there are some things to consider:
      - The file with the code must be named with the prefix of the expected argument you want it to be called from main, combine with `_reader`.
        > Example: __bhdleon__ is `bhdleon_reader.py` and from the main the argument it is called with is `bhdleon`.
      - The bank reader class must call the super class with the email the bank uses to send the transactions details.
        > Example:
        ```python
        class VimencaHtmlReader(BaseReader):
            def __init__(self):
            return super().__init__('internetbanking@vimenca.com')

        ```
      - Override the property methods with the logic of how to read the html email of the desired bank. The BaseReader class already has methods like: `get_element_by_class` and `get_elements_by_tag`.

       **Example:**

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
    That is all, from `main.py` and base on the argument passed when running the file y will find all subscribed banks.

## Make sure to checkout the [CONTRIBUTING.md](./CONTRIBUTING.md) guidelines.