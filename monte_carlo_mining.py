"""
Monte Carlo Simulation for Bitcoin Mining Investment
=====================================================
Runs N simulated 60-month paths through the mining P&L model,
using historically calibrated distribution parameters for BTC price
and network difficulty.

Methodology:
  1. Calibrate: Extract monthly log-return distributions from historical
     data (mean, std dev, correlation) for pre-halving and post-halving regimes.
  2. Simulate: Generate N correlated random paths for BTC price and difficulty
     using Cholesky decomposition. Derive hashprice from the standard formula.
  3. Evaluate: Run each path through the mining P&L (revenue, costs, tax, cashflow)
     using fixed project parameters (capacity, PPA rate, miner specs, capex).
  4. Aggregate: Compute percentile distributions (P10/P25/P50/P75/P90) for
     IRR, payback period, net income, and cumulative cashflow.

Output:
  - Excel workbook with probability distributions and sample paths
  - Summary statistics for investment committee presentation

Usage:
  python monte_carlo_mining.py [--simulations 10000] [--months 60] [--output-dir ./output]

Dependencies:
  pip install numpy pandas openpyxl

Built for the AGM Omerelu 10MW Bitcoin Mining Project.
"""

# Implementation to follow — see README.md for methodology notes.
