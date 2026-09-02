# AI-Augmented FinTech Advisory and Blockchain Risk

This folder contains the deliverables for Parts D and E of the capstone assignment.

## Included files

- **Part D — DCF valuation calculator:** [`dcf_calculator.ipynb`](./dcf_calculator.ipynb)
- **Part E — Blockchain/crypto risk-analysis appendix:** [`blockchain_risk_note.md`](./blockchain_risk_note.md)

## Part D — DCF valuation calculator

The accompanying [`dcf_calculator.ipynb`](./dcf_calculator.ipynb) presents an illustrative five-year discounted-cash-flow valuation. It calculates unlevered Free Cash Flow to the Firm (FCFF) as:

> **FCFF = EBIT × (1 − tax rate) + D&A − CapEx − ΔNet Working Capital**

The notebook projects cash flows over five years using a fading growth path, computes the cost of equity with CAPM, and blends it with an illustrative after-tax cost of debt to obtain WACC. It then estimates terminal value using the growing-perpetuity method, discounts the forecast cash flows and terminal value to the present, and reports enterprise and equity value. A 3 × 3 sensitivity table varies WACC and terminal growth by ±1 percentage point. The notebook also checks that WACC remains above terminal growth in the most aggressive sensitivity case and compares the DCF result with an illustrative EV/EBITDA valuation.

## Part E — Blockchain/crypto risk-analysis appendix

### 1. “Paytm Crypto Insights”: stablecoin and governance risks

Before Paytm responsibly surfaces a hypothetical “Crypto Insights” watchlist to retail users, it should distinguish clearly between stablecoin designs. A **fiat-collateralized stablecoin** seeks to maintain its peg through reserves—such as cash and short-term government securities—held by an issuer or custodian. Its principal risks include inadequate or low-quality reserves, weak attestations, redemption restrictions, custodial failure, regulatory action, and loss of confidence in the issuer. Paytm should therefore display the reserve composition, frequency and independence of attestations, redemption rights, issuer jurisdiction, liquidity, and any history of de-pegging. The label “stable” must not be presented as equivalent to “risk-free.”

An **algorithmic stablecoin**, by contrast, relies primarily on incentives, supply adjustments, arbitrage, or a linked token rather than fully matched fiat reserves. Such a design can enter a reflexive failure cycle: confidence falls, redemptions increase, the supporting token declines, and the mechanism loses the capacity to restore the peg. Paytm should classify these products separately, provide prominent warnings, and avoid implying that their historical price stability is a guarantee.

The watchlist must also explain **tokenomics and DeFi/DAO governance risk**. Relevant indicators include token supply caps, issuance and inflation schedules, insider and treasury allocations, vesting and unlock dates, liquidity concentration, and the sustainability of staking or incentive rewards. Governance tokens do not necessarily provide shareholder-like rights or claims on cash flow. Voting power may be concentrated among founders, venture investors, delegates, or large token holders; low participation can allow a small group to change fees, collateral rules, treasury use, or smart-contract parameters. Paytm should surface governance concentration, admin-key and upgrade powers, voting participation, audit status, oracle and bridge dependencies, and material proposal history. Information should be educational and risk-ranked, not framed as an endorsement or promise of safety.

### 2. Crypto as an asset class: recommendation for Paytm Money

For a mainstream retail advisory product, I recommend a **maximum strategic allocation of 1% of an investable portfolio**, available only to investors with high risk capacity, a long horizon, an adequate emergency fund, and no high-cost debt. A zero allocation should remain the default for conservative investors and anyone who cannot tolerate a complete loss. The 1% ceiling limits the portfolio-level damage of an extreme drawdown while allowing a suitable investor modest exposure to potential diversification or upside.

The recommendation is intentionally conservative. In a CAPM-style framework, an asset is attractive when its expected return compensates for systematic risk. Cryptocurrency lacks the intrinsic cash flows, earnings, or dividends used to anchor conventional valuation, making its expected return difficult to justify using standard portfolio theory. Low or occasionally negative correlation with traditional assets may offer diversification, but correlations are unstable and can rise during market stress, precisely when diversification is most valuable.

Crypto returns are also heavy-tailed and often positively skewed: a few exceptional outcomes can lift the average while most observations are far less attractive. Historical analyses can materially overstate opportunity because of **survivorship bias** when failed, delisted, illiquid, or abandoned tokens are excluded. Trading spreads, exchange fees, network fees, custody costs, taxes, and slippage further reduce realized returns, especially for small retail accounts or frequent rebalancing. Paytm Money should therefore treat crypto as speculative satellite exposure rather than a core allocation, prohibit leverage in an advisory portfolio, use suitability checks and explicit loss warnings, and rebalance rather than allow price appreciation to push exposure above the 1% cap.

### 3. T.A.N.G. fraud framework: two priority risks and defenses

The two most relevant social-engineering vectors for a combined UPI/wallet, lending, and wealth platform are **Authority plus Need** and **Temptation plus Greed**.

1. **Authority + Need — impersonation and urgent payment manipulation.** A fraudster may pose as Paytm support, a bank officer, a lender, a regulator, or a merchant and claim that KYC will expire, a loan is overdue, an account is blocked, or a refund requires immediate action. The victim may be induced to approve a UPI collect request, scan a malicious QR code, disclose an OTP, or install a screen-sharing application. A strong bank-side real-time defense is a **risk-based transaction-intervention engine** that combines new-beneficiary status, device changes, remote-access or screen-sharing signals, unusual amount or velocity, location/IP anomalies, and known mule-account intelligence. High-risk payments should trigger a clear payee-and-purpose warning, a cooling-off period, or a temporary block with step-up verification through a trusted in-app channel.

2. **Temptation + Greed — fake investment or loan offers.** Scammers may promise guaranteed crypto returns, pre-IPO access, instant high-limit loans, fee-free refinancing, or rewards that require an advance payment. They often move victims from social media to counterfeit apps or mule accounts. The corresponding defense is **real-time beneficiary and scam-pattern scoring**: the bank should assess recipient-account age, sudden inbound-fund spikes, rapid pass-through behavior, links to previously reported fraud, and many unrelated retail senders. Payments to high-risk beneficiaries should be delayed or blocked, accompanied by a warning that guaranteed returns or advance fees are common scam indicators, and routed for rapid confirmation and investigation.

These controls reduce harm at the moment of decision, when T.A.N.G.-based pressure is strongest, while preserving a clear path for legitimate customers to verify and complete genuine transactions.
