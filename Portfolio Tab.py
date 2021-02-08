import dash
import dash_table

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

from euronext import nav_item
from euronext import dropdown



# Light theme: LUX, dark theme: DARKLY (enable darktheme in navbar)
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
##############################################################
""" Data wrangling for datatable"""
df = pd.read_csv('Dashboard_columns.csv')

df['Acquisition Date'] = pd.to_datetime(df['Acquisition Date']).dt.date
df = df.rename(
    columns={'Acquisition Date': 'Acquisition', 'Pct of portfolio': '% Portfolio', 'Ticker Adj Close': 'Adj Close',
             'Share Value': 'Total Value (€)', 'SP Return': 'S&P Return', 'Cost Basis': 'Cost Basis (€)',})

df['T R filtering'] = df['Ticker Return'] * 100
df['SP R filtering'] = df['S&P Return'] * 100
df['S YTD filtering'] = df['Share YTD'] * 100
df['% oH filtering'] = df['% off High'] * 100

format_mapping = {
    'Cost Basis (€)':'{:,.2f}',
    'Total Value (€)':'{:,.2f}',
    '% Portfolio': "{:.2%}",
    'Share YTD': "{:.2%}",
    '% off High': "{:.2%}",
    'Ticker Return': "{:.2%}",
    'S&P Return': "{:.2%}",
}
for key, value in format_mapping.items():
    df[key] = df[key].apply(value.format)
df = df.round(2)
###############################################################
nav_item = nav_item

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
            dbc.Row(dbc.Col(dbc.NavbarToggler(id='navbar-toggler4'))),
            dbc.Row(dbc.Col(dbc.Collapse(
                dbc.Nav(
                    dbc.Col(
                        [nav_item,
                         dropdown,
                         ], width='auto'), className='ml-auto', navbar=True,
                ),
                id='navbar-collapse4',
                navbar=True,
            ), ))
        ],
    ),
    className='mb-5', )
###################################################################################################################
body3 = html.Div(
    dbc.Container(
    [
        dbc.Row(dbc.Col(dcc.Store(id='memory-output3'))),
        dbc.Row(dbc.Col(navbar)),
        dbc.Row(dbc.Col(html.H2('Portfolio Dashboard', style={'text-align': 'center'}))),
        dbc.Row(dbc.Col(html.Br())),
        dbc.Row(dbc.Col(
            dash_table.DataTable(
                id='datatable',
                data=df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.loc[:-4]],
                fixed_columns={'headers': True, 'data': 1},
                sort_action='native',
                style_cell={
                    # all three widths are needed
                    'minWidth': '160px', 'width': '160px', 'maxWidth': '160px',
                    'overflow': 'hidden',
                },
                style_cell_conditional= [{'if': {'column_id': 'T R filtering'},'display': 'None'},
                                         {'if': {'column_id': 'SP R filtering'},'display': 'None'},
                                         {'if': {'column_id': 'S YTD filtering'},'display': 'None'},
                                         {'if': {'column_id': '% oH filtering'},'display': 'None'}],
                style_table={'minWidth': '100%', },
                style_header=
                {'textAlign': 'left',
                 'backgroundColor': '#dae2e2',
                 'fontWeight': 'bold'
                 },
                style_data={'textAlign': 'left'},
                style_data_conditional=
                #* Background color of cells
                [{'if': {'column_id': c, 'row_index': 'even'}, 'backgroundColor': '#b0dbc1'} for c in ['Ticker']]
                + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#75c093'} for c in ['Ticker']]
                + [{'if': {'column_id': c, 'row_index': 'even'}, 'backgroundColor': '#fef9e7'} for c in ['Acquisition', 'Quantity', 'Unit Cost', 'Cost Basis (€)', '% Portfolio']]
                + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#FCF3CF'} for c in ['Acquisition', 'Quantity', 'Unit Cost', 'Cost Basis (€)', '% Portfolio']]
                + [{'if': {'column_id': c, 'row_index': 'even'}, 'backgroundColor': '#EBF5FB'} for c in ['Adj Close', 'Ticker Return', 'S&P Return', 'Total Value (€)', 'Share YTD']]
                + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#D6EAF8'} for c in ['Adj Close', 'Ticker Return', 'S&P Return', 'Total Value (€)', 'Share YTD']]
                + [{'if': {'column_id': c, 'row_index': 'even'}, 'backgroundColor': '#fcf2f2'} for c in ['% off High', 'Volatility', 'Beta']]
                + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#fae5e5'} for c in ['% off High', 'Volatility', 'Beta']]
                #* Data color of cells
                + [{'if': {'filter_query': '{T R filtering} > {SP R filtering}','column_id': 'Ticker Return'}, 'color': 'darkgreen'}]
                + [{'if': {'filter_query': '{T R filtering} < {SP R filtering}', 'column_id': 'Ticker Return'}, 'color': 'crimson'}]
                + [{'if': {'filter_query': '{S YTD filtering} > 0', 'column_id': 'Share YTD'}, 'color': 'darkgreen'}]
                + [{'if': {'filter_query': '{S YTD filtering} < 0', 'column_id': 'Share YTD'}, 'color': 'crimson'}]

                ,
                style_as_list_view=True,
                css=[{'selector': '.dash-cell div.dash-cell-value',
                      'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
            )))
    ]
    )
)
