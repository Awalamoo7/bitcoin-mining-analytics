# Bitcoin Mining Investment Analytics

A Python toolkit for evaluating Bitcoin mining investments. Built to support financial modelling for utility-scale mining operations, specifically calibrated for a mining data center in Nigeria.

## What this solves

Bitcoin mining financial models require assumptions about three volatile, interdependent variables: **BTC price**, **network difficulty**, and **hashprice** (mining revenue per unit of hashrate). Most models use straight-line growth rates for these variables — e.g., "BTC price grows 2% per month" — which compounds to unrealistic levels over a 5-year projection and completely ignores the cyclical, non-linear nature of Bitcoin markets.

This toolkit takes a different approach:

1. **`btc_data_downloader.py`** — Pulls 5 years of historical daily data for all three variables from free APIs, merges them on date, and outputs clean CSV and Excel files for model calibration.

2. **`monte_carlo_mining.py`** — Runs 10,000-path Monte Carlo simulation over the mining P&L model, using historically calibrated distribution parameters (mean, volatility, correlation, halving regime shifts) to generate probability distributions for IRR, MOIC, payback period, and cumulative cashflow. Outputs a professionally formatted "MC Simulation" sheet into a copy of the consolidated financial model.

## Why Monte Carlo instead of straight-line assumptions

Historical data (March 2021 – March 2026) shows:

| Metric            | Monthly Mean | Monthly Std Dev | Min    | Max    |
| ----------------- | ------------ | --------------- | ------ | ------ |
| BTC Price Change  | +1.3%        | 13.7%           | -23.9% | +35.8% |
| Difficulty Change | +3.4%        | 6.8%            | -29.1% | +18.3% |
| Hashprice Change  | -2.8%        | 14.2%           | -39.4% | +36.7% |

A 2% monthly BTC price assumption compounds to **+228% over 5 years**. The actual full-period CAGR was **+4.5% annually**. The standard deviation is 10x the mean — the "average" growth rate is nearly meaningless for forecasting any individual path.

Monte Carlo simulation respects this reality. Instead of one assumed path, it generates thousands of statistically plausible paths — each with its own bull runs, crashes, and halving shocks — and reports the **probability distribution** of investment outcomes.

## Quick start

### Requirements

```
Python 3.9+
pip install requests openpyxl pandas numpy scipy
```

### Monte Carlo simulation

```bash
python monte_carlo_mining.py                          # defaults: 10k sims, 60 months
python monte_carlo_mining.py --simulations 50000      # more paths for tighter confidence
python monte_carlo_mining.py --months 36              # shorter horizon
python monte_carlo_mining.py --output-dir ./results   # custom output directory
```

**Arguments:**

| Flag            | Default                     | Description                           |
| --------------- | --------------------------- | ------------------------------------- |
| `--simulations` | 10,000                      | Number of Monte Carlo paths           |
| `--months`      | 60                          | Projection horizon in months          |
| `--data-path`   | `data/btc_merged_data.xlsx` | Historical data file                  |
| `--model-path`  | `Consolidated Model.xlsx`   | Source financial model (not modified) |
| `--output-dir`  | `output`                    | Where to write the output workbook    |

**Output:** Copies the consolidated model to `output/Consolidated_Model.xlsx` and adds an "MC Simulation" sheet containing:

- Calibration parameters (regime-specific means, std devs, correlations)
- Summary statistics table (P10/P25/P50/P75/P90 for IRR, MOIC, payback, net income)
- Probability thresholds (IRR > 0%/10%/20%, payback within 24/36/48 months)
- Month-by-month cumulative free cashflow percentile curves
- IRR distribution histogram
- 20 sample simulation paths with full monthly detail

### Data downloader

```bash
python btc_data_downloader.py                     # 5 years, output to ./output/
python btc_data_downloader.py --days 2555          # 7 years
python btc_data_downloader.py --output-dir ./data  # custom output directory
```

**Output files:**

| File                       | Description                                              |
| -------------------------- | -------------------------------------------------------- |
| `btc_price.csv`            | Daily BTC/USD close price                                |
| `btc_difficulty.csv`       | Daily network difficulty                                 |
| `btc_hashprice.csv`        | Daily hashprice with price, difficulty, and block reward |
| `btc_merged_data.csv`      | All three datasets joined on date                        |
| `btc_historical_data.xlsx` | Formatted workbook with Daily, Annual, and Monthly tabs  |

### Data sources

All sources are free with no API key required:

| Data               | Primary Source                                        | Fallback                                                     |
| ------------------ | ----------------------------------------------------- | ------------------------------------------------------------ |
| BTC Price          | [CoinGecko API](https://www.coingecko.com/en/api)     | [CoinMetrics Community API](https://docs.coinmetrics.io/api) |
| Network Difficulty | [Blockchain.info API](https://www.blockchain.com/api) | [CoinMetrics Community API](https://docs.coinmetrics.io/api) |
| Hashprice          | Derived from price + difficulty + block reward        | —                                                            |

### Hashprice derivation

Hashprice is computed using the standard mining revenue formula:

```
Hashprice ($/PH/day) = BTC_Price × Block_Reward × 86400 / (Difficulty × 2^32) × 10^15
```

This formula is used by [Hashrate Index](https://hashrateindex.com/) (Luxor), institutional mining desks, and public mining companies in their financial reporting. The block reward adjusts automatically based on the Bitcoin halving schedule.

## Project context

This toolkit was built for the evaluation of a 10MW Bitcoin mining deploymentin Nigeria:

- **~ Bitmain S19XP miners** (140 TH/s, 21 J/TH each)
- **Power Purchase Agreement** at $x/kWh
- **60-month projection horizon** (April 2026 – March 2031)
- **One halving event** within the projection (April 2028: block reward drops from 3.125 to 1.5625 BTC)

The financial model evaluates two revenue approaches:

- **Model 1 (Hashprice-driven):** Uses hashprice as a direct input with a secular annual decline
- **Model 2 (BTC Price-driven):** Models revenue from first principles using BTC price, difficulty, and block reward as separate dynamic variables _(recommended — more transparent and calibratable)_

## Repository structure

```
btc-mining-analytics/
├── btc_data_downloader.py                # Historical data pipeline
├── monte_carlo_mining.py                 # Monte Carlo simulation engine
├── AGM Consolidated Model AA_2.0.xlsx    # Source financial model (do not modify)
├── data/
│   └── btc_merged_data.xlsx              # Historical BTC price + difficulty + hashprice
├── output/
│   └── AGM_Consolidated_Model_AA_2_0.xlsx  # Output model with MC Simulation sheet
├── requirements.txt
├── .gitignore
└── README.md
```

## Methodology notes

### Calibration approach

The simulation is calibrated from the **post-halving rally phase** (April 2024 – March 2025), which reflects the structural regime shift driven by spot Bitcoin ETF approvals and institutional adoption. The Q4-2025/Q1-2026 drawdown is excluded from calibration as it was driven by macro factors (tariff escalation, rate-hike cycle) rather than any change in Bitcoin's structural fundamentals.

**Calibrated parameters:**

| Regime                      | Price Drift          | Price Vol | Diff Drift           | Diff Vol | Correlation |
| --------------------------- | -------------------- | --------- | -------------------- | -------- | ----------- |
| Months 1–24 (pre-halving)   | +1.9%/mo (+25.6%/yr) | 10.3%/mo  | +2.6%/mo (+37.0%/yr) | 3.8%/mo  | 0.53        |
| Months 25–60 (post-halving) | +1.9%/mo (+25.6%/yr) | 10.3%/mo  | +1.3%/mo (+17.0%/yr) | 3.8%/mo  | 0.37        |

Post-halving difficulty growth is reduced by 50% to reflect miner capitulation when block rewards halve to 1.5625 BTC with already-compressed margins. A one-time -10% difficulty shock is applied at the halving month (April 2028), calibrated from the observed -5.1% peak-to-trough drop after the April 2024 halving, with a premium for thinner margins in 2028.

### On log-returns

The simulation uses log-returns (ln(P*t / P*{t-1})) rather than simple percentage returns. Log-returns are additive across time periods, better approximate normality for financial data, and prevent prices from going negative during simulation. This is standard practice in quantitative finance.

### On correlation modelling

BTC price and network difficulty are positively correlated — higher prices attract more mining investment, which increases difficulty. The simulation uses Cholesky decomposition to generate correlated random draws, preserving this relationship. Simulating them independently would produce unrealistic paths (e.g., price crashes while difficulty surges).

### On the halving event

The April 2028 halving is modelled as a structural break:

- Block reward drops instantaneously from 3.125 to 1.5625 BTC
- A one-time -10% difficulty shock (marginal miners exit)
- Difficulty growth rate shifts to a lower post-halving regime
- Price drift continues unchanged (halving supply squeeze supports price)

### Operational shutdown floor

The simulation applies an operational shutdown option: if monthly EBITDA drops below zero (net revenue doesn't cover PPA + O&M costs), the mine idles for that month. This means:

- No revenue, no variable costs, and FCF = $0 for that month
- The mine resumes automatically when conditions improve
- This prevents unrealistic cash hemorrhaging in downside scenarios
- Cumulative free cashflow is monotonically non-decreasing (it either grows or stays flat)

This reflects real operational practice — no rational operator runs machines at a loss when they can simply power down and wait.

### IRR computation

IRR is computed as the annualized internal rate of return on monthly free cashflows using bisection root-finding on the NPV function. For simulations where the investment never breaks even (no sign change in the cashflow series), IRR is assigned -100% (total loss). MOIC is computed as total positive cashflows divided by initial capex.

## Key results (10,000 simulations, seed 42)

| Metric            | P10    | P25    | P50      | P75   | P90   |
| ----------------- | ------ | ------ | -------- | ----- | ----- |
| IRR               | -99.9% | -88.4% | -39.1%   | 11.5% | 54.3% |
| MOIC              | 0.06x  | 0.18x  | 0.50x    | 1.21x | 2.46x |
| Payback month     | 16     | 18     | 23       | 43    | 53    |
| Year-1 net income | —      | —      | $278,945 | —     | —     |
| 5-year net income | —      | —      | $630,363 | —     | —     |

| Probability threshold          | Value |
| ------------------------------ | ----- |
| Prob. IRR > 0%                 | 30.6% |
| Prob. IRR > 10%                | 25.6% |
| Prob. IRR > 20%                | 21.2% |
| Prob. payback within 24 months | 18.3% |
| Prob. payback within 48 months | 25.3% |
| Prob. losing money (5-yr)      | 69.4% |

## License

MIT

## Acknowledgements

Built with assistance from Claude (Anthropic). Data sourced from CoinGecko, Blockchain.info, and CoinMetrics public APIs.
