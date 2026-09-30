# RedBooks Personal finances app

productivity app for managing personal finances. consolidated personal finance app for 

01. reporting financial reports
02. tracking expenses
03. reconciling statements. 

- customised to financial institutions in Singapore. 
- priority is web app version with backend API for automation workflows and integrations.

## References

- [financial-statements remote repo](https://github.com/yayfalafels/financial-statements/)
- [financial-statements local](../../../../financial-statements/README.md)
- [financial-statements about](../../../../financial-statements/docs/releases/010/about.md)

## requirements

The aim of the personal finances app is to fulfill the financial reporting for personal finances 

1. accuracy, consistiency, up-to-date actual statements live and up-to-date net worth ledger
2. minimal friction for user at all stages of the workflow
3. drill down capability for analysis reporting, insights and improvement opportunities

__current workflow__

The current workflow is based on HomeBudget as the primary UI and storage for personal finance, with additional supporting tools - Google sheets, python scripts to interface with the HomeBudget app, run automations, custom UI for certain workflows and analysis and reporting.  One of the primary capabilities gap of the HomeBudget app is lack of an API, which limits capabilities for automation and customization.

__financial-statements 010__

The aim of the financial statements project "fin-stat 010" was to streamline many of these helper and supporting features, while still retaining HomeBudget as the primary UI and financial accounting storage, and retaining Google Sheets for many of the UI operations.  The development of the app stalled at the requirements and design stage without ever producing any working implementation.

some of the challenges encountered from the fin-stat 010 experience

01. design-heavy: delay too long to have useful prototype that does something for the user
02. backend-only: de-emphasis on UI
03. bespoke business logic: too much custom user-specific business logic and rules baked into the software design and requirements, rather than left to the user
04. two accounting classification heirarchies: separate HomeBudget and financial reporting heirarchies with complex mapping rules between the two
05. tech-stack lock-in: locked into integrating and working within constraints of existing brownfield components - Google sheets, HomeBudget

## workflows

01. record and classify transactions in real time using phone app
02. report financial statements: account balances net worth spending analysis compare vs plan
03. track recurring bills and forecast known txns
04. upload store ingest financial statements on monthly cycle
05. reconcile txns between actual statements and live ledger



