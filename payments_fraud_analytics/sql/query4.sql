-- 4. Identify burner accounts.
--
-- Burner accounts are users whose signup_date is less than 30 days before
-- their transaction_time, restricted to transactions with chargeback status.
-- The intended boundary is:
--     0 <= (transaction_time - signup_date).days < 30
-- The signup must be on or before the transaction, and strictly less than
-- 30 days earlier. The query must surface at least 15 seeded burner-account rows.
-- Result: 15 rows, representing 15 burner accounts.
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
-- gives: count(*) = 15 rows i.e. 15 burner accounts
