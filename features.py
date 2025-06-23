import pandas as pd
import numpy as np
from scipy.stats import levy_stable
from visualization import plot_stats, plot_normal_mc, plot_levy_mc, plot_sensitivity_analysis

def indicator(data: pd.DataFrame, signal: str):
    data['pct'] = np.log(data.close / data.close.shift().bfill())

    if signal == 'ema':
        data['fast_ema'] = data.close.ewm(span=50, adjust=False).mean()
        data['slow_ema'] = data.close.ewm(span=100, adjust=False).mean()
        data['signal'] = (data.fast_ema > data.slow_ema).astype(int)

    else:
        data['fast_ema'] = data.close.ewm(span=12, adjust=False).mean()
        data['slow_ema'] = data.close.ewm(span=26, adjust=False).mean()
        data['signal'] = ((data.fast_ema - data.slow_ema).ewm(span=9).mean() > 0).astype(int)

    return data

def get_sensitivity_params(signal: str):
    params_1, params_2 = np.arange(10, 50, 2), np.arange(20, 120, 5)

    return params_1, params_2

def backtest(data: pd.DataFrame, tcosts: float):
    data['gross'] = data.signal.shift().fillna(0) * data.pct
    data['net'] = np.where(data.signal.diff(),
                           data.gross - tcosts,
                           data.gross)
    data['benchmark'] = data.pct.add(1).cumprod().sub(1).mul(100)
    data['gross_pnl'] = np.clip(data.gross.add(1).cumprod().sub(1).mul(100), -100.00, None)
    data['net_pnl'] = np.clip(data.net.add(1).cumprod().sub(1).mul(100), -100.00, None)
    data['benchmark_dd'] = ((data.pct.add(1).cumprod() - data.pct.add(1).cumprod().expanding(1).max())/
                            data.pct.add(1).cumprod().expanding(1).max()).mul(100)
    data['gross_dd'] = ((data.gross.add(1).cumprod() - data.gross.add(1).cumprod().expanding(1).max())/
                        data.gross.add(1).cumprod().expanding(1).max()).mul(100)
    data['net_dd'] = ((data.net.add(1).cumprod() - data.net.add(1).cumprod().expanding(1).max())/
                      data.net.add(1).cumprod().expanding(1).max()).mul(100)

    return data

def get_stats(data: pd.DataFrame, ticker: str):
    date = data.date
    pct = data.pct
    mean = pct.mean()
    sd = pct.std()

    fig = plot_stats(date, pct, mean, sd, ticker)

    return fig

def monte_carlo(data: pd.DataFrame, n_sim: int=100, alpha: float=1.7, beta: float=0.0):
    returns = data.pct.values
    original_equity = data.net_pnl.values
    mu = np.mean(returns)
    sigma = np.std(returns)
    n_steps = len(returns)
    
    def normal_distribution():
        normal_curve = []
        for _ in range(n_sim):
            normal_returns = np.random.normal(mu, sigma, n_steps)
            # normal_equity = np.multiply(np.clip(np.cumsum(normal_returns), -1.00, None), 100)
            normal_equity = np.multiply(np.clip((np.cumprod(1 + normal_returns) - 1), -1.00, None), 100)
            normal_curve.append(normal_equity)

        return normal_curve

    def levy_distribution():
        levy_curve = []
        for _ in range(n_sim):
            levy_returns = levy_stable.rvs(alpha, beta, loc=mu,
                                          scale=sigma, size=n_steps)
            # levy_equity = np.multiply(np.clip(np.cumsum(levy_returns), -1.00, None), 100)
            levy_equity = np.multiply(np.clip((np.cumprod(1 + levy_returns) - 1), -1.00, None), 100)
            levy_curve.append(levy_equity)
        
        return levy_curve

    normal_mc_curve = normal_distribution()
    levy_mc_curve = levy_distribution()

    fig_normal_curve = plot_normal_mc(original_equity, normal_mc_curve)
    fig_levy_curve = plot_levy_mc(original_equity, levy_mc_curve)
    
    return fig_normal_curve, fig_levy_curve

def sensitivity_analysis(data: pd.DataFrame, param_1, param_2, signals, tcosts):
    fast_periods = param_1
    slow_periods = param_2

    fast_periods_mesh, slow_periods_mesh = np.meshgrid(fast_periods, slow_periods)
    pnl_grids = np.zeros_like(fast_periods_mesh, dtype=float)

    def calc_sensitivity(fast, slow):
        fast_ema = data.close.ewm(span=fast, adjust=False).mean()
        slow_ema = data.close.ewm(span=slow, adjust=False).mean()
        if signals == 'ema':
            signal = (fast_ema > slow_ema).astype(int)
        else:
            signal = ((fast_ema - slow_ema).ewm(span=9).mean() > 0).astype(int)
        gross = (signal.shift(periods=1).fillna(0) * data.pct)
        net = gross.where(signal == signal.shift(periods=1), gross - tcosts)
        # pnl = np.multiply(np.clip(np.cumsum(net), -1.00, None), 100).iloc[-1]
        pnl = np.multiply(np.clip((np.cumprod(1 + net) - 1), -1.00, None), 100).iloc[-1]

        return pnl

    for _ in range(len(fast_periods)):
        for __ in range(len(slow_periods)):
            fast = fast_periods[_]
            slow = slow_periods[__]
            pnl_grids[_, __] = calc_sensitivity(fast, slow)

    pnl_grids = np.nan_to_num(pnl_grids, nan=0.0)
    
    fig = plot_sensitivity_analysis(fast_periods_mesh, slow_periods_mesh, pnl_grids)

    return fig