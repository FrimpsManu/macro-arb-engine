# Macro-Arb Engine

A data-driven global **macroeconomic statistical arbitrage engine** that uses macro signals and PCA-based divergence to generate trading signals and backtest asset strategies — currently focused on ETFs like **EWG (Germany)**.

---

## Project Overview

This project investigates the relationship between **macro fundamentals** and **asset prices** by:

* Applying **Principal Component Analysis (PCA)** to macroeconomic indicators
* Generating **macro divergence signals**
* Running **cointegration tests** between macro trends and asset prices
* Backtesting macro-driven trading strategies
* Comparing performance to a Buy-and-Hold benchmark
* Evaluating using performance metrics like Sharpe, Volatility, and Drawdown

---

## Project Structure

```
macro-arb-engine/
├── data/                  # Raw data files
│   ├── asset_prices.csv
│   ├── macro_data.csv
│   ├── macro_divergence.csv
│   └── signals.csv
│
├── notebooks/
│   └── pca_macro_analysis.ipynb
│
├── results/               # Output (performance reports, plots, etc.)
│
├── src/                   # Core Python modules
│   ├── backtester.py
│   ├── cointegration.py
│   ├── data_loader.py
│   ├── pca_engine.py
│   ├── signal_refiner.py
│   └── performance_metrics.py
│
└── README.md
```

---

## How to Run

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the full backtest**

   ```bash
   python src/backtester.py
   ```

3. **Output includes:**

   * Plot of Cumulative Returns (Buy-and-Hold vs Macro Strategy)
   * Performance metrics saved to `results/performance_report.csv`

---

## Methodology

* **PCA** extracts core macroeconomic trends
* **Divergence scores** measure deviation from long-term trends
* **Threshold-based signals** detect when assets are likely mispriced
* **Refined signals** filter noise to prevent false triggers
* **Backtesting** simulates trades with real historical price data
* **Evaluation metrics** include Sharpe Ratio, Max Drawdown, Volatility, etc.

---

## Completed Phases

* Phase 1: Load and align macro + asset price data
* Phase 2: PCA on macro indicators
* Phase 3: Divergence score generation
* Phase 4: Cointegration testing
* Phase 5: Signal-based backtesting
* Phase 6: Performance evaluation
* Phase 7: Signal refinement

---

## Upcoming Phases

* **Phase 8:** Add ML-based forecasting layer
* **Phase 9:** Build web dashboard / report UI
* **Phase 10:** Explore new markets, signals, and multi-asset strategies


## License

MIT License — see `LICENSE` (to be added).
 
