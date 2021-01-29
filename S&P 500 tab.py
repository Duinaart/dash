import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import yahoo_fin.stock_info as si

import pandas as pd
import requests

import plotly.graph_objects as go
import plotly.express as px

from dash.dependencies import Input, Output

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
            dbc.Row(dbc.Col(dbc.NavbarToggler(id='navbar-toggler3'))),
            dbc.Row(dbc.Col(dbc.Collapse(
                dbc.Nav(
                        dbc.Col(
                            [nav_item,
                            dropdown,
                            ], width='auto'), className='ml-auto', navbar=True,
                ),
                id='navbar-collapse3',
                navbar=True,
           ),))
        ],
    ),
    # color='dark',
    # dark=True,
    className='mb-5', )

###################################################################################################################
body2 = html.Div(
    dbc.Container(
    [
        dbc.Row(dbc.Col(navbar)),
        dbc.Row(dbc.Col(html.H2('Financial Dashboard for S&P 500', style={'text-align':'center'}))),
        dbc.Row(dbc.Col(html.Br())),
        dbc.Row(
            [
            dbc.Col(html.Div(dbc.Input(id="inputsp", placeholder='Insert ticker on S&P 500', type='text'))),
            dbc.Col(html.Div(id='output2sp')),
            dbc.Col(html.Div(id='outputsp')),
            ]),
        dbc.Row(dbc.Col(dbc.Card(dbc.CardBody(id='linegraph-container-sp')))),

    ]
    )
)
