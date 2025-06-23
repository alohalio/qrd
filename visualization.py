import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def plot_stats(date, pct, mean, sd, ticker):
    fig = go.Figure(go.Scatter(x=date, y=pct, mode='markers'))
    fig.add_hline(y=mean,annotation_text='Mean')
    fig.add_hline(y=mean+sd, annotation_text='+σ')
    fig.add_hline(y=mean-sd, annotation_text='-σ')
    fig.add_hline(y=mean+1.5*sd, annotation_text='+1.5σ')
    fig.add_hline(y=mean-1.5*sd, annotation_text='-1.5σ')
    fig.update_layout(
        title=f'{ticker} Daily Returns',
        shapes=[
            dict(
                type="line",
                line=dict(
                    color='#feebf6',
                    width=1
                    )
        )],
        template='plotly_dark',
        font_family='Noto Serif Kr',
        height=800
    )

    return fig

def plot_indicator(data: pd.DataFrame, ticker: str, signal: str):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=(f'Price Action', 'Signal'),
                        horizontal_spacing=None, vertical_spacing=.05)
    fig.append_trace(go.Scatter(x=data.date, y=data.close, mode='lines', name='Close'), 1, 1)
    if signal == 'ema':
        fig.append_trace(go.Scatter(x=data.date, y=data.fast_ema, mode='lines', name='EMA 50'), 1, 1)
        fig.append_trace(go.Scatter(x=data.date, y=data.slow_ema, mode='lines', name='EMA 100'), 1, 1)
    else:
        fig.append_trace(go.Scatter(x=data.date, y=data.fast_ema, mode='lines', name='EMA 12'), 1, 1)
        fig.append_trace(go.Scatter(x=data.date, y=data.slow_ema, mode='lines', name='EMA 26'), 1, 1)
    fig.append_trace(go.Scatter(x=data.date, y=data.signal, mode='lines', name='Signal'), 2, 1)
    fig.update_layout(
        title=f'{ticker.upper()} Technical Indicator',
        template='plotly_dark',
        font_family='Noto Serif Kr',
        legend=dict(
            font=dict(size=10)
        ),
        showlegend=True,
        height=800
        )
    fig.update_yaxes(title_text='Price(USD)', row=1, col=1)
    fig.update_yaxes(title_text='Signal', row=2, col=1)
    fig.update_xaxes(title_text='Date', row=2, col=1)
    
    return fig

def plot_equity(data: pd.DataFrame):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=('Cumulative Returns', 'Drawdowns'),
                        horizontal_spacing=None, vertical_spacing=.05)
    fig.append_trace(go.Scatter(x=data.date, y=data.benchmark, mode='lines', name='Benchmark'), 1, 1)
    fig.append_trace(go.Scatter(x=data.date, y=data.gross_pnl, mode='lines', name='Gross'), 1, 1)
    fig.append_trace(go.Scatter(x=data.date, y=data.net_pnl, mode='lines', name='Net'), 1, 1)
    fig.append_trace(go.Scatter(x=data.date, y=data.benchmark_dd, mode='lines',
                                fill='tozeroy', name='Benchmark'), 2, 1)
    fig.append_trace(go.Scatter(x=data.date, y=data.gross_dd, mode='lines',
                                fill='tozeroy', name='Gross'), 2, 1)
    fig.append_trace(go.Scatter(x=data.date, y=data.net_dd, mode='lines',
                                fill='tozeroy', name='Net'), 2, 1)
    fig.update_layout(
        title='Benchmark vs Strategy Performance',
        template='plotly_dark',
        font_family='Noto Serif Kr',
        legend=dict(
            font=dict(size=10)
        ),
        showlegend=True,
        height=800,
        )
    fig.update_yaxes(title_text='Percentage(%)', row=1, col=1)
    fig.update_yaxes(title_text='Percentage(%)', row=2, col=1)
    fig.update_xaxes(title_text='Date', row=2, col=1)
    
    return fig

def plot_normal_mc(original_curve, mc_curve):
    fig = go.Figure(go.Scatter(
        y=original_curve,
        mode='lines',
        line=dict(width=3, color='white'),
        name='Original'
        ))
        
    for curve in mc_curve:
        fig.add_trace(go.Scatter(
            y=curve,
            mode='lines',
            line=dict(width=1),
            opacity=0.2,
            showlegend=False
            ))

    fig.update_layout(
        title=f'Monte Carlo Simulations (Normal Distribution)',
        yaxis_title='PnL(%)',
        template='plotly_dark',
        font_family='Noto Serif Kr',
        legend=dict(
            font=dict(size=10)
            ),
        showlegend=True,
        height=800)
        
    return fig

def plot_levy_mc(original_curve, levy_curve):
    fig = go.Figure(go.Scatter(
        y=original_curve,
        mode='lines',
        line=dict(width=3, color='white'),
        name='Original'
        ))
        
    for curve in levy_curve:
        fig.add_trace(go.Scatter(
            y=curve,
            mode='lines',
            line=dict(width=1),
            opacity=0.2,
            showlegend=False
            ))
    
    fig.update_layout(
        title=f'Monte Carlo Simulations (Levy Distribution)',
        yaxis_title='PnL(%)',
        template='plotly_dark',
        font_family='Noto Serif Kr',
        legend=dict(
            font=dict(size=10)
            ),
        showlegend=True,
        height=800)
        
    return fig

def plot_sensitivity_analysis(x, y, z):
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.update_layout(title='Sensitivity Analysis',
                      template='plotly_dark',
                      scene={'xaxis': {'title':'Params 1'},
                             'yaxis': {'title':'Params 2'},
                             'zaxis': {'title':'PnL(%)'}
                             },
                             legend=dict(
                                 font=dict(size=10)
                                 ),
                             font_family='Noto Serif Kr',
                             height=800)
    
    return fig