import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import requests
from bs4 import BeautifulSoup as bs
import yahoo_fin.stock_info as si

from euronext import body1
from sp500 import body2

# Light theme: LUX, dark theme: DARKLY (enable darktheme in navbar)
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
###################################################################################################################
'''Make the tabs: one tab for Euronext and one tab for SP500 (different API's)
dbc.Tabs documentation: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/tabs/'''

tabs = dbc.Tabs(
    [
        dbc.Tab(body1, label='Euronext'),
        dbc.Tab(body2, label='S&P 500')
    ]
)

app.layout = tabs
###############################################################
'''CALLBACKS EURONEXT TAB'''


@app.callback(Output('output', 'children'), [Input('input', 'value')])
def get_company_name(value):
    if value is not None:
        response = requests.get(
            'https://www.quandl.com/api/v3/datasets/EURONEXT/{}.json?api_key=1eCS2saTbHTFds2LjKkX'.format(value))
        dataset = response.json()
        company_name = dataset['dataset']['name']
        return company_name


@app.callback(Output('output2', 'children'), [Input('input', 'value')])
def get_latest_close(value):
    if value is not None:
        response = requests.get(
            'https://www.quandl.com/api/v3/datasets/EURONEXT/{}.json?api_key=1eCS2saTbHTFds2LjKkX'.format(value))
        dataset = response.json()
        latest_close = dataset['dataset']['data'][0][4]
        return 'The latest close is: ' + str(latest_close)


@app.callback(Output('output3', 'children'), [Input('input', 'value')])
def get_market(value):
    if value is not None:
        response = requests.get(
            'https://www.quandl.com/api/v3/datasets/EURONEXT/{}.json?api_key=1eCS2saTbHTFds2LjKkX'.format(value))
        data = response.json()
        dataset = data['dataset']['description']
        split_dataset = dataset.split("<br>")
        market = split_dataset[2]
        return market


@app.callback(
    Output('linegraph-container-enx', 'figure'),
    [Input('input', 'value')])
def update_graph(value):
    response = requests.get(
        'https://www.quandl.com/api/v3/datasets/EURONEXT/{}.json?api_key=1eCS2saTbHTFds2LjKkX'.format(value))
    json_file = response.json()
    data = json_file['dataset']['data']
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
    df = df[::-1]

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

    # Make the subplots (way to have hover on both subplots simultaneously is not added yet)
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'],
                             hovertemplate='Price: € %{y}' +
                                           '<extra></extra>',
                             mode='lines', line=dict(color='#456987')), row=1, col=1)
    fig.add_trace(go.Bar(x=df['date'], y=df['volume'],
                         hovertemplate='Volume: %{y}' +
                                       '<extra></extra>', marker_color='#184a1a'), row=2, col=1)

    # Add the layout to the subplots
    fig.layout.update(
        title='Stock price evolution',
        showlegend=False,
        template='simple_white',
        title_x=0.5,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        hovermode='x unified',  # Displays date on the x-axis in full
    )

    # Add labels to subplots
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    return fig




#########################################################################################################
'''CALLBACKS SP500 tabs'''


@app.callback(Output('output2sp', 'children'), [Input('inputsp', 'value')])
def full_company_name_sp(value):
    if value is not None:
        r = requests.get('https://finance.yahoo.com/quote/{}/'.format(value))
        webpage = bs(r.content, features='lxml')
        title = str(webpage.find('title'))
        title = title[7:]
        split_title = title.split('(')
        full_name = split_title[0]
        return full_name
    else:
        return ''


@app.callback(Output('outputsp', 'children'), [Input('inputsp', 'value')])
def get_latest_close_sp(value):
    if value is not None:
        data = si.get_data(value, start_date='02/01/2017', index_as_date=True, interval='1d')
        df = pd.DataFrame(data)
        df = df[::-1]
        latest_close = round(df.loc[df.index[0], 'adjclose'], 2)
        return 'The latest close is: ' + str(latest_close)
    else:
        return ''


@app.callback(
    Output(component_id='linegraph-container-sp', component_property='figure'),
    [Input(component_id='inputsp', component_property='value')])
def update_graph(value):
    data = si.get_data(value, start_date='02/01/2017', index_as_date=True, interval='1d')
    df = pd.DataFrame(data)
    df.reset_index(inplace=True)  # make date-index full column and rename it
    df.rename(columns={'index': 'date'}, inplace=True)

    fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True, )

    # Make the subplots (way to have hover on both subplots simultaneously is not added yet)
    fig2.add_trace(go.Scatter(x=df['date'], y=df['close'],
                              hovertemplate='Price: € %{y}' +
                                            '<extra></extra>',
                              mode='lines', line=dict(color='#456987')), row=1, col=1)
    fig2.add_trace(go.Bar(x=df['date'], y=df['volume'],
                          hovertemplate='Volume: %{y}' +
                                        '<extra></extra>', marker=dict(color='#184a1a')), row=2, col=1)

    # Add the layout to the subplots
    fig2.layout.update(
        title='Stock price evolution',
        showlegend=False,
        template='simple_white',
        title_x=0.5,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        hovermode='x unified',  # Displays date on the x-axis in full
    )

    # Add labels to subplots
    fig2['layout']['yaxis']['title'] = 'Price'
    fig2['layout']['yaxis2']['title'] = 'Volume'

    return fig2


#########################################################################################################
if __name__ == '__main__':
    app.run_server(debug=True, port=8300, )
