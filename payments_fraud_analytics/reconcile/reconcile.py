# -*- coding: utf-8 -*-
"""Reconcile payment records between an internal ledger and a gateway export."""

import pandas as pd
from pathlib import Path


# BEFORE (default):
#   col1  col2  col3  ...  col20
#   1     2     3     ...  20
#
# AFTER (with these settings):
#   col1  col2  col3  col4  col5  col6  col7  ...  col20   ← All columns visible!
#   1     2     3     4     5     6     7     ...  20
# ============================================================================

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

REQUIRED_COLUMNS = {"transaction_id", "amount_inr", "status"}
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

def _validate(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Return a normalized copy and validate the columns needed for reconciliation."""
    prepared = df.copy()
    print("data frame name :" ,name)
    print("data size: ", prepared.shape)

    # =========================
    # Cleaning
    # =========================
    prepared.columns = prepared.columns.str.strip().str.lower()
    missing_columns = REQUIRED_COLUMNS - set(prepared.columns)
    if missing_columns:
        raise ValueError(f"{name} is missing required columns: {sorted(missing_columns)}")
    # Normalizing TransactionIds this would help in comparison
    prepared["transaction_id"] = prepared["transaction_id"].astype(str).str.strip()
    # =========================
    # Basic validation
    # =========================
    if prepared["transaction_id"].isna().any() or (prepared["transaction_id"] == "").any():
        raise ValueError(f"{name} contains a blank transaction_id")
    if prepared["transaction_id"].duplicated().any():
        raise ValueError(f"{name} contains duplicate transaction_id values")

    prepared["amount_inr"] = pd.to_numeric(prepared["amount_inr"], errors="raise")
    prepared["status"] = prepared["status"].astype("string").str.strip()
    return prepared




def reconcile_payments(
        ledger_df: pd.DataFrame, gateway_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Reconcile ledger and gateway data and return the four discrepancy DataFrames."""

    # Work on copies so that the original DataFrames passed to the function are unchanged
    
    df_ledger = _validate(ledger_df,"ledger_df")
    df_gateway =_validate(gateway_df,"gateway_df")


    # =========================
    #  Cleaning
    # =========================

    for df in [df_ledger, df_gateway]:
        df.columns = df.columns.str.strip().str.lower()
        ## end of for loop

    df_ledger["transaction_id"] = df_ledger["transaction_id"].astype(str).str.strip()
    df_gateway["transaction_id"] = df_gateway["transaction_id"].astype(str).str.strip()

    # =========================
    # To find the difference of records between ledger and gateway, use Sets
    # =========================

    ## Create Set of ledger - transaction_ids, gateway - transaction_ids
    ledgerids_set = set(df_ledger["transaction_id"])
    gatewayids_set = set(df_gateway["transaction_id"])

    print(f"Unique IDs (cnt) in Ledger: {len(ledgerids_set)}")
    print(f"Unique IDs (cnt) in Gateway: {len(gatewayids_set)}")

    # =========================
    # Find ids missing in gateway, but present in ledger
    # =========================
    missing_ids_gateway = ledgerids_set - gatewayids_set
    print(f"Missing IDs (cnt) in Gateway: {len(missing_ids_gateway)}")
    print("Missing txn_ids in Gateway: ", missing_ids_gateway)

    # =========================
    # Find entire rows from ids above, missing in gateway, but present in ledger
    # =========================

    df_missing_ids_gateway = df_ledger[
        df_ledger["transaction_id"].isin(missing_ids_gateway)
    ]
    print("Missing df_IDs in Gateway: \n", df_missing_ids_gateway)

    # =========================
    # Find ids missing in ledger, but present in gateway
    # =========================
    missing_ids_ledger = gatewayids_set - ledgerids_set
    print(f"Missing IDs (cnt) in Ledger: {len(missing_ids_ledger)}")
    print("Missing txn_ids in Ledger: ", missing_ids_ledger)

    # =========================
    # Find entire rows from ids above, missing in ledger, but present in gateway
    # =========================

    df_missing_ids_ledger = df_gateway[
        df_gateway["transaction_id"].isin(missing_ids_ledger)
    ]
    print("Missing df_IDs in Ledger: \n", df_missing_ids_ledger)

    # =========================
    # To find the amount mismatches
    # =========================

    ## First join/merge ledger and gateway records (find the common records)

    common_df = pd.merge(
        df_ledger,
        df_gateway,
        on="transaction_id",
        how="inner",
        indicator=True,
        suffixes=("_ledger", "_gateway"),
    )

    mismatch_amount_rows = []
    common_df.head(15)

    for row in common_df.itertuples(index=False):
        if row.amount_inr_ledger != row.amount_inr_gateway:
            mismatch_amount_rows.append(row)

    df_mismatch_amount = pd.DataFrame(
        mismatch_amount_rows, columns=common_df.columns
    ).reset_index(drop=True)

    ## Compute the required difference as ledger amount minus gateway amount
    df_mismatch_amount["amount_difference"] = (
        df_mismatch_amount["amount_inr_ledger"]
        - df_mismatch_amount["amount_inr_gateway"]
    )

    print("Mismatch Amount txn count: ", len(df_mismatch_amount))
    print(
        "Txn with mismatch in Amounts between Ledger & Gateway: \n",
        df_mismatch_amount,
    )

    # =========================
    #To find the status mismatches
    # =========================

    mismatch_status_rows = []
    common_df.head(15)

    for row in common_df.itertuples(index=False):
        if row.status_ledger != row.status_gateway:
            mismatch_status_rows.append(row)

    # Retain the original notebook variable name
    df_status_amount = pd.DataFrame(
        mismatch_status_rows, columns=common_df.columns
    ).reset_index(drop=True)

    #print(df_status_amount)
    print("Mismatch Status txn count: ", len(df_status_amount))
    print(
        "Txn with mismatch Status between Ledger & Gateway: \n",
        df_status_amount,
    )

    return (
        df_missing_ids_gateway.reset_index(drop=True),
        df_missing_ids_ledger.reset_index(drop=True),
        df_mismatch_amount,
        df_status_amount,
    )


def main():
    print("Libraries loaded successfully!")
    print(f"Pandas version: {pd.__version__}")

    # =========================
    #  Load data
    # =========================

    # Read the ledger and gateway files from the folder containing this script
    project_folder = Path(__file__).resolve().parent
    df_ledger = pd.read_csv(DATA_DIR / "ledger.csv")
    df_gateway = pd.read_csv(DATA_DIR / "gateway_export.csv")

    # df_ledger = pd.read_csv("/content/ledger.csv")
    # df_gateway = pd.read_csv("/content/gateway_export.csv")

    (
        df_missing_ids_gateway,
        df_missing_ids_ledger,
        df_mismatch_amount,
        df_status_amount,
    ) = reconcile_payments(df_ledger, df_gateway)

    # =========================
    # Export the missing and mismatched records into csv files
    # =========================

    
    #df_missing_ids_gateway.to_csv(
    #    project_folder /"output" / "missing_in_gateway.csv", index=False
    #)
    #df_missing_ids_ledger.to_csv(
    #    project_folder / "output" / "missing_in_ledger.csv", index=False
    #)
    #df_mismatch_amount.to_csv(project_folder /"output" /  "amount_mismatches.csv", index=False)
    #df_status_amount.to_csv(project_folder / "output" / "status_mismatches.csv", index=False)

    # Report all four discrepancy counts
    print("\nReconciliation Summary")
    print("Missing in gateway: ", len(df_missing_ids_gateway))
    print("Missing in ledger (extra in gateway): ", len(df_missing_ids_ledger))
    print("Amount mismatches: ", len(df_mismatch_amount))
    print("Status mismatches: ", len(df_status_amount))


if __name__ == "__main__":
    main()
