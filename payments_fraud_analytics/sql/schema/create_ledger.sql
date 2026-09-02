CREATE TABLE ledger (transaction_id TEXT PRIMARY KEY, user_id INTEGER, merchant_id INTEGER, transaction_time TEXT, amount_inr INTEGER, payment_method TEXT, status TEXT, risk_score INTEGER,FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
 )