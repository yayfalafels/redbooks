# RedBooks - Release Roadmap

## Scope

RedBooks is a productivity app for managing personal finances

the primary intended uses are for 

01. reporting financial reports
02. tracking expenses
03. reconciling statements

- customised to financial institutions in Singapore. 
- priority is web app version with backend API for automation workflows and integrations.

## References

- [financial-statements remote repo](https://github.com/yayfalafels/financial-statements/)
- [financial-statements local](../../../../financial-statements/README.md)
- [financial-statements about](../../../../financial-statements/docs/releases/010/about.md)

An earlier design attempt `financial-statements` was based on incremental improvement from the local prototype.  The local prototype  `hb helpers` uses 3rd party Mobile app HomeBudget as the primary financial accounting data storage, along with a suite of helper tools in Google sheets and local python scripts for UI and automation. The `financial-statements` was never implemented and only a design concept.  

__releases__

| id | repo                 | version   | description             |
| -- | -------------------- | --------- | ----------------------- |
| 01 | hb helpers           | 20260523  | prototype local         |
| 02 | financial-statements | 010       | design attempt          |
| 03 | redbooks             | 020       | POC Bookkeeping         |
| 04 | redbooks             | 030       | MVP Web App             |
| 05 | redbooks             | 040       | Live reconciled ledger  |
| 06 | redbooks             | 100       | Beta App store          |  

__release features__

| id | feature              | prototype local    | poc bookkeeping | mvp web app         |
| -- | -------------------- | ------------------ | --------------- | ------------------- | 
| -- | version              | ---                | 020             | 030                 |
| 01 | accounting store     | homebudget         | api             | api                 | 
| 02 | txn storage          | homebudget + gs    | postgresql db   | postgresql db       |
| 03 | deployment           | app + gs + scripts | docker local    | web app mob + desk  | 
| 04 | back end api         | homebudget         | python fastapi  | python fastapi      |
| 05 | front end ui         | homebudget + gs    | react.js        | react.js            |
| 06 | txn category model   | hb + fin stm       | consolidated    | consolidated        |
| 07 | manually record txns | homebudget         | X               | X                   |
| 08 | account ledger       | homebudget         | X               | X                   |
| 09 | multi currency       | homebudget         | X               | X                   |
| 10 | income statement     | fin stm gs         | X               | X                   |
| 11 | balance sheet        | fin stm gs         | X               | X                   |
| 12 | users                | bespoke 1 user     | X               | X                   |
| 13 | login                | unauth             | oauth           | oauth               |
| 14 | statement loaders    | python + sql + gs  | --              | --                  |
| 15 | stm txn reconcile    | gs ui              | manual          | manual              |
| 16 | csv export           | -----              | X               | X                   |
| 17 | file storage         | local + s3         | local           | S3                  |
| 18 | reconcile algorithm  | manual             | --              | --                  |
| 19 | split txn            | manual             | manual          | X                   |
| 20 | pdf export           | -----              | --              | X                   |
| 21 | forecast             | fin stm gs         | --              | --                  |

| id | feature              | reconciled ledger  | beta app store          |
| -- | -------------------- | ------------------ | ----------------------- |
| -- | version              | 040                | 100                     |
| 01 | accounting store     | api                | api                     |
| 02 | txn storage          | postgresql db      | postgresql db           |
| 03 | deployment           | web app mob + desk | cloud api + itunes app  |
| 04 | back end api         | python fastapi     | python fastapi          |
| 05 | front end ui         | react.js           | react.js                |
| 06 | txn category model   | consolidated       | consolidated            |
| 07 | manually record txns | X                  | X                       |
| 08 | account ledger       | X                  | X                       |
| 09 | multi currency       | X                  | X                       |
| 10 | income statement     | X                  | X                       |
| 11 | balance sheet        | X                  | X                       |
| 12 | users                | X                  | X                       |
| 13 | login                | oauth              | oauth                   |
| 14 | statement loaders    | desktop            | mobile app              |
| 15 | stm txn reconcile    | desktop            | desktop                 |
| 16 | csv export           | X                  | X                       |
| 17 | file storage         | S3                 | S3                      |
| 18 | reconcile algorithm  | rules + manual     | rules + gen ai          |
| 19 | split txn            | X                  | X                       |
| 20 | pdf export           | X                  | X                       |
| 21 | forecast             | tbd                | tbd                     |
