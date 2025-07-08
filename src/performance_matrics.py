# phase6/performance_metrics.py
import numpy as np
import pandas as pd

def compute_metrics(strategy_returns: pd.Series, benchmark_returns: pd.Series, freq='M'):
    metrics = {}

    # Ensure no NaNs
    strategy_returns = strategy_returns.dropna()
    benchmark_returns = benchmark_returns.dropna()

    # ---- Annualized Return ---- #
    periods_per_year = {'D': 252, 'M': 12, 'W': 52}[freq]
    metrics['Annualized Return'] = (1 + strategy_returns).prod() ** (periods_per_year / len(strategy_returns)) - 1

    # ---- Annualized Volatility ---- #
    metrics['Annualized Volatility'] = strategy_returns.std() * np.sqrt(periods_per_year)

    # ---- Sharpe Ratio (assumes risk-free rate = 0) ---- #
    if metrics['Annualized Volatility'] > 0:
        metrics['Sharpe Ratio'] = metrics['Annualized Return'] / metrics['Annualized Volatility']
    else:
        metrics['Sharpe Ratio'] = np.nan

    # ---- Max Drawdown ---- #
    cumulative = (1 + strategy_returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    metrics['Max Drawdown'] = drawdown.min()

    # ---- Win Rate ---- #
    metrics['Win Rate'] = (strategy_returns > 0).sum() / len(strategy_returns)

    # ---- Total Trades ---- #
    position_changes = strategy_returns.shift(1).fillna(0) != strategy_returns.fillna(0)
    metrics['Total Trades'] = position_changes.sum()

    return metrics
