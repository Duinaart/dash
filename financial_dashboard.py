import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import requests

import plotly.graph_objects as go
import plotly.express as px

from dash.dependencies import Input, Output, State

# Light theme: LUX, dark theme: DARKLY (enable darktheme in navbar)
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
##############################################################


###############################################################
# Make a navigation bar (dropdown items)
## Make a reusable navitem for different dashboards
nav_item = dbc.NavItem(
    dbc.Row(
        [dbc.NavLink('Euronext Stock Exchange', href='https://live.euronext.com/nl'),
        dbc.NavLink('Yahoo finance', href='https://finance.yahoo.com/')
         ],
        align='center',
    ),

)

## Make a Reusable dropdown for different dashboards
dropdown = dbc.Col(
    dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem('Dash Documentation', href='https://dash.plotly.com/'),
            dbc.DropdownMenuItem('Bootstrap Documentation', href='https://dash-bootstrap-components.opensource.faculty.ai/docs/'),
            dbc.DropdownMenuItem('Quandl Documentation', href='https://docs.quandl.com/'),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem('Youtube tutorial', href='https://www.youtube.com/watch?v=P-XYio7G_Dg&ab_channel=PipInstallPython')
        ],
        nav=True,       # needs to be set to true if it is inside navigation bar to get consistent styling
        in_navbar=True,  # say that it needs to be in navigation bar
        label= 'Useful Links',
        right=True,
    ),
    width='auto'
    )


## Navigation Bar layout
navbar = dbc.Navbar(
    dbc.Container(      # A container keeps the content of the rows and columns into one single blob that can be moved
        [
            # Use row and col to control vertical alignment of logo
            dbc.Row(
                [dbc.Col((html.Img(src='https://prismic-io.s3.amazonaws.com/plotly-marketing-website/bd1f702a-b623-48ab-a459-3ee92a7499b4_logo-plotly.svg',height='30px')), width='auto'),
                dbc.Col((dbc.NavbarBrand('Finance Dashboard')), width='auto')],
                align='center',
                no_gutters=True,
            ),
            dbc.Row(dbc.Col(dbc.NavbarToggler(id='navbar-toggler2'))),
            dbc.Row(dbc.Col(dbc.Collapse(
                dbc.Nav(
                        dbc.Col(
                            [nav_item,
                            dropdown,
                            ], width='auto'), className='ml-auto', navbar=True,
                ),
                id='navbar-collapse2',
                navbar=True,
           ),))
        ],
    ),
    # color='dark',
    # dark=True,
    className='mb-5', )
###################################################################################################################
app.layout = html.Div(
    dbc.Container(
    [
        dbc.Row(dbc.Col(navbar)),
        dbc.Row(dbc.Col(html.H2('Financial Dashboard for Euronext Stock Exchange', style={'text-align':'center'}))),

        dbc.Row(
            [
             dbc.Col(html.Div(dbc.Input(id="input", placeholder='Insert ticker on Euronext', type='text'))),
             dbc.Col(html.Div(id='output3')),
             dbc.Col(html.Div(id='output')),
             dbc.Col(html.Div(id='output2')),

            ]
    ),
        dbc.Row(dbc.Col(dbc.Card(dbc.CardBody(id='linegraph-container')))),
    html.Br(),
         dbc.Row(dbc.Col(dbc.Card(dbc.CardBody(id='candlestick-container')))),

    ]
    )
)
###############################################################
# !Figure out how to combine multiple outputs so that i can get a linegraph and candlestick chart under input box
@app.callback(Output('output', 'children'), [Input('input', 'value')])

def get_company_name(value):
    if value is not None:
        response = requests.get('https://www.quandl.com/api/v3/datasets/EURONEXT/{}.json?api_key={}'.format(value))
        dataset = response.json()
        company_name = dataset['dataset']['name']
        return company_name

@app.callback(Output('output2', 'children'), [Input('input', 'value')])

def get_latest_close(value):
    if value is not None:
        response = requests.get('https://www.quandl.com/api/v3/datasets/EURONEXT/{}.json?api_key={}'.format(value))
        dataset = response.json()
        latest_close = dataset['dataset']['data'][0][4]
        return 'The latest close is: ' + str(latest_close)

@app.callback(Output('output3', 'children'), [Input('input', 'value')])
def get_market(value):
    if value is not None:
        response = requests.get('https://www.quandl.com/api/v3/datasets/EURONEXT/{}.json?api_key={}'.format(value))
        data = response.json()
        dataset = data['dataset']['description']
        split_dataset = dataset.split("<br>")
        market = split_dataset[2]
        return market

@app.callback(
    [Output(component_id='linegraph-container', component_property='children'),
    Output(component_id='candlestick-container', component_property='children')],
    [Input(component_id='input', component_property='value')])


def get_ohlc_df(value):
    if value is not None:
        response = requests.get('https://www.quandl.com/api/v3/datasets/EURONEXT/{}.json?api_key={}'.format(value))
        json_file = response.json()
        data = json_file['dataset']['data']
        df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
        df = df[::-1]

        fig = px.line(df,x= df['date'],y=df['close'],
                      title='Stock price evolution',
                    )
        fig.layout.update(
            template='ggplot2',
            title_x=0.5,
        ),
        fig.update_traces(line_color='#456987')

        fig2 = go.Figure(data=[go.Candlestick(x=df['date'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])])
        fig2.layout.update(
            template='ggplot2'
        )
        return dcc.Graph(id='linegraph-container',
                    figure=fig
                    ),dcc.Graph(id='candlestick-container',
                    figure=fig2)
    else:
        return '',''



#################################################################
if __name__ == '__main__':
    app.run_server(debug=True, port=8000,)

