import os
from dotenv import load_dotenv


import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from utils import zoom_center
from data import load_data
from components import get_location_table, get_content

load_dotenv()

app =   dash.Dash(__name__)

token = os.getenv('MAPBOX_TOKEN')

# Create the app
app = dash.Dash(
    name=__name__,
    external_stylesheets=[dbc.themes.LUX],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)
server = app.server

# Define the layout
def layout():
    global df 
    df = load_data()
    content = get_content(df)

    return content    

df = load_data()
app.layout = layout

# Define the callback functions
@app.callback(
    Output('plot', 'figure'),
    Output('location-details', 'children'),
    Input('category-dropdown', 'value'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_plot(selected_location, start_date, end_date):
    # Filter the data based on the selected category and date range
    filtered_df = df[(df['location_of_interest'] == selected_location) | (
        selected_location == 'All')]
    filtered_df = filtered_df[(filtered_df['date_actual'] >= start_date) & (
        filtered_df['date_actual'] <= end_date)]

    zoom, center = zoom_center(
        lons=filtered_df['longitude'],
        lats=filtered_df['latitude']
    )
    # Create the plot
    fig = px.density_mapbox(filtered_df, lat='latitude', lon='longitude', radius=10,
                            center=center, zoom=zoom, height=900)
    fig.update_layout(mapbox_style="light", mapbox_accesstoken=token)

    table = get_location_table(filtered_df)

    return (fig, table)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
