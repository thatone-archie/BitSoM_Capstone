-- 5. Detect velocity attacks: users with 3 or more transactions within
-- any 10-minute window.
--
-- The query must surface at least eight seeded velocity clusters. When results
-- are grouped by user_id and a rounded or floored 10-minute transaction-time
-- bucket, all eight seeded clusters must appear as distinct qualifying groups.
-- Each cluster is identified by its victim user_id and earliest transaction_time.
-- Exact row counts and bucket boundaries may vary because overlapping windows
-- can be grouped in multiple reasonable ways.
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

-- Output: 8 user IDs with three or more transactions in a 10-minute window,
-- together with each cluster's start time.
