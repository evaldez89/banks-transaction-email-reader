# Bank Transaction Email Reader
The intention is of this project is to read emails comming from a bank regarding information of a transaction.

The ouput right now is an csv file delimited by pipes ("|") but the goal is to return a json with all the information so you can be able to use this on your mobile, desktop or web applications.

> Output Example: 
    
    date|currency|amount|merchant|status|type|
    21/12/19 23:40|RD|91.12|None|Reversada|Compra
    21/12/19 23:40|RD|91.12|UBR* PENDING.UBER.COM|Aprobada|Compra
    21/12/19 20:32|RD|125.53|UBR* PENDING.UBER.COM|Aprobada|Compra


## The current supported banks are:
  - Banco BHD León (Dominican Republic) `(in progress)`
  - Banco Vimenca (Dominican Republic) `(in progress)`

## The current supported email services are:
  - Gmail: Using the Google api with readonly permission

## Known issues:
  - Gmail autentication redirections says its unsafe