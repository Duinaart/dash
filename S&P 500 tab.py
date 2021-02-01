import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from euronext import nav_item
from euronext import dropdown
from euronext import navbar

# Light theme: LUX, dark theme: DARKLY (enable darktheme in navbar)
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
##############################################################


###############################################################
# Make a navigation bar (dropdown items)
## Make a reusable navitem for different dashboards
nav_item = nav_item

## Make a Reusable dropdown for different dashboards
dropdown = dropdown

# Navigation Bar layout
navbar = dbc.Navbar(
    dbc.Container(  # A container keeps the content of the rows and columns into one single blob that can be moved
        [
            # Use row and col to control vertical alignment of logo
            dbc.Row(
                [dbc.Col((html.Img(
                    src='https://prismic-io.s3.amazonaws.com/plotly-marketing-website/bd1f702a-b623-48ab-a459-3ee92a7499b4_logo-plotly.svg',
                    height='30px')), width='auto'),
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
            ), ))
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
            dbc.Row(dbc.Col(html.H2('Financial Dashboard for S&P 500', style={'text-align': 'center'}))),
            dbc.Row(dbc.Col(html.Br())),
            dbc.Row(
                [
                    dbc.Col(html.Div(
                        dbc.Input(id="inputsp", value='AAPL', debounce=True,))),
                    dbc.Col(html.Div(id='output2sp', style={'text-align': 'center'})),
                    dbc.Col(html.Div(id='outputsp', style={'text-align': 'center'})),
                ]),
            dbc.Row(dbc.Col(dbc.Card(dcc.Graph(id='linegraph-container-sp', figure={})))),

        ]
    )
)
