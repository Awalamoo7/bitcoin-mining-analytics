# Bitcoin Mining Investment Analytics

A Python toolkit for evaluating Bitcoin mining investments. Built to support financial modelling for utility-scale mining operations, specifically calibrated for a mining data center in Nigeria.

## What this solves

Bitcoin mining financial models require assumptions about three volatile, interdependent variables: **BTC price**, **network difficulty**, and **hashprice** (mining revenue per unit of hashrate). Most models use straight-line growth rates for these variables — e.g., "BTC price grows 2% per month" — which compounds to unrealistic levels over a 5-year projection and completely ignores the cyclical, non-linear nature of Bitcoin markets.

This toolkit takes a different approach:

1. **`btc_data_downloader.py`** — Pulls 5 years of historical daily data for all three variables from free APIs, merges them on date, and outputs clean CSV and Excel files for model calibration.

2. **`monte_carlo_mining.py`** _(coming soon)_ — Runs Monte Carlo simulation over the mining P&L model, using historical distribution parameters (mean, volatility, correlation, halving regime shifts) to generate probability distributions for IRR, payback period, and cumulative cashflow.

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
pip install requests openpyxl pandas numpy
```

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
├── btc_data_downloader.py     # Historical data pipeline
├── monte_carlo_mining.py      # Monte Carlo simulation (coming soon)
├── data/                      # Sample/cached data
├── output/                    # Generated files (gitignored)
├── requirements.txt
├── .gitignore
└── README.md
```

## Methodology notes

### On the choice of log-returns

The Monte Carlo simulation uses log-returns (ln(P*t / P*{t-1})) rather than simple percentage returns for calibration. Log-returns are additive across time periods, better approximate normality for financial data, and prevent the mathematical impossibility of prices going negative during simulation. This is standard practice in quantitative finance.

### On correlation modelling

BTC price and network difficulty are positively correlated — higher prices attract more mining investment, which increases difficulty. The simulation uses Cholesky decomposition to generate correlated random draws, preserving this relationship. Simulating them independently would produce unrealistic paths (e.g., price crashes while difficulty surges).

### On halving treatment

The April 2028 halving is modelled as a structural break, not a smooth transition:

- Block reward drops instantaneously from 3.125 to 1.5625 BTC
- Difficulty growth parameters shift (historically, difficulty growth decelerates post-halving as marginal miners shut down)
- BTC price growth parameters shift (post-halving periods have historically seen stronger price appreciation)

The pre-halving and post-halving distribution parameters are calibrated separately from historical data.

## License

MIT

## Acknowledgements

Built with assistance from Claude (Anthropic). Data sourced from CoinGecko, Blockchain.info, and CoinMetrics public APIs.
