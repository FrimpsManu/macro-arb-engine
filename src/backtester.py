import pandas as pd
import matplotlib.pyplot as plt

# Load signals and prices
signals = pd.read_csv("data/signals_refined.csv", index_col="Date", parse_dates=True)
prices = pd.read_csv("data/asset_prices.csv", index_col="Date", parse_dates=True)

# Use EWG as traded asset and macro signal column (e.g., GERMANY_3M_RATE)
asset = 'EWG'
signal_column = "GERMANY_3M_RATE"

# Align data
prices = prices[[asset]].dropna()
signals = signals[[signal_column]].reindex(prices.index).fillna(0)

# Compute returns
returns = prices.pct_change().fillna(0)

# Strategy: long when signal > 0
positions = signals[signal_column].apply(lambda x: 1 if x > 0 else 0)

strategy_returns = positions.shift(1) * returns[asset]  # Shift to avoid lookahead bias
benchmark_returns = returns[asset]

# Compute cumulative returns
strategy_cum = (1 + strategy_returns).cumprod()
benchmark_cum = (1 + benchmark_returns).cumprod()

# Plot
plt.figure(figsize=(12, 6))
plt.plot(benchmark_cum, label="Buy and Hold")
plt.plot(strategy_cum, label="Signal Strategy (net)")
plt.title("Cumulative Returns: Buy-and-Hold vs Macro Signal Strategy")
plt.axhline(1, linestyle="--", color="black")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ============ PHASE 6: Performance Metrics ============ #
def evaluate_performance(strategy_returns, benchmark_returns):
	import numpy as np
	import pandas as pd

	def annualized_return(returns, periods_per_year=252):
		compounded_growth = (1 + returns).prod()
		n_periods = returns.count()
		return compounded_growth ** (periods_per_year / n_periods) - 1

	def annualized_volatility(returns, periods_per_year=252):
		return returns.std() * np.sqrt(periods_per_year)

	def sharpe_ratio(returns, risk_free_rate=0, periods_per_year=252):
		excess_ret = returns - risk_free_rate / periods_per_year
		ann_ret = annualized_return(excess_ret, periods_per_year)
		ann_vol = annualized_volatility(excess_ret, periods_per_year)
		return ann_ret / ann_vol if ann_vol != 0 else np.nan

	def max_drawdown(cumulative_returns):
		roll_max = cumulative_returns.cummax()
		drawdown = cumulative_returns / roll_max - 1
		return drawdown.min()

	metrics = {
		"Annualized Return": [
			annualized_return(strategy_returns),
			annualized_return(benchmark_returns)
		],
		"Annualized Volatility": [
			annualized_volatility(strategy_returns),
			annualized_volatility(benchmark_returns)
		],
		"Sharpe Ratio": [
			sharpe_ratio(strategy_returns),
			sharpe_ratio(benchmark_returns)
		],
		"Max Drawdown": [
			max_drawdown((1 + strategy_returns).cumprod()),
			max_drawdown((1 + benchmark_returns).cumprod())
		]
	}
	df = pd.DataFrame(metrics, index=["Strategy", "Benchmark"]).T
	return df

performance = evaluate_performance(strategy_returns, benchmark_returns)
print("\n📊 Performance Metrics:\n")
print(performance.round(4))

# Save to CSV
performance.to_csv("results/performance_report.csv")
print("\n✅ Saved performance metrics to results/performance_report.csv")
