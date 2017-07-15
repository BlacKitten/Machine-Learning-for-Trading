import plotly as py
import pandas as pd
import numpy as np

UOPIX = pd.read_csv("NVDA.csv", index_col='Date', parse_dates=True,
                    usecols=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], na_values=['nan'])
dates = pd.date_range('2016-07-15', '2017-07-14')
df_NVDA = pd.DataFrame(index=dates)
df_NVDA = df_NVDA.join(UOPIX)
df_NVDA = df_NVDA.dropna()
df_NVDA.fillna(method="ffill", inplace="TRUE")
df_NVDA.fillna(method="bfill", inplace="TRUE")

INCREASING_COLOR = '#16c910'
DECREASING_COLOR = '#ff0000'
data = [dict(
    type='candlestick',
    open=df_NVDA['Open'],
    high=df_NVDA['High'],
    low=df_NVDA['Low'],
    close=df_NVDA['Close'],
    x=df_NVDA.index,
    yaxis='y2',
    name='Price',
    increasing=dict(line=dict(color=INCREASING_COLOR)),
    decreasing=dict(line=dict(color=DECREASING_COLOR)),
)]

layout = dict()

fig = dict(data=data, layout=layout)

fig['layout'] = dict()
fig['layout']['plot_bgcolor'] = 'rgb(20, 20, 20)'
fig['layout']['xaxis'] = dict(rangeselector=dict(visible=True))
fig['layout']['yaxis'] = dict(domain=[0, 0.2], showticklabels=False)
fig['layout']['yaxis2'] = dict(domain=[0.2, 0.8])
fig['layout']['legend'] = dict(orientation='h', y=0.9, x=0.3, yanchor='bottom')
fig['layout']['margin'] = dict(t=0, b=40, r=40, l=40)

rangeselector = dict(
    visibe=True,
    x=0, y=0.9,
    bgcolor='rgba(117, 15, 201, 0.4)',
    font=dict(size=13),
    buttons=list([
        dict(count=1,
             label='reset',
             step='all'),
        dict(count=1,
             label='1yr',
             step='year',
             stepmode='backward'),
        dict(count=3,
             label='3 mo',
             step='month',
             stepmode='backward'),
        dict(count=1,
             label='1 mo',
             step='month',
             stepmode='backward'),
        dict(step='all')
    ]))

fig['layout']['xaxis']['rangeselector'] = rangeselector


def movingaverage(interval, window_size=10):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')


mv_y = movingaverage(df_NVDA.Close)
mv_x = list(df_NVDA.index)

# Clip the ends
mv_x = mv_x[5:-5]
mv_y = mv_y[5:-5]

fig['data'].append(dict(x=mv_x, y=mv_y, type='scatter', mode='lines',
                        line=dict(width=1),
                        marker=dict(color='#E377C2'),
                        yaxis='y2', name='Moving Average'))

colors = []

for i in range(len(df_NVDA.Close)):
    if i != 0:
        if df_NVDA.Close[i] > df_NVDA.Close[i - 1]:
            colors.append(INCREASING_COLOR)
        else:
            colors.append(DECREASING_COLOR)
    else:
        colors.append(DECREASING_COLOR)

fig['data'].append(dict(x=df_NVDA.index, y=df_NVDA.Volume,
                        marker=dict(color=colors),
                        type='bar', yaxis='y', name='Volume'))


def bbands(price, window_size=10, num_of_std=2):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return rolling_mean, upper_band, lower_band


bb_avg, bb_upper, bb_lower = bbands(df_NVDA.Close)

fig['data'].append(dict(x=df_NVDA.index, y=bb_upper, type='scatter', yaxis='y2',
                        line=dict(width=1),
                        marker=dict(color='#750fc9'), hoverinfo='none',
                        legendgroup='Bollinger Bands', name='Bollinger Bands'))

fig['data'].append(dict(x=df_NVDA.index, y=bb_lower, type='scatter', yaxis='y2',
                        line=dict(width=1),
                        marker=dict(color='#750fc9'), hoverinfo='none',
                        legendgroup='Bollinger Bands', showlegend=False))
py.offline.plot(fig, filename='candlestick-test-3', validate=False)