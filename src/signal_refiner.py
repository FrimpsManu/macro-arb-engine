# src/signal_refiner.py

import pandas as pd

# Load signals
raw_signals = pd.read_csv("data/signals.csv", index_col="Date", parse_dates=True)

# Parameters
z_thresh = 0.5  # Z-score threshold for signal strength
rolling_window = 1  # Smooth using rolling average

# Smooth & refine signals
refined_signals = raw_signals.copy()

for col in raw_signals.columns:
    # Apply rolling mean smoothing
    refined_signals[col] = raw_signals[col].rolling(rolling_window).mean()

    # Filter weak signals (absolute z-score < threshold)
    refined_signals[col] = refined_signals[col].apply(lambda x: x if abs(x) >= z_thresh else 0)

# Save refined signals
refined_signals.to_csv("data/signals_refined.csv")
print("✅ Saved refined signals to data/signals_refined.csv")
print("Signal activity by column:")
print((refined_signals != 0).sum())

