from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import calendar

df = pd.read_csv("Carcass_Classification_Salmon.csv")

app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}



# Navigation Bar Component
navbar = dbc.Navbar (
    html.A(dbc.NavbarBrand("Carcass Classification of Aquaculture Salmon in BC"))
)

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

# Sidebar Component
sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Container(
            [
                licence_dropdown,
                year_slider,
                month_slider,
                species_checklist,
                production_info_checklist
            ]
        ),
    ],
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = dbc.Container([
    html.H1("Carcass Classifications of Farmed Salmon in British Columbia"),
    html.Hr(),
    dbc.Row(
        [
            dbc.Col(sidebar),
            dbc.Col(html.H1("test")),
        ],
        align="center",
        ),
    ],
    fluid=True,
)

# app.layout = dbc.Container(
#     children= [
#     navbar,
#     licence_dropdown,
#     year_slider,
#     month_slider,
#     species_checklist,
#     production_info_checklist
#     ]
# )






@app.callback(
    Output('output-container-year-slider', 'children'),
    Output('output-container-month-slider', 'children'),
    Input('year-slider', 'value'),
    Input('month-slider', 'value'))
def update_output(year, month):
    return 'You have selected "{}"'.format(year), 'You have selected "{}"'.format(month)


if __name__ == '__main__':
    app.run_server(debug=True)