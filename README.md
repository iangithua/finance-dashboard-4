# Finance Dashboard

A personal finance pipeline for importing bank statement CSV files, classifying transactions,
storing them in SQLite, and generating Excel/CSV reports.

## What it does

1. Reads bank statement CSV files from `input/statements/`
2. Cleans dates, amounts, descriptions, and months
3. Applies classification rules from `input/rules/classification_rules.csv`
4. Ignores internal transfers such as Pocket/Flexible Cash Fund movements
5. Stores transactions in SQLite
6. Generates:
   - Excel dashboard
   - CSV dashboard
   - categorized transaction file
   - monthly cash-flow report
   - money leak report

## Folder structure

```text
finance-dashboard/
├── input/
│   ├── statements/
│   ├── rules/
│   └── goals/
├── database/
├── output/
│   ├── excel/
│   ├── csv/
│   ├── charts/
│   └── monthly_reports/
├── config/
├── src/
│   └── finance_dashboard/
├── tests/
├── requirements.txt
└── README.md
```

## Setup

```bash
cd finance-dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Put your Revolut CSV file into:

```text
input/statements/
```

Then run:

```bash
python -m src.finance_dashboard.main
```

Outputs will be created in:

```text
output/excel/
output/csv/
output/monthly_reports/
```

## Editing classification rules

Edit:

```text
input/rules/classification_rules.csv
```

Example:

```csv
keyword,category,group,ignore,confidence
Ian Githua,Rent,Needs,false,high
LemFi,Money to Kenya,Support,false,high
Pocket,Internal Transfer,Internal,true,high
```

Rules are matched by checking whether `keyword` appears inside the transaction description.

## Recommended workflow

1. Export a monthly CSV statement from Revolut.
2. Put it in `input/statements/`.
3. Run the project.
4. Open the generated Excel dashboard.
5. Review `Unclassified Transactions`.
6. Add new rules.
7. Re-run the project.

## Future upgrades

- Vaadin/Spring Boot dashboard
- PostgreSQL database
- Multiple bank accounts
- Subscription detection
- Payday-to-payday cash flow
- Forecasting
- Financial health score improvements

## Charts

Every run now generates chart images in:

```text
output/charts/
```

Current charts:

- `monthly_cash_flow.png` — income, expenses, and net cash flow over time
- `top_spending_categories.png` — biggest spending categories
- `spending_by_group.png` — needs/wants/support grouping
- `money_leaks.png` — small purchases that add up

The generated Excel file also contains a **Charts** sheet where these charts are embedded.

## Suggested finance charts to add later

- Payday-to-payday cash balance
- Subscription trend
- Spending by weekday
- Spending by merchant
- Savings goal progress
- Emergency fund runway

## Unclassified transaction review UI

The project includes a small Streamlit UI for correcting unclassified transactions
and saving the result as reusable rules.

Run:

```bash
streamlit run ui/review_unclassified.py
```

Or:

```bash
./run_review_ui.sh
```

Workflow:

```text
1. Run the pipeline
2. Open the review UI
3. Select an unclassified transaction
4. Create a keyword rule
5. Save the rule
6. Re-run the pipeline
7. Future statements classify automatically
```

Example:

```text
Description: Ian Githua Passau
Keyword: Ian Githua
Category: Rent
Group: Needs
Ignore: false
```

The rule is saved into:

```text
input/rules/classification_rules.csv
```

This creates a feedback loop:

```text
Unclassified transaction
    ↓
Human review
    ↓
New rule saved
    ↓
Future automatic classification
```
