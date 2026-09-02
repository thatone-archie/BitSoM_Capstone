# BitSoM Capstone Part 3 — AI-Augmented FinTech Advisory & Blockchain Risk

This section is for all the files for Part 3 of the capstone assignment.

## Included Files

- **Part D — DCF valuation calculator:** [`dcf_calculator.ipynb`](./dcf_calculator.ipynb)
- **Part E — Blockchain/crypto risk-analysis appendix:** [`blockchain_risk_note.md`](./blockchain_risk_note.md)

## Part D — DCF Valuation Calculator

The discounted-cash-flow valuation calculator is available in [`dcf_calculator.ipynb`](./dcf_calculator.ipynb). The notebook projects five years of FCFF, calculates WACC, estimates terminal value, discounts the cash flows to present value, provides a 3 × 3 sensitivity table, checks the WACC–terminal-growth constraint, and compares the DCF valuation with an EV/EBITDA multiple.

## Part E — Blockchain/Crypto Risk-Analysis Appendix

### 1. Paytm Crypto Insights Watchlist

Cryptocurrencies are digital, decentralized assets transacted globally on-chain. Transactions happen on a distributed ledger, and smart contracts automatically carry out agreed rules. Bitcoin has shown extreme price movements and is highly volatile.

Stablecoins are cryptocurrency tokens whose value is pegged to an underlying asset such as a fiat currency or commodity. There are four types: fiat-collateralized, crypto-collateralized, commodity-backed, and algorithmic. This can reduce price volatility. Paytm must explain that a fiat-collateralized stablecoin is backed by reserves, while an algorithmic stablecoin depends on algorithms and market incentives and can be more vulnerable to collapse.

DeFi governance relies on Decentralized Autonomous Organizations (DAOs)—internet-based organizations in which community members propose, discuss, and vote on smart-contract-enforced rules. Any change to the rules still has to go through proposal, discussion, and voting.

Holding tokens can qualify someone to be part of the governance body. Good tokenomics is designed with a clear supply cap, predictable issuance schedule, balanced allocation, transparent vesting, a clear voting and governance process, and rewards for genuine activity. Before surfacing a token to retail users, Paytm should clearly show these factors and warn users about concentrated ownership, unequal voting power, unclear vesting, excessive issuance, smart-contract risk, and governance controlled by a small number of participants.

### 2. Crypto as an Asset Class

CAPM is a model that estimates the expected return of an asset, given its volatility (beta) relative to the market. Traditional tools such as CAPM and the Gordon Growth Model advise against holding crypto because it generates no earnings or dividends. Looking at crypto through these two lenses implies not holding crypto at all because there are no underlying earnings; crypto is simply a mode of exchange.

However, empirically, cryptocurrency shows high average returns, high standard deviation, positively skewed return distributions, and a beta relative to the S&P 500 that is less than one. The same traditional theories advise against holding cash, and yet people do. From 2017–2021, the price appreciation of Bitcoin was 284%, much higher than gold or the S&P 500. With increased clarity in crypto regulation, many institutions invested in Bitcoin.

A Goldman Sachs simulation showed that reallocating 2.5% of a 60/40 portfolio to Bitcoin boosted annualized returns by 165 basis points. While the simulation showed good portfolio returns, it ignored the cost and risks of investing in Bitcoin. Cryptocurrency transaction costs can be very high.

**Survivorship bias:** Calculating returns from the top two or three cryptocurrencies and assuming the same effect for the many other cryptocurrencies available.

**Concentration risk:** There is no mechanism that prevents large institutions from holding large amounts of crypto; therefore, concentration risk remains an open, unresolved issue.

Bitcoin shows a positively skewed and heavy-tailed return distribution: a small number of exceptional days pull the mean above the median, while on most days returns are low or negative. Yet crypto can appeal to investors for hedging and portfolio diversification because of its low or negative correlation with some traditional assets.

Investing in crypto should be measured according to an individual’s time horizon and risk-taking appetite. Even when an asset is highly volatile, it can be worth holding if its returns compensate for its risk. Crypto assets are not safe; they are speculative assets. I recommend that Paytm allow a cautious allocation of **no more than 5%** for suitable retail investors for hedging and diversification, with continuous monitoring. A lower allocation, including zero, is more appropriate for conservative investors.

### 3. T.A.N.G. Fraud Framework

Cybersecurity protects systems, networks, and data. Cyber fraud deceives people to gain access to their money, identity, and accounts. Both must be addressed.

Social-engineering scams exploit human psychology using the T.A.N.G. framework:

- **Temptation:** Unrealistic, low-effort riches.
- **Authority:** Impersonating trusted authorities.
- **Need:** Creating artificial urgency.
- **Greed:** Promising outsized returns.

#### Risk Vector 1 — Authority and Need

For a UPI/wallet system, it is easy to trick people with a QR code that sends payment to a fraudster’s account. A scammer may impersonate bank support and create urgency by claiming that KYC must be updated, an account will be blocked, or a refund must be collected. If someone creates urgency, step back and analyze.

**Bank-side real-time defense:** Banks can use real-time transaction monitoring and AI-based user-behavior anomaly detection. Signals include SIM-card status, device ID, location, IP address, a new beneficiary, remote screen sharing, and unusual payment behavior. A high-risk transaction can be paused for additional verification. Do not share an OTP or password or click links received from suspicious sources.

#### Risk Vector 2 — Temptation and Greed

For lending and wealth platforms, a user may receive an offer from a fake lender or lending app, or an investment offer promising returns that are too good to be true. Users should check the source, keep apps updated, and avoid links leading to unrealistic offers or requesting remote access.

**Bank-side real-time defense:** Banks can use AI to identify fraudulent burner and mule accounts through beneficiary-risk scoring, transaction-velocity analysis, and unusual movement of funds. Transfers to a high-risk recipient can be delayed, blocked, or escalated for verification.

Any social-engineering scam thrives on impulsive action: stop, think, verify, and then act. Users should protect wealth accounts with two-factor authentication, check statements regularly, use strong passwords, and avoid reusing passwords. Awareness, behavioral controls, and safe habits can act as strong defenses against scams.
