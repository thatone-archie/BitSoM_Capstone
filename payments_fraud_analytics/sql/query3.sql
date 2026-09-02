-- 3. Identify unique users affected by chargeback transactions.
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
-- gives: count = 27 rows i.e. 27 unique users
