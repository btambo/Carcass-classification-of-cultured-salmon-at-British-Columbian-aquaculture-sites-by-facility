from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import calendar

df = pd.read_csv("Carcass_Classification_Salmon.csv")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Licence Holder Dropdown Component
licence_dropdown = dcc.Dropdown(
        options= df['Licence Holder'].unique(),
        id = "licence-holder-dropdown",
        value= df['Licence Holder'][1],
        clearable=False
    )

# Year Slider Component
year_slider = html.Div([
    dcc.RangeSlider(
        df['Year'].min(),
        df['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()},
        id='year-slider',
        value = [2013, 2021]
        ),
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
        id='month-slider',
        value = [1, 12]),
    html.Div(id='output-container-month-slider')
    ])


# Species Checklist Component
species = {str(species): str(species) for species in df['Species'].unique()}
species_checklist = dcc.Checklist(species, id='species-selection', value=df['Species'].unique()[:], labelStyle={'display': 'block'}, style={'overflow':'auto'})

# Production Information & Report Status Checklist Component
production_info = {str(prod_info): str(prod_info) for prod_info in df['Production Information & Report Status'].unique()}
production_info_checklist = dcc.Checklist(production_info, id='production-selection', value=df['Production Information & Report Status'].unique()[:], labelStyle={'display': 'block'}, style={'overflow':'auto'})


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "4rem",
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "padding": "2rem 1rem"
}

sidebar = html.Div(
    [
        html.H5("Licence Holder"),
        licence_dropdown,
        html.H5("Year"),
        year_slider,
        html.H5("Month"),
        month_slider,
        dbc.Row([
            dbc.Col([html.H5("Species"),
                    species_checklist]),
            dbc.Col([html.H5("Production"),
                    production_info_checklist])  
        ])
    ],
    style=SIDEBAR_STYLE,
)

carcass_class_pie_chart = dcc.Graph(id='carcass-class-pie-chart')

carcass_class_geo_chart = dcc.Graph(id='carcass-class-geo-chart')

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Salmon Carcass Classification for Fish Farms in British Columbia"),
        html.Hr()
    ], style={"position": "absolute", "left": 0, "padding": "1rem", "width": "100vw"}),
    dbc.Row([
        dbc.Col(sidebar),
        dbc.Col(carcass_class_pie_chart),
    ]),
    carcass_class_geo_chart
]
)

@app.callback(
    Output('output-container-year-slider', 'children'),
    Output('output-container-month-slider', 'children'),
    Input('year-slider', 'value'),
    Input('month-slider', 'value'))
def update_output(year, month):
    return 'You have selected "{}"'.format(year), 'You have selected "{}"'.format(month)

# Update Pie Chart
@app.callback(
    Output('carcass-class-pie-chart', 'figure'),
    Input('licence-holder-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('month-slider', 'value'),
    #Input('species-selection', 'value'),
    #Input('production-selection', 'value')
    )
def update_pie_chart(licence_holder, year, month):
    filtered_df = df.loc[
        (df["Licence Holder"]==licence_holder)
        & (df['Year']>=year[0])
        & (df['Year']<=year[1])
        & (df['Month']>=month[0])
        & (df['Month']<=month[1])]

    fig = px.pie(filtered_df["Total Mortality (%/month)"], filtered_df["Production Information & Report Status"])
    return fig


# Update geo chart
@app.callback(
    Output('carcass-class-geo-chart', 'figure'),
    Input('licence-holder-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('month-slider', 'value'),
    #Input('species-selection', 'value'),
    #Input('production-selection', 'value')
    )
def update_geo_chart(licence_holder, year, month):
    filtered_df = df.loc[
        (df["Licence Holder"]==licence_holder)
        & (df['Year']>=year[0])
        & (df['Year']<=year[1])
        & (df['Month']>=month[0])
        & (df['Month']<=month[1])]

    f_df = filtered_df.mean()

    fig = px.scatter_geo(
        lon = filtered_df['Longitude'],
        lat = filtered_df['Latitude'],
        text = filtered_df['Site Common Name'],
        size = filtered_df['Total Mortality (%/month)']
        )
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)