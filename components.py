
from dash import dcc, html
import dash_bootstrap_components as dbc

import numpy as np

def get_content(df):
    content = dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div(
                    [
                        html.H2("Location", className="display-5"),
                        html.Hr(),
                        get_controls(df)
                    ],
                    className="d-flex flex-column flex-shrink-0 p-3 bg-light",
                ),
                md=3
            ),
            dbc.Col(
                [
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                dcc.Graph(id='plot'),
                                body=True
                            )
                        )
                    ),
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                html.Div(id="location-details"),
                                body=True
                            )
                        )
                    ),
                ],
                md=9
            )
        ]
        ),
        dcc.Location(id='url')],
    )
    
    return content

def get_controls(df):
    locations = df['location_of_interest'].unique()
    locations = np.insert(locations, 0, 'All')

    content = html.Div([dbc.Card(
        [
            dbc.Label("Month"),
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': c, 'value': c} for c in locations],
                value='All'
            ),
        ],
        body=True,
    ),
        dbc.Card(
        [
            dbc.Label("Main category"),
            dcc.DatePickerRange(
                id='date-range-picker',
                start_date=df['date_actual'].min(),
                end_date=df['date_actual'].max()
            ),
        ],
        body=True,
    )])
    return content

def get_location_table(df):
    df_grouped = df.groupby(['date_actual'])[['duration_minutes', 'distance_meter']].sum().reset_index().sort_values(by='date_actual', ascending=False)
    
    df_grouped['distance_meter'] =df_grouped['distance_meter']/1000
    df_grouped['distance_meter'] =df_grouped['distance_meter'].map('{:,.2f}'.format)

    df_grouped['duration_minutes'] =df_grouped['duration_minutes']/60
    df_grouped['duration_minutes'] =df_grouped['duration_minutes'].map('{:,.2f}'.format)

    table_header = [
        html.Thead(html.Tr([
            html.Th("Date"), 
            html.Th("Duration"), 
            html.Th("Distance (km)"), 
        ]))
    ]

    table_rows = []
    for index, row in df_grouped.iterrows():
        table_rows.append(html.Tr([
            html.Td(row['date_actual']), 
            html.Td(row['duration_minutes'], style={"text-align": "right"}), 
            html.Td(row['distance_meter'], style={"text-align": "right"}), 
            
        ]))

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, className="details-table")

    return table