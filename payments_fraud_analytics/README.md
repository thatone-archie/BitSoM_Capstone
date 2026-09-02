# BitSoM Fintech & AI Capstone — Payments & Fraud Analytics

This repository contains the Paytm payments deliverables:

- **Source data:** the project CSV files are generated and stored in the shared
  [`data/`](data/) directory.
- **Excel/Sheets analysis:** [`merchant_workbook.xlsx`](merchant_workbook.xlsx)
  contains the cleaned merchant workbook, formulas, pivot table, and fee-tier
  lookup.
- **SQL fraud analysis:** SQLite schemas and queries identify chargebacks,
  affected users, burner accounts, and transaction-velocity patterns.
- **Python reconciliation:** a reusable function compares the ledger with the
  gateway export and returns four discrepancy DataFrames.
- **Analytics dashboard:** Python produces four layers of PNG scorecards,
  trends, details, and breakdown charts; this is not a live BI tool.
- **Runtime:** the Python files were developed from Google Colab work and can be
  executed in a standard Python environment.

- **Reading the visuals:** generated images contain explanatory text for each
  scorecard or chart. Open the images or the linked Markdown documents to read
  the complete commentary.

### Deliverables and reference documents

| Part | Deliverable | Main artifact | Reference documentation |
| --- | --- | --- | --- |
| [Part A](#part-a--excelsheets-merchant-workbook) | Excel/Sheets merchant workbook | [`merchant_workbook.xlsx`](merchant_workbook.xlsx) | [Part A notes in this README](#part-a--excelsheets-merchant-workbook) |
| [Part B](#part-b--sql-fraud-pattern-detection) | SQL fraud-pattern detection | [`sql/`](sql/) | [`analytics.md`](sql/analytics.md) |
| [Part C](#part-c--python-payment-reconciliation) | Python payment reconciliation | [`reconcile.py`](reconcile/reconcile.py) | [Part C instructions in this README](#part-c--python-payment-reconciliation) |
| [Part D](#part-d--four-layer-analytics-dashboard-code-generated-not-a-live-bi-tool) | Four-layer analytics dashboard | [`dashboard.py`](dashboard/dashboard.py) | [`dashboard.md`](dashboard/dashboard.md) |

## Part A — Excel/Sheets merchant workbook

[`merchant_workbook.xlsx`](merchant_workbook.xlsx) is the spreadsheet
deliverable. It combines transaction data with merchant attributes and
demonstrates lookup, pivot-table, and conditional-classification techniques.

### Workbook logic

- The `merchant_name`, `category`, and `region` columns use `VLOOKUP`.
- The `MDR%` column uses `HLOOKUP` and refers to the `mdr table` sheet for the
  fee-tier lookup.
- `merchant_day_total` is pulled from the `Pivot_merchant_txndate` pivot-table
  sheet. The grouping uses a compound `merchant_id + transaction date` key.
- The `classification` column demonstrates `IF`/`AND`. When
  `merchant_day_total > 5000` and the region is not `East`, the merchant and day
  are classified as `High-Value Merchant Day`.

### Fee tier used

| Payment Method | Wallet | UPI | Netbanking | Card |
| --- | ---: | ---: | ---: | ---: |
| MDR Rate | 1.50% | 0% | 1% | 2% |

### Install and run setup

Use Python 3.9 or newer. From the `payments_fraud_analytics` project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

#### Primary step: generate the shared source data

[`data/generate_data.py`](data/generate_data.py) is the primary step for the
entire workflow. It uses fixed Python and NumPy random seeds (`42`) to generate
the merchant, user, ledger, and deliberately discrepant gateway datasets used
by Parts A–D.

The generator writes its CSV files to the current working directory, so run it
from inside `data/`:

```bash
cd data
python3 generate_data.py
cd ..
```

It creates or overwrites these shared inputs:

- `merchants.csv` — merchant names, categories, and regions;
- `users.csv` — established users plus injected burner accounts;
- `ledger.csv` — baseline payments plus burner-account chargebacks and eight
  transaction-velocity clusters; and
- `gateway_export.csv` — a ledger-derived export with intentionally missing,
  extra, amount-mismatched, and status-mismatched records for reconciliation.

Because the generator overwrites the existing CSV files, preserve a copy first
if you have manually changed the data.

#### Run the downstream deliverables

After generating the data, run the three code deliverables as individual
scripts from the project root:

```bash
python3 sql/load_payments_db.py
python3 reconcile/reconcile.py
python3 dashboard/dashboard.py
```

### Design decisions

- **Generate once, consume everywhere:** `generate_data.py` creates
  `ledger.csv`, `gateway_export.csv`, `merchants.csv`, and `users.csv` in the
  shared [`data/`](data/) folder. The SQL loader, reconciliation script, and
  dashboard resolve this directory relative to the project, so every module
  uses the same inputs and there is no need to upload or duplicate CSV files
  for each script.
- **One dependency file:** [`requirements.txt`](requirements.txt) is the single
  source for the project's Python packages.
- **Individual script entry points:** the SQL loader, reconciliation process,
  and dashboard can be reviewed and run independently. No application server
  or live notebook session is required.
- **Reusable reconciliation logic:** file loading and terminal output stay in
  `main()`, while `reconcile_payments()` accepts DataFrames and can be imported
  without automatically executing the command-line workflow.

## Part B — SQL fraud-pattern detection

The SQL deliverable creates a SQLite database from the shared CSV files and
contains six analyses covering chargebacks, affected users, burner accounts,
and transaction-velocity attacks. The complete explanations, SQL text, outputs,
schema links, and database link are available in
[`sql/analytics.md`](sql/analytics.md).

### Query and output index

| Query | Analysis | SQL | Generated output |
| --- | --- | --- | --- |
| 1 | Count chargeback transactions | [`query1.sql`](sql/query1.sql) | [`query1.csv`](sql/output/query1.csv) |
| 2 | Calculate total chargeback value | [`query2.sql`](sql/query2.sql) | [`query2.csv`](sql/output/query2.csv) |
| 3 | Identify users affected by chargebacks | [`query3.sql`](sql/query3.sql) | [`query3.csv`](sql/output/query3.csv) |
| 4 | Identify burner accounts | [`query4.sql`](sql/query4.sql) | [`query4.csv`](sql/output/query4.csv) |
| 5 | Detect transaction-velocity attacks | [`query5.sql`](sql/query5.sql) | [`query5_and_6.csv`](sql/output/query5_and_6.csv) |
| 6 | Continue the Query 5 velocity analysis | [`query6.sql`](sql/query6.sql) | [`query5_and_6.csv`](sql/output/query5_and_6.csv) |

### Build and run

The SQL schemas must be applied before the analysis queries. The database loader
does this in the correct order, loads the CSVs from `data/`, validates foreign
keys and database integrity, and then creates
[`sql/database/paytm_payments.db`](sql/database/paytm_payments.db):

```bash
python3 sql/load_payments_db.py
```

The loader uses only the Python standard library. Run a standalone query with
the SQLite command-line tool, for example:

```bash
sqlite3 -header -column sql/database/paytm_payments.db < sql/query1.sql
```

`query6.sql` is a continuation fragment that depends on the CTE defined in
`query5.sql`; run `query5.sql` to reproduce their shared output.

### How the 10-minute window was defined

The intended fraud rule is **three or more transactions by the same user within
an inclusive 10-minute window**. The supplied seed data makes the expected
pattern unambiguous by injecting eight clusters of four transactions spaced one
minute apart—four transactions inside a five-minute period.

In [`query5.sql`](sql/query5.sql), the implementation:

1. prefilters user/date groups containing at least three transactions;
2. orders each user's transactions by `transaction_time`;
3. uses `LEAD()` to calculate the next-transaction gap and multiplies the
   SQLite Julian-day difference by 1,440 to convert it to minutes;
4. treats a rounded adjacent gap of 10 minutes or less as qualifying; and
5. retains users with at least three qualifying rows and reports the earliest
   transaction as `cluster_start_time`.

The comparison is inclusive (`<= 10`). Because velocity windows can overlap,
other valid fixed-bucket or rolling-window implementations can produce slightly
different boundaries while still identifying the eight seeded clusters.

Read the full embedded SQL analysis and result commentary in
[`sql/analytics.md`](sql/analytics.md).

## Part C — Python payment reconciliation

[`reconcile/reconcile.py`](reconcile/reconcile.py) compares the internal ledger
with the gateway export using `transaction_id`. It validates required columns,
normalizes identifiers, rejects blank or duplicate transaction IDs, converts
amounts to numeric values, uses set differences for missing records, and
compares amount and status fields for IDs present in both files.

### Run instructions

After installing `requirements.txt`, run from the project root:

```bash
python3 reconcile/reconcile.py
```

The script automatically reads [`data/ledger.csv`](data/ledger.csv) and
[`data/gateway_export.csv`](data/gateway_export.csv). It prints the detailed
discrepancies and then a summary. With the supplied data, the result is:

```text
Missing in gateway: 27
Missing in ledger (extra in gateway): 10
Amount mismatches: 16
Status mismatches: 9
```

The CLI does not write reconciliation CSV files by default; optional export
examples are present as commented code in `main()`.

### Import the reusable function

A reusable function does not mean that reconciliation must be run repeatedly.
It means separating reconciliation logic from file loading and terminal output.
`reconcile_payments(ledger_df, gateway_df)` works with any ledger and gateway
DataFrames, not only the two supplied CSV files. It can be imported into a
notebook, another script, a test, or an automated pipeline:

```python
import pandas as pd

from reconcile.reconcile import reconcile_payments

ledger_df = pd.read_csv("data/ledger.csv")
gateway_df = pd.read_csv("data/gateway_export.csv")

(
    missing_in_gateway,
    missing_in_ledger,
    amount_mismatches,
    status_mismatches,
) = reconcile_payments(ledger_df, gateway_df)
```

Importing the function does not rerun the file-loading or CLI-printing code. It
is also easy to test with small DataFrames.

### What `reconcile_payments()` returns

The function works on copies, leaving the input DataFrames unchanged, and
returns four discrepancy DataFrames as a tuple:

| Position | DataFrame | Contents |
| ---: | --- | --- |
| 1 | `missing_in_gateway` | Full ledger rows whose `transaction_id` is absent from the gateway export |
| 2 | `missing_in_ledger` | Full gateway rows whose `transaction_id` is absent from the ledger |
| 3 | `amount_mismatches` | Joined rows present in both inputs where the amounts differ; includes `amount_difference`, calculated as ledger amount minus gateway amount |
| 4 | `status_mismatches` | Joined rows present in both inputs where the statuses differ |

Returning DataFrames lets callers inspect, test, filter, export, visualize, or
analyze each discrepancy group.

## Part D — Four-layer analytics dashboard (code-generated, not a live BI tool)

The dashboard is a reproducible set of PNG artifacts generated by
[`dashboard/dashboard.py`](dashboard/dashboard.py) with pandas and Matplotlib.
It is **not a live BI dashboard**. Rerunning the script recalculates the metrics
from the shared CSV files and overwrites the images in
[`dashboard/screenshots/`](dashboard/screenshots/).

Run it from the project root:

```bash
python3 dashboard/dashboard.py
```

The full metric definitions, interpretations, and embedded visuals are in
[`dashboard/dashboard.md`](dashboard/dashboard.md).

### 1. Headline layer

Scorecards show total GMV, success rate, reconciliation match rate, and
chargeback ratio.

[![Headline-layer scorecards](dashboard/screenshots/Headline_layer_scorecards.png)](dashboard/screenshots/Headline_layer_scorecards.png)

### 2. Trends layer

Daily GMV and daily chargeback count are plotted across the 30-day analysis
period.

[![Daily GMV over time](dashboard/screenshots/trends_layer_daily_gmv_over_time.png)](dashboard/screenshots/trends_layer_daily_gmv_over_time.png)

[![Daily chargeback count](dashboard/screenshots/trends_layer_daily_chargeback_count.png)](dashboard/screenshots/trends_layer_daily_chargeback_count.png)

### 3. Details layer

The top 10 merchants by transaction count are rendered as a table, with a flag
for merchants whose count-based chargeback ratio exceeds 1%.

[![Top merchants details table](dashboard/screenshots/details_layer_table.png)](dashboard/screenshots/details_layer_table.png)

### 4. Breakdown layer

Bar charts compare GMV by payment method and by merchant category.

[![GMV by payment method](dashboard/screenshots/breakdown_layer_gmv_by_payment_method.png)](dashboard/screenshots/breakdown_layer_gmv_by_payment_method.png)

[![GMV by merchant category](dashboard/screenshots/breakdown_layer_%20gmv_by_merchant_category.png)](dashboard/screenshots/breakdown_layer_%20gmv_by_merchant_category.png)

For image-by-image explanations, open the complete
[`dashboard/dashboard.md`](dashboard/dashboard.md) documentation.
