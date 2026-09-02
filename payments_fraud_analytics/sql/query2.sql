-- 2. Quantify chargeback impact by calculating the total chargeback amount.
SELECT SUM(amount_inr) AS total_chargeback_amount
FROM ledger
WHERE LOWER(status) = 'chargeback';

-- O/P:  "54472"    
