from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("AllData2Pivot.csv")


def prepare_energy_mix_df(df: pd.DataFrame, suffix: str = 'Production') -> pd.DataFrame:
    df_energy_mix = df.copy()
    df_energy_mix = df_energy_mix[['Year', 'Country'] + [col for col in df_energy_mix.columns if col.endswith(suffix)]]
    df_energy_mix_world = df_energy_mix.groupby("Year").sum([col for col in df_energy_mix.columns if col.endswith(suffix)]).reset_index()
    df_energy_mix_world['Country'] = 'World'
    df_out = pd.concat([df_energy_mix, df_energy_mix_world], axis=0)
    return df_out


df_energy_mix = prepare_energy_mix_df(df)

app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div([  # ----------ENERGY MIX----------------------------------
        html.H1('TEAM102', style={'textAlign': 'center'}),
        html.H3('Production Energy Mix'),

        html.Label([
            "Select Country",
            dcc.Dropdown(
                id='country_dropdown',
                clearable=False,
                options=[
                    {'label': c, 'value': c}
                    for c in
                    sorted(df['Country'].unique().tolist())],
                value='World',
                placeholder="World",
                style=dict(
                    width='40%',
                    verticalAlign="left",
                    margin="4px",
                    padding="4px"
                )),
            dcc.Graph(id="energy_mix_graph"), ],
            style={"height": "60%", "width": "70%", "margin-left": "10px", "margin-top": "19px"}),

        html.Div([  # -----------FIRST LAYOUT-----------------------------------
            html.H3('CO2 Emision Model'),

            html.Label([
                "Select Energy Source",
                dcc.Dropdown(
                    id='energy_dropdown', clearable=False,
                    value='CoalConsumption', options=[
                        {'label': c, 'value': c}
                        for c in
                        ['BiofuelConsumption', 'BiofuelElectricity', 'CoalConsumption', 'GasConsumption',
                         'GasElectricity',
                         'HydroConsumption']],
                    placeholder="CoalConsumption",
                    style=dict(
                        width='40%',
                        verticalAlign="left",
                        margin="4px",
                        padding="4px"
                    )),
                dcc.Graph(id="graph"), ],
                style={"height": "60%", "width": "70%", "margin-left": "10px", "margin-top": "19px"})

        ]),

        html.Div([  # -----------SECOND LAYOUT-----------------------------------
            html.H3('Population growth Model'),

            html.Label([
                "###",
                dcc.Dropdown(
                    id='energy_dropdown2', clearable=False,
                    value='###', options=[
                        {'label': c, 'value': c}
                        for c in
                        ['BiofuelConsumption', 'BiofuelElectricity', 'CoalConsumption', 'GasConsumption',
                         'GasElectricity',
                         'HydroConsumption']],
                    placeholder="###",
                    style=dict(
                        width='40%',
                        verticalAlign="left",
                        margin="4px",
                        padding="4px"
                    )),
                dcc.Graph(id="graph2"), ],
                style={"height": "60%", "width": "70%", "margin-left": "10px", "margin-top": "19px"})

        ]),

        html.Div([  # -----------THIRD LAYOUT-----------------------------------
            html.H3('GDP growth Model'),

            html.Label([
                "###",
                dcc.Dropdown(
                    id='energy_dropdown3', clearable=False,
                    value='###', options=[
                        {'label': c, 'value': c}
                        for c in
                        ['BiofuelConsumption', 'BiofuelElectricity', 'CoalConsumption', 'GasConsumption',
                         'GasElectricity',
                         'HydroConsumption']],
                    placeholder="###",
                    style=dict(
                        width='40%',
                        verticalAlign="left",
                        margin="4px",
                        padding="4px"
                    )),
                dcc.Graph(id="graph3"), ],
                style={"height": "60%", "width": "70%", "margin-left": "10px", "margin-top": "19px"})

        ]),
        html.Div([  # -----------FOURTH LAYOUT-----------------------------------
            html.H3('CO2 Prediction'),

            html.Label([
                "###",
                dcc.Dropdown(
                    id='energy_dropdown4', clearable=False,
                    value='###', options=[
                        {'label': c, 'value': c}
                        for c in
                        ['BiofuelConsumption', 'BiofuelElectricity', 'CoalConsumption', 'GasConsumption',
                         'GasElectricity',
                         'HydroConsumption']],
                    placeholder="###",
                    style=dict(
                        width='40%',
                        verticalAlign="left",
                        margin="4px",
                        padding="4px"
                    )),
                dcc.Graph(id="graph4"), ],
                style={"height": "60%", "width": "70%", "margin-left": "10px", "margin-top": "19px"})

        ])
    ])
])


@app.callback(
    Output("graph", "figure"),
    Input("energy_dropdown", "value"))
def update_line_chart(value):
    df = pd.read_csv("AllData2Pivot.csv")
    fig = px.line(df, x="Year", y=value, color='Country')
    fig.update_layout(template='plotly_dark')
    return fig


@app.callback(
    Output("energy_mix_graph", "figure"),
    Input("country_dropdown", "value"))
def update_energy_mix_chart(value):
    fig = px.line(df_energy_mix.query("Country == @value"),
                  x="Year",
                  y=[col for col in df_energy_mix.columns if col.endswith('Production')],
                  title=f"{value} Energy Mix",
                  )
    fig.update_layout(yaxis_title="Energy Production Sources", template='plotly_dark')
    return fig


app.run_server(debug=True)
