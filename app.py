from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import calendar

df = pd.read_csv("Carcass_Classification_Salmon.csv")

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Licence Holder Dropdown Component
licence_holders = df['Licence Holder'].unique()

licence_dropdown = dcc.Dropdown(
        options=licence_holders,
        id = "select-licence-dropdown"
    )

# Year Slider Component
year_minimum = df["Year"].min()
year_maximum = df["Year"].max()
year_slider = html.Div([
    dcc.RangeSlider(
        df['Year'].min(),
        df['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()},
        id='year-slider'),
    html.Div(id='output-container-year-slider')
    ])


# Month Slider Component
month_slider_marks = {
    1: {"label": "Jan"},
    2: {"label": "Feb"},
    3: {"label": "Mar"},
    4: {"label": "Apr"},
    5: {"label": "May"},
    6: {"label": "Jun"},
    7: {"label": "Jul"},
    8: {"label": "Aug"},
    9: {"label": "Sep"},
    10: {"label": "Oct"},
    11: {"label": "Nov"},
    12: {"label": "Dec"}
}

month_slider = html.Div([
    dcc.RangeSlider(
        1,
        12,
        step=1,
        marks=month_slider_marks,
        id='month-slider'),
    html.Div(id='output-container-month-slider')
    ])


# Species Checklist Component
species = {str(species): str(species) for species in df['Species'].unique()}
species_checklist = dcc.Checklist(species)

# Production Information & Report Status Checklist Component
production_info = {str(prod_info): str(prod_info) for prod_info in df['Production Information & Report Status'].unique()}
production_info_checklist = dcc.Checklist(production_info)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H2("Salmon Carcass Classification for Fish Farms in British Columbia"),
        html.Hr(),
        html.H5("Licence Holder"),
        licence_dropdown,
        html.H5("Year"),
        year_slider,
        html.H5("Month"),
        month_slider,
        html.H5("Species"),
        species_checklist,
        html.H5("Production Information"),
        production_info_checklist
        
    ],
    style=SIDEBAR_STYLE,
)


app.layout = dbc.Container([
    sidebar
]
)

@app.callback(
    Output('output-container-year-slider', 'children'),
    Output('output-container-month-slider', 'children'),
    Input('year-slider', 'value'),
    Input('month-slider', 'value'))
def update_output(year, month):
    return 'You have selected "{}"'.format(year), 'You have selected "{}"'.format(month)


if __name__ == '__main__':
    app.run_server(debug=True)