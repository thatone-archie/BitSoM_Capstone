-- count of chargeback transactions

-- 1. Query to get count of chargebacks:
SELECT  count(*) as cnt_of_chargebacks FROM ledger
where  lower(status) = 'chargeback' ;
-- O/P:   "28"