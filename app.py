from dash import Dash, html, dcc, callback, Output, Input
from fetching import fetch_tickers, load_data
from features import indicator, get_sensitivity_params, backtest, get_stats, monte_carlo, sensitivity_analysis
from visualization import plot_indicator, plot_equity

tickers = fetch_tickers()
default_ticker = 'AAPL'
default_period = '365'
default_signal = 'ema'
fees = .25 # 0.25%
slippage = .1 # 0.1%
tcosts = (fees + slippage) / 100 # Change to the same format as log percentage returns

""" --- Dash App --- """
app = Dash(__name__,
           title='QRD',
           external_stylesheets=['https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap'],
           )

app.layout = html.Div(children=[
    html.H2('QRD', style={'padding':'20px'}),
    html.Div([
        dcc.Dropdown(
            id='ticker',
            options=tickers,
            value=default_ticker,
            searchable=True,
            clearable=False
        ),
        
        dcc.Dropdown(
            id='period',
            options=[
                {'label': '1 Month', 'value': '30'},
                {'label': '3 Months', 'value': '90'},
                {'label': '6 Months', 'value': '180'},
                {'label': '1 Year', 'value': '365'},
                {'label': '2 Years', 'value': '730'},
                {'label': '5 Years', 'value': '1825'},
                {'label': '10 Years', 'value': '3650'},
                {'label': '20 Years', 'value': '7300'}
            ],
            value=default_period,
            clearable=False,
            searchable=False
            ),

        dcc.Dropdown(
            id='signal',
            options=[
                {'label': 'EMA', 'value': 'ema'},
                {'label': 'MACD', 'value': 'macd'},
            ],
            value=default_signal,
            clearable=False,
            searchable=False
            ),],className='dropdown-row'),
    
    dcc.Graph(id='stats-chart'),
    dcc.Graph(id='indicator-chart'),
    dcc.Graph(id='equity-chart'),
    dcc.Graph(id='normal-mc-graph'),
    dcc.Graph(id='levy-mc-graph'),
    dcc.Graph(id='sensitivity-graph')
], style={'background-color':'#111111'})


@callback(
    [Output('stats-chart', 'figure'),
     Output('indicator-chart', 'figure'),
     Output('equity-chart', 'figure'),
     Output('normal-mc-graph', 'figure'),
     Output('levy-mc-graph', 'figure'),
     Output('sensitivity-graph', 'figure')],
    [Input('ticker', 'value'),
     Input('period', 'value'),
     Input('signal', 'value')]
)

def update_chart(ticker, period, signal):
    try:
        data = load_data(ticker, period)
        data = indicator(data, signal)

        params_1, params_2 = get_sensitivity_params(signal)

        data = backtest(data, tcosts)

        fig_stats = get_stats(data, ticker)
        fig_indicator = plot_indicator(data, ticker, signal)
        fig_equity = plot_equity(data)
        fig_normal_mc, fig_levy_mc = monte_carlo(data)
        fig_sensitivity = sensitivity_analysis(data, params_1, params_2, signal, tcosts)
        
        return fig_stats, fig_indicator, fig_equity, fig_normal_mc, fig_levy_mc, fig_sensitivity
    
    except Exception as e:
        return {
            'data': [],
            'layout': {
                'title': f'Error: Invalid symbol or data unavailable ({str(e)})',
                'template': 'plotly_dark'
            }
        }

if __name__ == '__main__':
    app.run_server(debug=True)