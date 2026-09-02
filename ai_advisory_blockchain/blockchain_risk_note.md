# BitSoM Capstone Part 3 — AI-Augmented FinTech Advisory & Blockchain Risk

This section is for all the files for Part 3 of the capstone assignment.

## Included Files

- **Part D — DCF valuation calculator:** [`dcf_calculator.ipynb`](./dcf_calculator.ipynb)
- **Part E — Blockchain/crypto risk-analysis appendix:** [`blockchain_risk_note.md`](./blockchain_risk_note.md)

## Part D — DCF Valuation Calculator

The discounted-cash-flow valuation calculator is available in [`dcf_calculator.ipynb`](./dcf_calculator.ipynb). The notebook projects five years of FCFF, calculates WACC, estimates terminal value, discounts the cash flows to present value, provides a 3 × 3 sensitivity table, checks the WACC–terminal-growth constraint, and compares the DCF valuation with an EV/EBITDA multiple.

## Part E — Blockchain/Crypto Risk-Analysis Appendix

### 1. Paytm Crypto Insights Watchlist

> A short assessment of what a hypothetical “Paytm Crypto Insights” watchlist feature would need to get right on stablecoin type and DeFi/DAO governance risk before Paytm could responsibly surface it to retail users (reference the fiat-collateralized vs. algorithmic stablecoin distinction and tokenomics/DAO governance risks).

**Answer:**

Cryptocurrencies are digital, decentralized assets transacted globally on-chain without central banks or intermediaries. The transactions happen on a distributed ledger, and smart contracts (self-executing code) automatically carry out the agreed rules on the chain.

Bitcoin has shown extreme price movements and is a highly volatile asset.

Stablecoins are cryptocurrency tokens whose value is pegged to an underlying asset such as a fiat currency or a commodity. There are four types of stablecoins: fiat-collateralized, crypto-collateralized, commodity-backed, and algorithmic.

They are correlated to the underlying asset, making them more stable and reducing price volatility. A Paytm Crypto Insights watchlist should clearly distinguish fiat-collateralized stablecoins, which are supported by reserves, from algorithmic stablecoins, which depend on algorithms and market incentives to maintain their peg. The feature should explain that algorithmic stablecoins can be more vulnerable to losing their peg.

DeFi governance relies on Decentralized Autonomous Organizations (DAOs)—internet-based organizations in which community members propose, discuss, and vote on smart-contract-enforced rules. Any change to the rules still has to go through proposal, discussion, and voting.

Holding tokens can qualify someone to be part of the governance body. Good tokenomics is designed with a clear supply cap, a predictable issuance schedule, balanced allocation, transparent vesting, a clear voting and governance process, and a reward process for genuine activity. Before surfacing a token to retail users, Paytm should explain risks such as concentrated token ownership, unequal voting power, unclear vesting, excessive token issuance, and governance decisions controlled by a small number of participants.

### 2. Crypto as an Asset Class

> A crypto-as-an-asset-class recommendation for Paytm Money: using the standard finding that CAPM-style portfolio theory does not favor including an asset lacking intrinsic value/dividends, such as cryptocurrency, in an optimal portfolio, together with low/negative correlation with traditional assets, heavy-tailed/positively-skewed returns, survivorship bias, and high transaction costs, state a specific, justified maximum allocation percentage (or a justified “zero allocation”) recommendation for a retail advisory product.

**Answer:**

CAPM is a model that estimates the expected return of an asset, given its volatility (beta) relative to the market.

Traditional tools such as CAPM and the Gordon Growth Model advise against holding crypto because it generates no earnings or dividends. Looking at crypto through these two lenses implies not holding crypto at all because there are no underlying earnings; crypto is simply a mode of exchange.

However, empirically, cryptocurrency shows high average returns, high standard deviation, positively skewed return distributions, and a beta relative to the S&P 500 that is less than one. The same traditional theories advise against holding cash, and yet people do. From 2017–2021, the price appreciation of Bitcoin was 284%, much higher than gold or the S&P 500. With increased clarity in crypto regulation, many institutions invested in Bitcoin.

A Goldman Sachs simulation showed that reallocating 2.5% of a 60/40 portfolio to Bitcoin boosted annualized returns by 165 basis points. While the simulation results showed good portfolio returns, they ignored the cost of investing in Bitcoin and its risks. Cryptocurrency transaction costs can be very high.

**Survivorship bias:** Calculating returns from the top two or three cryptocurrencies and assuming the same effect for the many other cryptocurrencies available.

**Concentration risk:** There is no mechanism that prevents large institutions from holding large amounts of crypto; therefore, concentration risk remains an open, unresolved issue.

Bitcoin shows a positively skewed return distribution, as a small number of exceptional days pulled the mean above the median, while on most days the return was low or negative. Crypto returns can also be heavy-tailed, meaning extreme gains and losses occur more frequently than a normal distribution would suggest.

Yet crypto can appeal to many investors for reasons such as hedging and portfolio diversification, including its low or negative correlation with some traditional assets. Investing in crypto should be measured according to an individual’s time horizon and risk-taking appetite. Even when an asset is highly volatile, it can be worth holding if its returns compensate for its risk.

Crypto assets are not safe; they are speculative assets. I recommend that Paytm allow a cautious allocation of **no more than 5%** for suitable retail investors for reasons such as hedging and diversification, while continuously monitoring the investment. A lower allocation, including zero, would be more appropriate for conservative investors or those with a short time horizon.

### 3. T.A.N.G. Fraud Framework

> A short section applying the T.A.N.G. (Temptation/Authority/Need/Greed) fraud framework to identify the two social-engineering risk vectors you consider most relevant to a UPI/wallet + lending + wealth platform specifically, and one bank-side real-time defense mechanism that mitigates each.

**Answer:**

Cybersecurity protects systems and devices, networks, and data. Cyber fraud is about deceiving people to gain access to their money, identity, and accounts. Both are required to combat fraud and scams.

Social-engineering scams exploit human psychology using the T.A.N.G. framework:

- **Temptation:** Unrealistic, low-effort riches.
- **Authority:** Impersonating trusted authorities.
- **Need:** Creating artificial urgency.
- **Greed:** Promising outsized returns.

The two most relevant risk vectors for a UPI/wallet, lending, and wealth platform are the following:

#### Risk Vector 1 — Authority and Need

For a UPI/wallet digital-payment system, it is easy to trick people with a QR code that sends a payment to a fraudster’s account. A scammer may impersonate bank or platform support and create urgency by claiming that KYC must be updated, an account will be blocked, or a refund must be collected immediately. Being cautious and checking before making payments can reduce the risk of sending money to the wrong user. If someone is creating urgency, step back and analyze.

**Bank-side real-time defense:** Banks can use real-time transaction monitoring and AI-based user-behavior anomaly detection. Signals can include SIM-card status, device ID, location, IP address, a new beneficiary, and unusual payment behavior. A high-risk transaction can be paused and subjected to additional verification. Payment apps can also use defenses such as screen-share blackouts. Banks require authentication to confirm payments; users should not share an OTP or password or click links received from suspicious sources.

#### Risk Vector 2 — Temptation and Greed

For lending and wealth platforms, a user may receive an offer from a fake lender or lending app, or an investment offer promising returns that are too good to be true. Users should check the source of the information, keep their apps updated, install antivirus software, and avoid links that lead to unrealistic offers. If an opened link tries to gain remote access to a device, the user should go into the phone’s settings and disable remote access.

**Bank-side real-time defense:** Banks can use AI to identify fraudulent burner and mule accounts through beneficiary-risk scoring, transaction-velocity analysis, and unusual movement of funds. Transfers to a high-risk recipient can be delayed, blocked, or escalated for verification before the money leaves the customer’s account.

Any social-engineering scam thrives on impulsive action: stop, think, verify, and then act.

For a wealth platform, users should protect their accounts with at least two-factor authentication (2FA), such as a password combined with biometrics or an OTP. They should check account statements regularly to flag anything suspicious, never share authentication details, change passwords regularly, use strong passwords, and avoid reusing the same password across different apps.

Every payment transaction is monitored for fraud and anomalies by banks before it is authenticated and authorized. Banks use AI for user-behavior anomaly detection and document verification. Banks also invest in awareness programs to keep their stakeholders safe. Awareness, behavioral controls, and safe habits can act as strong defenses against scams.
