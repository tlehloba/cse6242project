from datastore.load_data import LoadAllData
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import Dash, dcc, html, Input, Output
from datastore import lookup as lp
import plotly.express as px
import pandas as pd


data = LoadAllData()
app = Dash(__name__)


# app.layout = html.Div(children=[
#      html.Div([#-----------FIRST LAYOUT-----------------------------------
#       html.H1('TEAM102',style={'textAlign': 'center',
#                              'backgroundColor' : '#DBDDDB',
#                              'color' : 'gray'}),
#     html.H3('CO2 Emision Model'),

#     html.Label([
#         "Select_Country",
#     dcc.Dropdown(
#         # df = data.get_all_data(),
#         id='country_dropdown', clearable=True,
#             value='country_dropdown', options=[
#                 {'label': c, 'value': c}
#                 for c in 
#                 data.get_all_countries()],
#             placeholder="Countries CO2 Emission",
#             style=dict(
#             width='40%',
#             verticalAlign="left",
#             margin = "4px",
#             padding ="4px"
#         )),
#     dcc.Graph(id="graph"),], style={"height": "60%", "width": "40%", "margin-left":"10px", "margin-top":"19px","margin-right":"20px"})
   
   
#     ]),
# ])


app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H3('TEAM102', style = {"margin-bottom": "0px", 'color': 'white','text-align': 'center'}),
                html.H5('CSE6242', style = {"margin-top": "0px", 'color': 'white'}),

            ]),
        ], style ={"text-align": "center"}),

    ], id = "#", className = "row flex-display", style = {"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.P('Select_Country', className = 'fix_label', style = {'color': 'white'}),
            dcc.Dropdown(
            # df = data.get_all_data(),
            id='country_dropdown', clearable=True,
                value='country_dropdown', options=[
                    {'label': c, 'value': c}
                    for c in 
                    data.get_all_countries()],
                placeholder="Countries CO2 Emission",
                style=dict(
                width='40%',
                verticalAlign="left",
                margin = "4px",
                padding ="4px"
            )),

        ], style = {"border-radius": "5px","background-color": "#010915","margin": "18px","padding": "15px","position": "relative","box-shadow": "2px 2px 2px #010915"}),

        html.Div([
            dcc.Graph(id = 'graph',config = {'displayModeBar': 'hover'}),

        ])
    ]),

], style = {"display": "flex", "flex-direction": "column"})


@app.callback(
    Output("graph", "figure"), 
    [Input(component_id="country_dropdown",  component_property='value')])

def update_line_chart(country):
    if country!="World CO2 Emission":
        df = data.get_all_data().query("Country==@country")
 
        df_country = df[['Country','Year','CO2EQ']].copy()
        df_country.drop(df_country.tail(1).index,inplace=True)
        
        df_prediction =pd.DataFrame([(country,2030,25000)],# Values to be substituted with prediction results
	            columns=('Country','Year','CO2EQ'))
        df_results=df_country.append(df_prediction)
        # print(df_results)
        fig = px.line(df_results, x=df_results['Year'], y=df_results['CO2EQ'], title=country + " CO2 Emission", color="Country")
        fig.update_layout(template='plotly_dark')
        return fig
    else:
        df_world = data.get_coutry_co2()
        fig = px.line(df_world,  x=df_world['Year'], y=df_world['CO2 Emmisions in Billion metric tons'],color="green")
        fig.update_layout(template='plotly')
        return fig

app.run_server(debug=True)