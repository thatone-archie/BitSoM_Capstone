-- 6. Continue Query 5 using the table created by its WITH clause.
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
