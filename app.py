# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go 
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__ ,meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
app.config.suppress_callback_exceptions=True
# - - - - - - - - - - - - - - #
# Functions definitions
# - - - - - - - - - - - - - - #


# - - - - - - - - - - - - - - #
# Loading data
# - - - - - - - - - - - - - - #

df = pd.read_csv('data/GCB2020v18_MtCO2_flat.csv',sep=',',encoding='latin-1')
df = df.loc[df.Year > 1950]
country='Global'
df_without_Total = df.loc[df.Country != 'Global']

df_continent = pd.read_csv('data/Countries-Continents.csv',encoding='latin-1')
df2 = df_without_Total
df2.loc[df2.Country == 'USA', 'Country'] = 'United States'
df_with_continent = pd.merge(
  df2, 
  df_continent, 
  left_on='Country', 
  right_on='Country',
  how="left",
)

df_with_continent = df_with_continent.loc[ df_with_continent.Continent.isin(['asia', 'europe', 'africa','north america', 'south america','oceania'])]

# - - - - - - - - - - - - - - #
# Defining figures
# - - - - - - - - - - - - - - #

def map_fig(dataframe,value):

    if value != 'world':
        fig = px.choropleth(dataframe.loc[dataframe['Continent'] == value ], locations="ISO 3166-1 alpha-3",
                        color="Total",
                        hover_name="Country", 
                        animation_frame = "Year",
                        color_continuous_scale=[[0,'rgb(54, 233, 18)'],[0.005,'rgb(230, 233, 18)'],[0.4,'rgb(233, 145, 18)'],[1,'rgb(233, 18, 18)']],
                        title="Evolution of CO2 Global Emission (MtCO2)",
                        height=800,
                        scope = value,
                        projection = 'miller',
                        template = 'ggplot2'
                        )
    
    else:
        fig = px.choropleth(dataframe, locations="ISO 3166-1 alpha-3",
                        color="Total",
                        hover_name="Country", 
                        animation_frame = "Year",
                        color_continuous_scale=[[0,'rgb(54, 233, 18)'],[0.005,'rgb(230, 233, 18)'],[0.4,'rgb(233, 145, 18)'],[1,'rgb(233, 18, 18)']],
                        title="Evolution of CO2 Global Emission (MtCO2)",
                        height=800,
                        projection = 'miller',
                        template = 'ggplot2'
                        )

    


    return fig 


def plot_fig(country):
    Total = go.Scatter(
        x = df.loc[df.Country == country]['Year'],
        y = df.loc[df.Country == country]['Total'],
        mode='lines+markers',
        name= 'Total'
    )
    Coal = go.Scatter(
        x = df.loc[df.Country == country]['Year'],
        y = df.loc[df.Country == country]['Coal'],
        name= 'Coal'
    )
    Oil = go.Scatter(
        x = df.loc[df.Country == country]['Year'],
        y = df.loc[df.Country == country]['Oil'],
        name= 'Oil'
    )
    Gas = go.Scatter(
        x = df.loc[df.Country == country]['Year'],
        y = df.loc[df.Country == country]['Gas'],
        name= 'Gas'
    )
    Cement = go.Scatter(
        x = df.loc[df.Country == country]['Year'],
        y = df.loc[df.Country == country]['Cement'],
        name= 'Cement'
    )
    Flaring = go.Scatter(
        x = df.loc[df.Country == country]['Year'],
        y = df.loc[df.Country == country]['Flaring'],
        name= 'Flaring'
    )
    Other = go.Scatter(
        x = df.loc[df.Country == country]['Year'],
        y = df.loc[df.Country == country]['Other'],
        name= 'Other'
    )
    data = go.Data([Total, Coal, Oil, Gas, Cement,Flaring,Other])

    layout = go.Layout(
        title = f"CO2 Emission of {country} over the years",
        xaxis = go.XAxis(
            title = "Year",
        ),
        yaxis = go.YAxis(
            title = "CO2 Emission (MtCO2)",
        )
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

def plot_per_capita(country):
    Total = go.Scatter(
        x = df.loc[df.Country == country]['Year'],
        y = df.loc[df.Country == country]['Per Capita'],
        name= 'Total'
    )
    data = go.Data([Total])

    layout = go.Layout(
        title = f"{country} Emission per capita (tCO2)",
        xaxis = go.XAxis(
            title = "Year",
        ),
        yaxis = go.YAxis(
            title = "CO2 Emission per capita",
        )
    )

    figure = go.Figure(data=data, layout=layout)
    return figure

def plot_bar(country):
    Coal = go.Bar(
        x = ['Coal'],
        y = df.loc[(df.Year == 2019) & (df.Country == country)]['Coal'],
        name= 'Coal'
    )
    Oil = go.Bar(
        x = ['Oil'],
        y = df.loc[(df.Year == 2019) & (df.Country == country)]['Oil'],
        name= 'Oil'
    )
    Gas = go.Bar(
        x = ['Gas'],
        y = df.loc[(df.Year == 2019) & (df.Country == country)]['Gas'],
        name= 'Gas'
    )
    Cement = go.Bar(
        x = ['Cement'],
        y = df.loc[(df.Year == 2019) & (df.Country == country)]['Cement'],
        name= 'Cement'
    )
    Flaring = go.Bar(
        x = ['Flaring'],
        y = df.loc[(df.Year == 2019) & (df.Country == country)]['Flaring'],
        name= 'Flaring'
    )
    Other = go.Bar(
        x = ['Other'],
        y = df.loc[(df.Year == 2019) & (df.Country == country)]['Other'],
        name= 'Other'
    )
    data = go.Data([Coal, Oil, Gas, Cement,Flaring,Other])

    layout = go.Layout(
        title = f"{country} CO2 Emission of 2019",
        xaxis = go.YAxis(
            title = "Fossil fuels",
        ),

        yaxis = go.YAxis(
            title = "CO2 Emission (MtCO2)",
        )
    )

    figure = go.Figure(data=data, layout=layout)
    return figure
# - - - - - - - - - - - - - - #
# App layout
# - - - - - - - - - - - - - - #
def build_map():
    return html.Div(
        id="map",
        className="map",
        children=[
        dcc.Dropdown(
            id='map-dropdown',
            options=[
                {'label': 'World', 'value': 'world'},
                {'label': 'North America', 'value': 'north america'},
                {'label': 'Asia', 'value': 'asia'},
                {'label': 'South america', 'value': 'south america'},
                {'label': 'Africa', 'value': 'africa'},
                {'label': 'Europe', 'value': 'europe'},
            ],
            value = 'world',
            style={"width": "50%"},
        ),

        

        dcc.Graph(
            id='map-graph',
            figure= map_fig(df_with_continent,'world'),

        )


        ])

def build_graph():

    return html.Div(
        id='graph',
        className='graph',
        children=[

    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': country, 'value': country} for country in df['Country'].unique()
        ],
        placeholder="Select a Country",
        value = 'World',
        style={"width": "50%"},
    ),

    dcc.Graph(
        id='example-graph',
        figure=plot_fig(country),
    ),

    dcc.Graph(
        id='bar-graph',
        figure=plot_bar(country),
    ),
    dcc.Graph(
        id='capita-graph',
        figure=plot_per_capita(country),
    ),



        ])

def build_tab():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Graph",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Map",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )





app.layout = html.Div(children=[
    html.Div(
        className="header-title",
        children=[
            html.H1(
                id="title",
                children="Global CO2 Emission",
                style={'text-align':'center', 'fontSize': 74, "fontWeight": "bold", "color": "inherit",}

            ),
        ],
    ),

    html.Div(
        id="tab-container",
        children=[
            build_tab(),
            # Main app
            html.Div(id="tab-content"),
        ],
    ),


])


# - - - - - - - - - - - - - - #
# App call backs
# - - - - - - - - - - - - - - #

@app.callback(
    Output("tab-content", "children"),
    Input("app-tabs","value")
)
def select_builder(value):
    if value == 'tab1':
        return build_graph()
    else: 
        return build_map()

@app.callback(
    Output('example-graph', 'figure'),
    Input('demo-dropdown', 'value')
)

def update_fig(value):
    return plot_fig(value)

@app.callback(
    Output('bar-graph', 'figure'),
    Input('demo-dropdown', 'value')
)

def update_bar(value):
    return plot_bar(value)

@app.callback(
    Output('capita-graph', 'figure'),
    Input('demo-dropdown', 'value')
)

def update_capita(value):
    return plot_per_capita(value)


@app.callback(
    Output('map-graph', 'figure'),
    Input('map-dropdown', 'value')
)
def update_map(value):
    return map_fig(df_with_continent,value)

# - - - - - - - - - - - - - - #
# App Main
# - - - - - - - - - - - - - - #

if __name__ == '__main__':
    app.run_server(debug=True)
