from datastore.load_data import LoadAllData
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import Dash, dcc, html, Input, Output, State
from datastore import lookup as lp
import plotly.express as px
import pandas as pd


data = LoadAllData()
app = Dash(__name__)

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
            # WE CAN PUT THE SLIDERS HERE
        # ], style ={"width": "400px", "float": "left","background-color": "#010915","position": "relative"}),
            html.Div([
                        html.Button('CO2 PREDICTION', id='submit', n_clicks=0),
                        html.Button('RESET', id='reset', n_clicks=0),
                    ],style = {"margin-bottom": "18px","padding": "10px","position": "relative",'font-size': '12px', 'width': '600px', 'display': 'inline-block', 'height':'10px'}),
        ], style = {"background-color": "#010915","margin-bottom": "10px","padding": "10px","position": "relative"}),

        

        html.Div([
            dcc.Graph(id = 'graph',config = {'displayModeBar': 'hover'}),

        ]),
    ]),

], style = {"display": "flex", "flex-direction": "column"})


@app.callback(
    Output("graph", "figure"), 
    [Input(component_id="country_dropdown",  component_property='value')],
    [Input("submit", 'n_clicks')],
    
    )

def update_line_chart(country, n_clicks):
    # x=format(n_clicks)
    if country!="World CO2 Emission":
        df = data.get_all_data().query("Country==@country")
        # co2 =data.get_co2_prediction(2021, country, biofuel=0.4, other_renewable_exc_biofuel=0.2, solar=0.4) # value of co2
 
        df_country = df[['Country','Year','CO2EQ']].copy()
        df_country.drop(df_country.tail(1).index,inplace=True)
        
        df_prediction =pd.DataFrame([(country,2030,35677)],# Values to be substituted with prediction results
	            columns=('Country','Year','CO2EQ'))
        df_results=df_country.append(df_prediction)
        print(n_clicks)

        
        if n_clicks:
            fig = px.line(df_results, x=df_results['Year'], y=df_results['CO2EQ'], title=country + " CO2 Emission", color="Country")
            fig.update_layout(template='plotly_dark')
            n_clicks = 0
            return fig
        else:
            fig = px.line(df_country, x=df_country['Year'], y=df_country['CO2EQ'], title=country + " CO2 Emission", color="Country")
            fig.update_layout(template='plotly')
            return fig

    else:
        df_world = data.get_coutry_co2()
        fig = px.line(df_world,  x=df_world['Year'], y=df_world['CO2 Emmisions in Billion metric tons'],color="green")
        fig.update_layout(template='plotly')
        return fig

@app.callback(Output('submit','n_clicks'),
             [Input('reset','n_clicks')])
def update(reset):
    return 0


app.run_server(debug=False)