# BitSoM Fintech & AI Capstone

This repository contains three independent capstone modules covering payments
and fraud analytics, credit-risk and lending machine learning, and
AI-augmented advisory with blockchain risk. Each part can be reviewed and run
on its own.

## Project parts

| Part | Module | What it contains |
| --- | --- | --- |
| 1 | [Payments & Fraud Analytics](payments_fraud_analytics/README.md) | Merchant analysis, SQL fraud detection, payment reconciliation, and a code-generated analytics dashboard |
| 2 | [Credit Risk & Lending ML](credit_risk_lending_ml/README.md) | Credit-risk EDA, classification, risk-based pricing, and transaction anomaly detection |
| 3 | [AI Advisory & Blockchain Risk](ai_advisory_blockchain/README.md) | A DCF valuation notebook and a blockchain/crypto risk-analysis appendix |

## Part 1 — Payments & Fraud Analytics

```bash
cd payments_fraud_analytics
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip

# Optional: regenerate the shared input data.
(cd data && python3 generate_data.py)

# Run the code deliverables.
python3 sql/load_payments_db.py
python3 reconcile/reconcile.py
python3 dashboard/dashboard.py
```

The data generator overwrites the existing CSV inputs. See the
[Part 1 README](payments_fraud_analytics/README.md) for the generated outputs,
SQL query instructions, reconciliation API, and dashboard documentation.

## Part 2 — Credit Risk & Lending ML

```bash
cd credit_risk_lending_ml
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip

# Optional: regenerate both input datasets.
(cd data && python3 generate_data.py)

# Launch the notebooks interactively.
python3 -m jupyter lab
```

To execute both notebooks non-interactively and save their results, follow the
`nbconvert` commands in the
[Part 2 build and run guide](credit_risk_lending_ml/README.md#first-time-setup-and-command-line-execution).

## Part 3 — AI Advisory & Blockchain Risk

```bash
cd ai_advisory_blockchain
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip

# Open and run the DCF calculator interactively.
python3 -m jupyter lab dcf_calculator.ipynb
```

The DCF notebook uses the CSV files stored alongside it. The blockchain and
crypto analysis is a Markdown deliverable and requires no build step; read
[the risk-analysis appendix](ai_advisory_blockchain/blockchain_risk_note.md)
directly.

Run all remaining commands from the selected module's directory so relative
data and output paths resolve correctly.
