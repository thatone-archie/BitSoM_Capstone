# Payments Fraud Analytics — SQL Queries

This directory contains six queries for analyzing chargebacks, affected users,
burner accounts, and transaction-velocity attacks in the payments ledger. Each
section below explains the query, links to its source SQL and generated CSV
output, and includes the SQL inline for convenient review.

## Query and output index

| Query | Analysis | SQL | Output |
| --- | --- | --- | --- |
| 1 | Count chargeback transactions | [query1.sql](query1.sql) | [query1.csv](output/query1.csv) |
| 2 | Calculate total chargeback value | [query2.sql](query2.sql) | [query2.csv](output/query2.csv) |
| 3 | Identify users affected by chargebacks | [query3.sql](query3.sql) | [query3.csv](output/query3.csv) |
| 4 | Identify burner accounts | [query4.sql](query4.sql) | [query4.csv](output/query4.csv) |
| 5 | Detect transaction-velocity attacks | [query5.sql](query5.sql) | [query5_and_6.csv](output/query5_and_6.csv) |
| 6 | Continue the Query 5 velocity analysis | [query6.sql](query6.sql) | [query5_and_6.csv](output/query5_and_6.csv) |

## 1. Count chargeback transactions

[View the SQL](query1.sql) · [View the output](output/query1.csv)

Counts all ledger transactions whose status is `chargeback`. The status is
converted to lowercase so the comparison is case-insensitive.

**Result:** 28 chargeback transactions.

```sql
SELECT COUNT(*) AS cnt_of_chargebacks
FROM ledger
WHERE LOWER(status) = 'chargeback';
```

## 2. Calculate total chargeback value

[View the SQL](query2.sql) · [View the output](output/query2.csv)

Quantifies the financial impact of chargebacks by summing `amount_inr` for all
ledger rows with chargeback status.

**Result:** INR 54,472 in chargebacks.

```sql
SELECT SUM(amount_inr) AS total_chargeback_amount
FROM ledger
WHERE LOWER(status) = 'chargeback';
```

## 3. Identify users affected by chargebacks

[View the SQL](query3.sql) · [View the output](output/query3.csv)

Groups chargeback transactions by user and status. For each affected user, it
reports the user's total chargeback amount and number of chargeback
transactions. The inner join ensures that each ledger user exists in the
`users` table.

**Result:** 27 rows, representing 27 unique affected users.

```sql
SELECT
    l.user_id,
    l.status,
    SUM(l.amount_inr) AS chargeback_amt,
    COUNT(*) AS chargeback_cnt
FROM ledger AS l
INNER JOIN users AS u
    ON l.user_id = u.user_id
WHERE LOWER(status) = 'chargeback'
GROUP BY
    l.user_id,
    l.status
ORDER BY u.user_id;
```

## 4. Identify burner accounts

[View the SQL](query4.sql) · [View the output](output/query4.csv)

Treats a user as a burner account when the account signup date is shortly
before a chargeback transaction. It calculates the number of days between the
signup and transaction dates, requires the signup to occur on or before the
transaction, and filters to the first 30 days.

The query's documented intended boundary is `0 <= days_difference < 30`.
However, SQLite's `BETWEEN 0 AND 30` is inclusive at both ends, so the SQL as
written also includes a transaction exactly 30 days after signup.

**Result:** 15 rows, representing 15 burner accounts in the seeded data.

```sql
SELECT
    l.user_id,
    DATE(l.transaction_time) AS DT_txn,
    DATE(u.signup_date) AS DT_sign,
    JULIANDAY(DATE(l.transaction_time))
        - JULIANDAY(DATE(u.signup_date)) AS days_difference
FROM users AS u
INNER JOIN ledger AS l
    ON u.user_id = l.user_id
WHERE LOWER(status) = 'chargeback'
  AND (
      JULIANDAY(DATE(l.transaction_time))
      - JULIANDAY(DATE(u.signup_date))
  ) BETWEEN 0 AND 30
ORDER BY (
    JULIANDAY(DATE(l.transaction_time))
    - JULIANDAY(DATE(u.signup_date))
);
```

## 5. Detect transaction-velocity attacks

[View the SQL](query5.sql) · [View the output](output/query5_and_6.csv)

Looks for users with three or more transactions in a 10-minute window. The CTE
first limits the search to user/date combinations containing at least three
transactions. The inner query orders those transactions, calculates the gap to
the next transaction in minutes, and the outer query retains qualifying groups
and reports their earliest transaction time.

The seeded data is expected to produce at least eight distinct velocity
clusters. Exact bucket boundaries can vary when overlapping 10-minute windows
are grouped using different valid approaches.

**Result:** eight user IDs with qualifying activity, together with each
cluster's start time.

```sql
WITH grp_by_day_cnt_grt_3 AS (
    SELECT
        l.user_id,
        DATE(l.transaction_time) AS txn_date,
        COUNT(*)
    FROM ledger AS l
    GROUP BY
        l.user_id,
        DATE(l.transaction_time)
    HAVING COUNT(*) >= 3
    ORDER BY
        l.user_id,
        l.transaction_time
)
SELECT
    t2.user_id,
    MIN(transaction_time) AS cluster_start_time
FROM (
    SELECT
        l.user_id,
        l.transaction_time,
        DATE(l.transaction_time),
        TIME(l.transaction_time),
        l.status,
        RANK() OVER (
            PARTITION BY l.user_id
            ORDER BY l.transaction_time ASC
        ) AS txn_time_rank,
        (
            LEAD(JULIANDAY(TIME(l.transaction_time)), 1) OVER (
                PARTITION BY l.user_id
                ORDER BY l.transaction_time ASC
            ) - JULIANDAY(TIME(l.transaction_time))
        ) * 1440 AS time_Diff
    FROM grp_by_day_cnt_grt_3 AS t1
    INNER JOIN ledger AS l
        ON t1.user_id = l.user_id
       AND txn_date = DATE(l.transaction_time)
    ORDER BY l.user_id
) AS t2
WHERE ROUND(t2.time_Diff) <= 10
   OR t2.time_Diff IS NULL
GROUP BY t2.user_id
HAVING COUNT(*) >= 3
ORDER BY t2.user_id;
```

## 6. Continue the Query 5 velocity analysis

[View the SQL](query6.sql) · [View the shared output](output/query5_and_6.csv)

Repeats the selection and grouping stage of Query 5 using the
`grp_by_day_cnt_grt_3` table produced by Query 5's `WITH` clause. It returns the
same eight user IDs and earliest cluster times, which is why Queries 5 and 6
share one output file.

> **Execution note:** As stored, `query6.sql` is a continuation fragment and is
> not standalone SQL. The `grp_by_day_cnt_grt_3` CTE exists only for the single
> statement that defines it, so execute the complete statement in
> [query5.sql](query5.sql) to reproduce the linked output.

```sql
SELECT
    t2.user_id,
    MIN(transaction_time) AS cluster_start_time
FROM (
    SELECT
        l.user_id,
        l.transaction_time,
        DATE(l.transaction_time),
        TIME(l.transaction_time),
        l.status,
        RANK() OVER (
            PARTITION BY l.user_id
            ORDER BY l.transaction_time ASC
        ) AS txn_time_rank,
        (
            LEAD(JULIANDAY(TIME(l.transaction_time)), 1) OVER (
                PARTITION BY l.user_id
                ORDER BY l.transaction_time ASC
            ) - JULIANDAY(TIME(l.transaction_time))
        ) * 1440 AS time_Diff
    FROM grp_by_day_cnt_grt_3 AS t1
    INNER JOIN ledger AS l
        ON t1.user_id = l.user_id
       AND txn_date = DATE(l.transaction_time)
    ORDER BY l.user_id
) AS t2
WHERE ROUND(t2.time_Diff) <= 10
   OR t2.time_Diff IS NULL
GROUP BY t2.user_id
HAVING COUNT(*) >= 3
ORDER BY t2.user_id;
```

## Run the database loader

The [database loader](load_payments_db.py) creates a fresh SQLite database from
the schema files and source CSV files. It uses only Python's standard library,
so no additional packages are required.

From the `sql` directory, run:

```bash
python3 load_payments_db.py
```

Alternatively, from the `payments_fraud_analytics` directory, run:

```bash
python3 sql/load_payments_db.py
```

The loader reads `merchants.csv`, `users.csv`, and `ledger.csv` from the
project's `data` directory. It builds and validates a temporary database before
replacing [database/paytm_payments.db](database/paytm_payments.db), then prints
the number of rows loaded into each table and the validation result.

> **Note:** Running the loader replaces the existing database after the new
> database passes its foreign-key and integrity checks.

## Schemas

- **Merchants table:** [schema/create_merchants.sql](schema/create_merchants.sql)
- **Users table:** [schema/create_users.sql](schema/create_users.sql)
- **Ledger table:** [schema/create_ledger.sql](schema/create_ledger.sql)

## Database

- **SQLite database:** [database/paytm_payments.db](database/paytm_payments.db)

## References

- [SQLite Online](https://sqliteonline.com/) — used to run and validate the SQL queries.
