from datastore.load_data import LoadAllData
from dash import Dash, dcc, html, Input, Output
from datastore import lookup as lp
import plotly.express as px


'''
Load All Data return df frame for the entire dataset
data.get_all_data().columns
data.get_all_countries()
data.get_all_years()
data.get_all_data_for_country()
data.get_all_data_for_country_for_year()
'''
data = LoadAllData()
app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div([  # -----------FIRST LAYOUT-----------------------------------
        html.H1('TEAM102', style={'textAlign': 'center'}),
        html.H3('CO2 Emission Prediction'),

        html.Label([
            "select_energy_source",
            dcc.Dropdown(
                id='energy_dropdown', clearable=False,
                value='CoalConsumption', options=[
                    {'label': c, 'value': c}
                    for c in
                    lp.ENERGY_MIX],
                placeholder=lp.biofuel,
                style=dict(
                    width='40%',
                    verticalAlign="left",
                    margin="4px",
                    padding="4px"
                )),
            dcc.Graph(id="graph"), ],
            style={"height": "60%", "width": "70%", "margin-left": "10px", "margin-top": "19px"})

    ]),

    # html.Div([  # -----------SECOND LAYOUT-----------------------------------
    #     html.H3('Population growth Model'),
    #
    #     html.Label([
    #         "###",
    #         dcc.Dropdown(
    #             id='energy_dropdown2', clearable=False,
    #             value='###', options=[
    #                 {'label': c, 'value': c}
    #                 for c in
    #                 ['BiofuelConsumption', 'BiofuelElectricity', 'CoalConsumption', 'GasConsumption', 'GasElectricity',
    #                  'HydroConsumption']],
    #             placeholder="###",
    #             style=dict(
    #                 width='40%',
    #                 verticalAlign="left",
    #                 margin="4px",
    #                 padding="4px"
    #             )),
    #         dcc.Graph(id="graph2"), ],
    #         style={"height": "60%", "width": "70%", "margin-left": "10px", "margin-top": "19px"})
    #
    # ]),
    #
    # html.Div([  # -----------THIRD LAYOUT-----------------------------------
    #     html.H3('GDP growth Model'),
    #
    #     html.Label([
    #         "###",
    #         dcc.Dropdown(
    #             id='energy_dropdown3', clearable=False,
    #             value='###', options=[
    #                 {'label': c, 'value': c}
    #                 for c in
    #                 ['BiofuelConsumption', 'BiofuelElectricity', 'CoalConsumption', 'GasConsumption', 'GasElectricity',
    #                  'HydroConsumption']],
    #             placeholder="###",
    #             style=dict(
    #                 width='40%',
    #                 verticalAlign="left",
    #                 margin="4px",
    #                 padding="4px"
    #             )),
    #         dcc.Graph(id="graph3"), ],
    #         style={"height": "60%", "width": "70%", "margin-left": "10px", "margin-top": "19px"})
    #
    # ]),
    # html.Div([  # -----------FOURTH LAYOUT-----------------------------------
    #     html.H3('CO2 Prediction'),
    #
    #     html.Label([
    #         "###",
    #         dcc.Dropdown(
    #             id='energy_dropdown4', clearable=False,
    #             value='###', options=[
    #                 {'label': c, 'value': c}
    #                 for c in
    #                 ['BiofuelConsumption', 'BiofuelElectricity', 'CoalConsumption', 'GasConsumption', 'GasElectricity',
    #                  'HydroConsumption']],
    #             placeholder="###",
    #             style=dict(
    #                 width='40%',
    #                 verticalAlign="left",
    #                 margin="4px",
    #                 padding="4px"
    #             )),
    #         dcc.Graph(id="graph4"), ],
    #         style={"height": "60%", "width": "70%", "margin-left": "10px", "margin-top": "19px"})
    #
    # ])
])


@app.callback(
    Output("graph", "figure"),
    Input("energy_dropdown", "value"))
def update_line_chart(select_energy_source):
    df = data.get_all_data()
    print(" CO2 Predicted:",
          data.get_co2_prediction(2021, "India", biofuel=0.4, other_renewable_exc_biofuel=0.2, solar=0.4))
    fig = px.line(df, x="Year", y=select_energy_source, color='Country')
    fig.update_layout(template='plotly_dark')
    return fig


app.run_server(debug=True)
