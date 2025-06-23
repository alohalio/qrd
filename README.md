# QRD (Quant Research Dashboard)

**The primary goal of this project is to demonstrate and illustrate research methodology in quant finance with the simple dashboard--not to generate robust alpha**

![Landing Page](https://github.com/alohalio/qrd/blob/main/pics/landing_page.png)

---

## Overview

QRD is an interactive, browser-based dashboard for quantitative finance research and trading strategy analysis, built with Python, Plotly Dash, Scipy, and yfinance. It allows you to explore, visualize, and backtest trading signals, run Monte Carlo simulations, and perform sensitivity analysis to financial time series. The focus is on methodology, hypothesis testing, and exploratory data analysis, not on deploying production trading systems.

---

## Project Structure

The project is organized into the following Python files:

- **app.py**: Main entry point; orchestrates the dashboard layout, callbacks, and workflow.
- **fetching.py**: Fetches historical price data from yfinance, and scarpe all tickers in S&P 500 from wikipedia.
- **feature_engineering.py**: Implements technical indicators (EMA, MACD) and generates trading signals.
- **backtest.py**: Runs vectorized backtests of strategies, calculating gross/net returns and drawdowns.
- **sensitivity_analysis.py**: Computes strategy PnL or performance across a grid of signal parameters (e.g., EMA fast/slow periods), enabling parameter robustness analysis.
- **statistical_analysis.py**: Computes statsistical analysis such as daily returns with for mean, mean ± 1 standard deviation, and mean ± 1.5 standard deviation to summary of returns distribution.
- **simulation.py**: Runs Monte Carlo simulations (Normal, Levy) on returns and equity curves.
- **visualization.py**: Generates interactive Plotly figures for price, signals, equity, drawdowns, and sensitivity surfaces.
- **local.css**: Custom CSS file for additional dashboard styling (fonts, colors, layout tweaks, etc.).

> **Note:** In this project, many of these modules are implemented in a single file for simplicity. The above structure is recommended for larger or production projects.

---

## Dataset

- **Source**: Daily OHLCV data for S&P 500 companies, downloaded via yfinance.
- **Date Range**: User-selectable (e.g., 1 month, 1 year, up to 20 years).
- **Fields**: Date, Open, High, Low, Close, Volume.

---

## Data Processing

### Filtering and Preperation

- **Signal Engineering**: Computes EMA/MACD and binary signals for long/flat switching.
- **Return Calculation**: Log returns (`ln(Close_t / Close_{t-1})`) for more stable statistical properties.
- **Parameter Grid**: Sensitivity analysis over fast/slow EMA periods.

---

## Statistical Analysis

- **Returns Plot**: Visualizes daily log returns over the selected period.
- **Statistical Overlays**: Draws horizontal dotted lines at the mean, mean ± 1 standard deviation, and mean ± 1.5 standard deviations.
- **Interpretation**: This plot helps you quickly assess the distribution, volatility, and outlier behavior of the returns, providing context for strategy development and risk assessment.

![Statistical Analysis](https://github.com/alohalio/qrd/blob/main/pics/stats_analysis.png)

---

## Trading Strategy

- **Signal Logic**: Simple EMA or MACD crossover strategies.
- **Backtest**: Applies signals to log returns, updates equity curves, and computes drawdowns.
- **Transaction Costs**: Default commission + slippage(adjustable).
- **Benchmark**: Buy & hold equity curve for comparison.

![Technical Analysis](https://github.com/alohalio/qrd/blob/main/pics/technical_analysis.png)

---

## Equity Curve

Compare the different between benchmark and strategy performance

![Equity Curve](https://github.com/alohalio/qrd/blob/main/pics/equity_curve.png)

---

## Statistical Modelling

### Monte Carlo Simulation

- **Normal/Levy**: Simulates possible strategy paths to assess risk and robustness.
- **Visualization**: Overlays simulated paths with actual PnL for comparison.

**Monte Carlo Normal Distribution**
![Normal Distribution](https://github.com/alohalio/qrd/blob/main/pics/montecarlo_normal_distribution.png)

**Monte Carlo Levy Distribution**
![Levy Distribution](https://github.com/alohalio/qrd/blob/main/pics/montecarlo_levy_distribution.png)

---

## Sensitivity Analysis

- **Parameter Sweep:** For each combination of parameters (e.g., fast and slow EMA periods), the strategy is run and final PnL or another performance metric is recorded.
- **Robustness Visualization:** Results are visualized as a 3D surface (using Plotly), helping to identify regions of parameter stability and avoid overfitting.
- **Interpretation:** The heatmap or surface plot allows you to see which parameter sets lead to consistent outperformance and which are sensitive to small changes.

![Sensitivity Analysis](https://github.com/alohalio/qrd/blob/main/pics/sensitivity_analysis.png)

---

## Visualization

QRD generates multiple interactive charts:

- **Price & Signal**: Overlay price, fast/slow EMAs, and buy/sell signals.
- **Equity Curve**: Shows cumulative returns (benchmark, gross, net) and drawdowns.
- **Monte Carlo Simulations**: Visualizes simulated equity outcomes under different distributions.
- **Sensitivity Analysis**: 3D plot of strategy PnL across parameter grids.

---

## Notes

- Default time frame: daily, with period selectable from dropdown.
- Transaction costs: 0.25% commission and 0.1% slippage (adjustable).
- For best statistical significance, use long timeframes and ensure enough trades.
- The dashboard is for demonstration/learning, not live trading.
- For advanced strategies, consider integrating machine learning models, additional factors, or more robust backtesting engines.
- Visualizations use the plotly_dark theme and Noto Serif Kr font. You can customize these in `visualization.py`.

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/alohalio/qrd?tab=MIT-1-ov-file) file for details.

---

## Contact

- LinkedIn: [Nutthapat Lohasawaroge](https://www.linkedin.com/in/nutthapat-l/)
- GitHub: [Alohalio](https://github.com/alohalio)