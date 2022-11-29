
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 22:24:46 2022

@author: afrob
"""
from dash import ctx
import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input, State
from datastore.load_data import LoadAllData
import os
import plotly.express as px
import datastore.lookup as lp
from PIL import Image

DefaultCountry = 'Global'
DefaultYear = 2019
DefaultPrediction = 10  # years

data_loader = LoadAllData()
data = data_loader.get_all_data()

# Tempoary logo file for demo
image_path = 'team102logo.png'
pil_img = Image.open(image_path)

def SetEnergyMix(Country=DefaultCountry, Year=DefaultYear):
    # --------------------------------------------------------------------
    # Outputs the energy mix percentage passed from the datafile.
    # Converts to % for ease of user
    # Replace with call to data class
    # --------------------------------------------------------------------
    Coal = data.loc[(data['Country'] == Country) & (data['Year'] == Year), 'Coal_%'].astype('float').round(2).values[0] * 100
    Oil = data.loc[(data['Country'] == Country) & (data['Year'] == Year), 'Oil_%'].astype('float').round(2).values[0] * 100
    Gas = data.loc[(data['Country'] == Country) & (data['Year'] == Year), 'Gas_%'].astype('float').round(2).values[0] * 100
    Solar = data.loc[(data['Country'] == Country) & (data['Year'] == Year), 'Solar_%'].astype('float').round(2).values[0] * 100
    Wind = data.loc[(data['Country'] == Country) & (data['Year'] == Year), 'Wind_%'].astype('float').round(2).values[0] * 100
    Hydro = data.loc[(data['Country'] == Country) & (data['Year'] == Year), 'Hydro_%'].astype('float').round(2).values[0] * 100
    Nuclear = data.loc[(data['Country'] == Country) & (data['Year'] == Year), 'Nuclear_%'].astype('float').round(2).values[0] * 100
    Biofuel = data.loc[(data['Country'] == Country) & (data['Year'] == Year), 'Biofuel_%'].astype('float').round(2).values[0] * 100
    OtherRenew = \
    data.loc[(data['Country'] == Country) & (data['Year'] == Year), 'OtherRenewableExcBiofuel_%'].astype('float').round(2).values[0] * 100

    return Coal, Oil, Gas, Solar, Wind, Hydro, Nuclear, Biofuel, OtherRenew


def SetZero():  # (Coal,Oil,Gas,Solar,Wind,Hydro,Nuclear,Biofuel,OtherRenew):
    # --------------------------------------------------------------------
    #
    # Sets all to 0%
    #
    # --------------------------------------------------------------------
    Coal = 0
    Oil = 0
    Gas = 0
    Solar = 0
    Wind = 0
    Hydro = 0
    Nuclear = 0
    Biofuel = 0
    OtherRenew = 0

    print("Inside Zero function")
    return Coal, Oil, Gas, Solar, Wind, Hydro, Nuclear, Biofuel, OtherRenew


def SumTotal(Coal=0, Oil=0, Gas=0, Solar=0, Wind=0, Hydro=0, Nuclear=0, Biofuel=0, OtherRenew=0):
    # --------------------------------------------------------------------
    #
    # Sum all percentages. defaults to 0 if a value is not passed
    #
    # --------------------------------------------------------------------

    Total = Coal + Oil + Gas + Solar + Wind + Hydro + Nuclear + Biofuel + OtherRenew
    return int(Total)
# def PlotCO2_WithPredictions(Prediction,Country):
#
#     fig = px.line(Prediction, x='Year', y='CO2EQ', title=Country+ " CO2 Emission")
#     fig.update_layout(template='plotly_dark')
#
#     return fig
#
#
# def PlotCO2_NoPredictions(Country):
#
#     fig = px.line(data_loader.get_global_co2(Country), x='Year', y='CO2EQ',
#                   title=Country + " CO2 Emission")
#     fig.update_layout(template='plotly')
#     return fig

def CorrectSum( CoalValue,
                OilValue,
                GasValue,
                SolarValue,
                WindValue,
                HydroValue,
                NuclearValue,
                BiofuelValue,
                OtherRenewValue):


        tuple_values = [CoalValue,
                              OilValue,
                              GasValue,
                              SolarValue,
                              WindValue,
                              HydroValue,
                              NuclearValue,
                              BiofuelValue,
                              OtherRenewValue]

        sum_difference = 100 - int(np.sum(tuple_values))
        print(tuple_values)
        print(sum_difference)
        if sum_difference > 0:
            for _ in range(sum_difference):
                i = np.random.randint(len(tuple_values))
                if tuple_values[i] < 100 :
                    tuple_values[i] = tuple_values[i] + 1
            CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue = tuple_values
        elif sum_difference < 0:
            for _ in range(abs(sum_difference)):
                i = np.random.randint(len(tuple_values))
                if tuple_values[i] > 0 :
                    tuple_values[i]-= 1
            CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue = tuple_values
        else:
            pass
        print(tuple_values)
        sum_difference = 100 - int(np.sum(tuple_values))
        print(sum_difference)
        return CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue

def LastYear(Country):
    #----------------------------------------------------
    # Checks for the last year the CO2 emissions is not 0
    #----------------------------------------------------
    maxyear = 1960
    for row in data[data['Country']==Country].itertuples():
        if row.CO2EQ > 0:
            maxyear = row.Year
    return maxyear

# Set initial values from default country and year.
# Replace with World totals in final implementation

CoalDefault, OilDefault, GasDefault, SolarDefault, WindDefault, HydroDefault, NuclearDefault, BiofuelDefault, OtherRenewDefault = SetEnergyMix(DefaultCountry, DefaultYear)

CoalDefault, OilDefault, GasDefault, SolarDefault, WindDefault, HydroDefault, NuclearDefault, BiofuelDefault, OtherRenewDefault = CorrectSum(CoalDefault,
                                                                                                                                             OilDefault,
                                                                                                                                             GasDefault,
                                                                                                                                             SolarDefault,
                                                                                                                                             WindDefault,
                                                                                                                                             HydroDefault,
                                                                                                                                             NuclearDefault,
                                                                                                                                             BiofuelDefault,
                                                                                                                                             OtherRenewDefault)

TotalMix = SumTotal(CoalDefault, OilDefault, GasDefault, SolarDefault, WindDefault, HydroDefault, NuclearDefault,
                    BiofuelDefault, OtherRenewDefault)
maxlen = 0
for country in data.Country.unique():
    if len(country) > maxlen:
        maxlen = len(country)
CountryMaxWidth = data.Country.str.len().max()

# --------------------------------------------------------------
# define styles. Replace with css if possible

FontStandard = 'Arial'
TitleColor = 'darkslategrey'
HeaderColor = 'slategrey'
HeaderBackgroundColor = 'white'
TextColor = 'lightgrey'
ButtonTextColor = 'white'
ButtonBackgroundColor = 'slategrey'

MainTitleStyle = {'font-family': FontStandard,
                    'font-size': 25,
                    'color': TitleColor,
                    'background-color': HeaderBackgroundColor,
                     'margin-top': '5px',
                    #'padding-left': '10px',
                    # 'padding-right':'10px',
                    'height': '20px',
                    'text-align':'center'
                    }
SubTitleStyle = {'font-family': FontStandard,
                    'font-size': 20,
                    'color': TitleColor,
                    'background-color': HeaderBackgroundColor,
                    #'margin-top': '-10px',
                    #'padding-left': '10px',
                    # 'padding-right':'10px',
                    'height': '15px',
                    'text-align':'center'
                    }
HelpTextStyle = {'font-family': FontStandard,
                    'font-size':15,
                    'color': TitleColor,
                    'background-color': HeaderBackgroundColor,
                    #'margin-top': '-10px',
                    'padding-left': '10px',
                    'padding-right':'10px',
                    'height': '15px',
                    'text-align':'left'
                    }

DropdownHeaderStyle = {'font-family': FontStandard,
                       'font-size': 15,
                       'text-color': HeaderColor,
                       'width': '150px',
                       'padding-left': '10px'
                       }

ButtonStyle = {'color': ButtonTextColor,
               'font-family': FontStandard,
               'font-size': 15,
               'background-color': ButtonBackgroundColor,
               'height': '40px',
               'width': '180px',
               'border': 'None',
               'border-radius': '5px'}

PercentInputStyle = {'width': '40px',
                     'height': '15px',
                     'border': '2px LightGrey solid',
                     'border-radius': '5px',
                     'font-family': FontStandard,
                     'text-color': TextColor}

PercentHeaderStyle = {'font-family': FontStandard,
                      'font-size': 15,
                      'text-color': HeaderColor,
                      'width': '80px',
                      'padding-left': '10px'
                      }

SliderTooltipStyle = {'placement': 'bottom',
                      'always_visible': True}

SliderRowStyle = {'display': 'flex',
                  'flex-direction': 'row',
                  'height': '45px'}

SliderWidth = {'width': '250px'}

BlockHeaderStyle = {'font-family': FontStandard,
                    'font-size': 17,
                    'color': TitleColor,
                    'background-color': HeaderBackgroundColor,
                    'margin-top': '-10px',
                    'padding-left': '10px',
                    # 'padding-right':'10px',
                    'height': '30px'
                    }

BlockSpacing = {'height': '20px'}

CountryBlockHeaderStyle = BlockHeaderStyle.copy()
CountryBlockHeaderStyle['margin-left'] = str(CountryMaxWidth * 8 / 2 - 80) + 'px'
CountryBlockHeaderStyle['width'] = '150px'

HelpBlockHeaderStyle = BlockHeaderStyle.copy()
HelpBlockHeaderStyle['margin-left'] = str(CountryMaxWidth * 8 / 2 - 50) + 'px'
HelpBlockHeaderStyle['width'] = '50px'

EnergyMixBlockHeaderStyle = BlockHeaderStyle.copy()
EnergyMixBlockHeaderStyle['margin-left'] = str(CountryMaxWidth * 8 / 2 - 100) + 'px'
EnergyMixBlockHeaderStyle['width'] = '175px'

PredictionBlockHeaderStyle = BlockHeaderStyle.copy()
PredictionBlockHeaderStyle['margin-left'] = str(CountryMaxWidth * 8 / 2 - 65) + 'px'
PredictionBlockHeaderStyle['width'] = '120px'

DiagnosticBlockHeaderStyle = BlockHeaderStyle.copy()
DiagnosticBlockHeaderStyle['margin-left'] = str(CountryMaxWidth * 8 / 2 - 70) + 'px'
DiagnosticBlockHeaderStyle['width'] = '150px'

BorderStyle = '2px LightGrey solid'
BorderRadius = '10px'
BorderWidth = str(CountryMaxWidth * 7+10) + 'px'
# --------------------------------------------------------------

# initalize Dash

app = dash.Dash(__name__)


app.title = "Team 102 C02 Emission Predictions"

app.layout = html.Div([
                html.Div([
                         html.Img(src=pil_img,style={'textAlign':'center','height':'120px','width':'120px'}),
                         html.Div([
                                    html.H1('CO2 Emission Predictions',style=MainTitleStyle),
                                    html.H2('CSE6252 Course Project',style=SubTitleStyle),
                                    html.H2('by Team 102',style=SubTitleStyle),
                                    ],
                                    style={'padding-left':'20px'}
                                    )
                         ],
                          style={'display': 'flex',
                                 'flex-direction': 'row',
                                 'height': '150px',
                                 'margin-left':'500px',
                                 'margin-top':'0px'
                                 }
                          ),

               html.Div([
                          html.Div([
                                    html.Div([html.Div(['Country Selection'], style=CountryBlockHeaderStyle),

                                             html.Div([
                                                       dcc.Dropdown(id='CountryFilter',
                                                                    options=[{'label': country, 'value': country}
                                                                            for country in np.sort(data.Country.unique())
                                                                            ],
                                                                    style={'font-family': FontStandard,
                                                                           'text-color': TextColor,
                                                                           'font-size': 15,
                                                                           'padding-left': 10},
                                                                    value=DefaultCountry,
                                                                    clearable=False,
                                                                    maxHeight=100,
                                                                    searchable=True,
                                                                    ),
                                                       ],
                                                        style={'width': str(CountryMaxWidth * 7) + 'px',
                                                               'height':'50px'}
                                                       ),
                                             ],
                                             style={'width': BorderWidth,
                                                    'height': '80px',
                                                    'border': BorderStyle,
                                                    'border-radius': BorderRadius}
                                             ),
                                    html.Div([''], style=BlockSpacing),
                                    html.Div([html.Div(['Help'], style=HelpBlockHeaderStyle),

                                             html.Div([
                                                       daq.ToggleSwitch(id='HelpToggleSwitch',
                                                                        size = 30,
                                                                        #value=True,
                                                                        label='Show Help',
                                                                        labelPosition='top',
                                                                        style={'font-family': FontStandard,
                                                                              'text-color': TextColor,
                                                                              'font-size': 15},
                                                                     ),
                                                       ],
                                                        style={'width': str(CountryMaxWidth * 7) + 'px',
                                                               'height':'50px'}
                                                       ),
                                             html.P([
                                                      'Goal : Select an energy mix to reduce the CO@ emissions from you country',html.Br(),html.Br(),
                                                      '1. Select your country',html.Br(),
                                                      '2. Adjust the energy mix to reduce CO2 emission',html.Br(),
                                                      '3. When your energy mix reaches 100%, click on "Generate CO2 Predictions',html.Br(),
                                                      '4. Continue to adjust the engergy mix to optimize the CO2 emissions',html.Br(),
                                                       ],
                                                      hidden = True,
                                                      style = HelpTextStyle,
                                                      id = 'HelpText'
                                                      )
                                             ],
                                             id='HelpCollection'
                                             ),
                                    html.Div([''], style=BlockSpacing),
                                    html.Div([
                                                html.Div(['CO2 Prediction'], style=PredictionBlockHeaderStyle),

                                                html.Div([
                                                          html.Div(id='TotalMix'),
                                                         ],
                                                          #style={'padding-left': '15px',
                                                          #       'height': '40px'}
                                                                 ),
                                                html.Div([
                                                    html.Div([
                                                                html.Div(["Years to predict"], style=PercentHeaderStyle),
                                                                html.Div([dcc.Slider(min=0,
                                                                                   max=30,
                                                                                   step=1,
                                                                                   marks={0: {'label': '0'},
                                                                                          30: {'label': '30'},
                                                                                          },
                                                                                   value=DefaultPrediction,
                                                                                   tooltip=SliderTooltipStyle,
                                                                                   id='PredictionSlider')
                                                                        ],
                                                                        style=SliderWidth
                                                                         ),
                                                                      dcc.Input(id='PredictionInput',
                                                                                style=PercentInputStyle,
                                                                                type='number',
                                                                                min=0,
                                                                                max=30,
                                                                                debounce=False,
                                                                                value=int(DefaultPrediction))
                                                                  ],
                                                                      style=SliderRowStyle
                                                                  ),

                                                             ]),
                                              html.Div([html.Button('Generate CO2 Prediction',
                                                                    id='PredictionClick',
                                                                    style=ButtonStyle,
                                                                    n_clicks=0)
                                                        ],
                                                       style={#'align': 'center',
                                                              'height': '50px',
                                                              'margin-left': str(CountryMaxWidth * 8 / 2 - 100) + 'px',
                                                              }
                                                       ),

                                              ],
                                             style={'width': BorderWidth,
                                                    'height': '150px',
                                                    'border': BorderStyle,
                                                    'border-radius': BorderRadius},
                                             id='PredictionCollection',
                                             hidden=True

                                             ),
                                    html.Div([''], style=BlockSpacing),
                                    html.Div([
                                                html.Div(['Energy Mix Selection'],style = EnergyMixBlockHeaderStyle),

                                                html.Div([
                                                          html.Div(["Coal"], style=PercentHeaderStyle),
                                                          html.Div([dcc.Slider(min=0,
                                                                               max=100,
                                                                               step=1,
                                                                               marks={0: {'label': '0'},
                                                                                      100: {'label': '100'},
                                                                                      },
                                                                               value=CoalDefault,
                                                                               tooltip=SliderTooltipStyle,
                                                                               id='CoalSlider')
                                                                   ],
                                                                   style=SliderWidth
                                                                   ),
                                                          dcc.Input(id='CoalInput',
                                                                    style=PercentInputStyle,
                                                                    type='number',
                                                                    min=0,
                                                                    max=100,
                                                                    debounce=False,
                                                                    value=int(CoalDefault))
                                                          ],
                                                          style=SliderRowStyle
                                                          ),

                                                html.Div([html.Div(['Oil'], style=PercentHeaderStyle),
                                                          html.Div([dcc.Slider(min=0,
                                                                               max=100,
                                                                               step=1,
                                                                               marks={0: {'label': '0'},
                                                                                      100: {'label': '100'},
                                                                                      },
                                                                               value=OilDefault,
                                                                               tooltip=SliderTooltipStyle,
                                                                               id='OilSlider')],
                                                                   style=SliderWidth
                                                                   ),  # {'width':'250px'}),
                                                          dcc.Input(id='OilInput',
                                                                    style=PercentInputStyle,
                                                                    type='number',
                                                                    min=0,
                                                                    max=100,
                                                                    debounce=False,
                                                                    value=int(OilDefault))
                                                          ],
                                                         style=SliderRowStyle
                                                         ),
                                                html.Div([html.Div(['Gas'], style=PercentHeaderStyle),
                                                          html.Div([dcc.Slider(min=0,
                                                                               max=100,
                                                                               step=1,
                                                                               marks={0: {'label': '0'},
                                                                                      100: {'label': '100'},
                                                                                      },
                                                                               value=GasDefault,
                                                                               tooltip=SliderTooltipStyle,
                                                                               id='GasSlider')],
                                                                   style={'width': '250px'}),
                                                          dcc.Input(id='GasInput',
                                                                    style=PercentInputStyle,
                                                                    type='number',
                                                                    min=0,
                                                                    max=100,
                                                                    debounce=False,
                                                                    value=int(GasDefault))
                                                          ],
                                                         style=SliderRowStyle
                                                         ),
                                                html.Div([html.Div(['Solar'], style=PercentHeaderStyle),
                                                          html.Div([dcc.Slider(min=0,
                                                                               max=100,
                                                                               step=1,
                                                                               marks={0: {'label': '0'},
                                                                                      100: {'label': '100'},
                                                                                      },
                                                                               value=SolarDefault,
                                                                               tooltip=SliderTooltipStyle,
                                                                               id='SolarSlider')],
                                                                   style=SliderWidth
                                                                   ),
                                                          dcc.Input(id='SolarInput',
                                                                    style=PercentInputStyle,
                                                                    type='number',
                                                                    min=0,
                                                                    max=100,
                                                                    debounce=False,
                                                                    value=int(SolarDefault))
                                                          ],
                                                         style=SliderRowStyle
                                                         # {'display':'flex','flex-direction':'row','height':'45px'}
                                                         ),
                                                html.Div([html.Div(['Wind'], style=PercentHeaderStyle),
                                                          html.Div([dcc.Slider(min=0,
                                                                               max=100,
                                                                               step=1,
                                                                               marks={0: {'label': '0'},
                                                                                      100: {'label': '100'},
                                                                                      },
                                                                               value=WindDefault,
                                                                               tooltip=SliderTooltipStyle,
                                                                               # {'placement': 'bottom','always_visible': True,},
                                                                               id='WindSlider')],
                                                                   style=SliderWidth
                                                                   ),
                                                          dcc.Input(id='WindInput',
                                                                    style=PercentInputStyle,
                                                                    type='number',
                                                                    min=0,
                                                                    max=100,
                                                                    debounce=False,
                                                                    value=int(WindDefault))
                                                          ],
                                                         style=SliderRowStyle
                                                         ),
                                                html.Div([html.Div(['Hydro'], style=PercentHeaderStyle),
                                                          html.Div([dcc.Slider(min=0,
                                                                               max=100,
                                                                               step=1,
                                                                               marks={0: {'label': '0'},
                                                                                      100: {'label': '100'},
                                                                                      },
                                                                               value=HydroDefault,
                                                                               tooltip=SliderTooltipStyle,
                                                                               id='HydroSlider')],
                                                                   style=SliderWidth
                                                                   ),
                                                          dcc.Input(id='HydroInput',
                                                                    style=PercentInputStyle,
                                                                    type='number',
                                                                    min=0,
                                                                    max=100,
                                                                    debounce=False,
                                                                    value=int(HydroDefault))
                                                          ],
                                                         style=SliderRowStyle
                                                         ),
                                                html.Div([html.Div(['Nuclear'], style=PercentHeaderStyle),
                                                          html.Div([dcc.Slider(min=0,
                                                                               max=100,
                                                                               step=1,
                                                                               marks={0: {'label': '0'},
                                                                                      100: {'label': '100'},
                                                                                      },
                                                                               value=NuclearDefault,
                                                                               tooltip=SliderTooltipStyle,
                                                                               id='NuclearSlider')],
                                                                   style=SliderWidth
                                                                   ),

                                                          dcc.Input(id='NuclearInput',
                                                                    style=PercentInputStyle,
                                                                    type='number',
                                                                    min=0,
                                                                    max=100,
                                                                    debounce=False,
                                                                    value=int(NuclearDefault))
                                                          ],
                                                         style=SliderRowStyle
                                                         ),
                                                html.Div([html.Div(['Biofuel'], style=PercentHeaderStyle),
                                                          html.Div([dcc.Slider(min=0,
                                                                               max=100,
                                                                               step=1,
                                                                               marks={0: {'label': '0'},
                                                                                      100: {'label': '100'},
                                                                                      },
                                                                               value=BiofuelDefault,
                                                                               tooltip=SliderTooltipStyle,
                                                                               id='BiofuelSlider')],
                                                                   style=SliderWidth
                                                                   ),
                                                          dcc.Input(id='BiofuelInput',
                                                                    style=PercentInputStyle,
                                                                    type='number',
                                                                    min=0,
                                                                    max=100,
                                                                    debounce=False,
                                                                    value=int(BiofuelDefault))
                                                          ],
                                                         style=SliderRowStyle
                                                         ),

                                                html.Div([html.Div(['Other Renewables'], style=PercentHeaderStyle),
                                                          html.Div([dcc.Slider(min=0,
                                                                               max=100,
                                                                               step=1,
                                                                               marks={0: {'label': '0'},
                                                                                      100: {'label': '100'},
                                                                                      },
                                                                               value=OtherRenewDefault,
                                                                               tooltip=SliderTooltipStyle,
                                                                               id='OtherRenewSlider')],
                                                                   style=SliderWidth
                                                                   ),

                                                          dcc.Input(id='OtherRenewInput',
                                                                    style=PercentInputStyle,
                                                                    type='number',
                                                                    min=0,
                                                                    max=100,
                                                                    debounce=False,
                                                                    value=int(OtherRenewDefault))
                                                          ],
                                                         style=SliderRowStyle
                                                         ),
                                                html.Div([
                                                          html.Div([html.Button('Reset All to 0',
                                                                                id='ResetZeroClick',
                                                                                style=ButtonStyle,
                                                                                n_clicks=0)
                                                                    ],
                                                                   style={'padding-left': '10px'}
                                                                   ),
                                                          html.Div([
                                                                    html.Button('Select Random Values',
                                                                                  id='ResetRandomClick',
                                                                                  style=ButtonStyle,
                                                                                  n_clicks=0)
                                                                    ],
                                                                    style={'padding-left': '20px'},
                                                                    ),

                                                          ],
                                                          style={'display': 'flex', 'flex-direction': 'row', 'height': '50px'}
                                                          ),
                                                 html.Div([
                                                           # html.Div(["Year"], style=DropdownHeaderStyle),
                                                            html.Div([html.Button('Reset to Year',
                                                                        id='ResetYearClick',
                                                                        style=ButtonStyle,
                                                                        n_clicks=0)
                                                                      ],
                                                                      style={'padding-left': '10px'}
                                                                      ),
                                                            dcc.Dropdown(id="YearFilter",
                                                               options=[{"label": year, "value": year}
                                                                        for year in np.sort(data.loc[data['Country'] == DefaultCountry, 'Year'].unique().astype('int'))[::-1]
                                                                        ],
                                                               style={#'height':'5px',
                                                                      'width': '100px',
                                                                      'font-family': FontStandard,
                                                                      'text-color': TextColor,
                                                                      'font-size': 15,
                                                                      'padding-left': '20px'
                                                                      },
                                                               value=DefaultYear,
                                                               clearable=False,
                                                               searchable=True,
                                                               maxHeight=100,
                                                               ),

                                                            ],
                                                             style={'display': 'flex', 'flex-direction': 'row', 'height': '50px'}
                                                            ),

                                                ],
                                                style={'width': BorderWidth,
                                                       'height': '525px',
                                                       'border': BorderStyle,
                                                       'border-radius': BorderRadius},
                                                id='EnergyMixCollection',
                                                hidden=True

                                                ),
                         ]
                        ),
                       html.Div([
                                html.Div([
                                         dcc.Graph(id="energy_mix_graph"),
                                         ],
                                         style={'border': BorderStyle,
                                                'border-radius': BorderRadius,
                                                'overflow': 'hidden',
                                                'height':'450px'}
                                        ),
                                html.Div([
                                          dcc.Graph(id="co2_graph")
                                         ],
                                        style={'border': BorderStyle,
                                               'border-radius': BorderRadius,
                                               'overflow': 'hidden',
                                               'height':'450px'}
                                        ),
                                ],
                                style={'padding-left':'10px',
                                       'width':'1000px',

                                       }
                                ),

                        ],
                         style={
                                'display':'flex',
                                'flex-direction':'row'}
                        ),
        ])

@app.callback(
    Output('TotalMix', 'children'),
    Output('TotalMix', 'style'),
    Output('CoalInput', 'value'),
    Output('OilInput', 'value'),
    Output('GasInput', 'value'),
    Output('SolarInput', 'value'),
    Output('WindInput', 'value'),
    Output('HydroInput', 'value'),
    Output('NuclearInput', 'value'),
    Output('BiofuelInput', 'value'),
    Output('OtherRenewInput', 'value'),
    Output('PredictionInput', 'value'),
    Input('CoalSlider', 'value'),
    Input('OilSlider', 'value'),
    Input('GasSlider', 'value'),
    Input('SolarSlider', 'value'),
    Input('WindSlider', 'value'),
    Input('HydroSlider', 'value'),
    Input('NuclearSlider', 'value'),
    Input('BiofuelSlider', 'value'),
    Input('OtherRenewSlider', 'value'),
    Input('PredictionSlider', 'value'),
    Input('CountryFilter','value'))
def update_EnergyMixTotal(CoalPercent,
                          OilPercent,
                          GasPercent,
                          SolarPercent,
                          WindPercent,
                          HydroPercent,
                          NuclearPercent,
                          BiofuelPercent,
                          OtherRenewPercent,
                          Prediction,
                          CountryValue):
    SumPercent = SumTotal(CoalPercent, OilPercent, GasPercent, SolarPercent, WindPercent, HydroPercent, NuclearPercent,
                          BiofuelPercent, OtherRenewPercent)

    if CountryValue == 'Global':
        Style = {'color': 'red',
                 'fontSize': 25,
                 'fontWeight': 'bold',
                'padding-left': '120px',
                'height': '40px'}

        msg = 'Select a Country'
    elif (SumPercent == 100):
        Style = {'color': 'green',
                 'fontSize': 25,
                 'fontWeight': 'bold',
                 'padding-left': '15px',
                 'height': '40px'}

        msg = str(SumPercent) + '% : Ready to Predict ' + str(Prediction) + ' years'
    elif (SumPercent < 100):
        Style = {'color': 'red',
                 'fontSize': 25,
                 'fontWeight': 'bold',
                'padding-left': '15px',
                'height': '40px'}

        msg = str(SumPercent) + '% : Total must be 100%!'
    elif (SumPercent > 100):
        Style = {'color': 'red',
                 'fontSize': 25,
                 'fontWeight': 'bold',
                'padding-left': '15px',
                'height': '40px'}
        msg = str(SumPercent) + '% : Total must be 100%!'

    return msg, Style, CoalPercent, OilPercent, GasPercent, SolarPercent, WindPercent, HydroPercent, NuclearPercent,\
           BiofuelPercent, OtherRenewPercent, Prediction


@app.callback(
   #Output('ActionText', 'children'),
    Output('CoalSlider', 'value'),
    Output('OilSlider', 'value'),
    Output('GasSlider', 'value'),
    Output('SolarSlider', 'value'),
    Output('WindSlider', 'value'),
    Output('HydroSlider', 'value'),
    Output('NuclearSlider', 'value'),
    Output('BiofuelSlider', 'value'),
    Output('OtherRenewSlider', 'value'),
    Output('PredictionSlider', 'value'),
    Output("co2_graph", "figure"),
    Output('EnergyMixCollection', 'hidden'),
    Output('PredictionCollection', 'hidden'),
    Input('ResetZeroClick', 'n_clicks'),
    Input('ResetRandomClick', 'n_clicks'),
    Input('ResetYearClick', 'n_clicks'),
    Input('PredictionClick', 'n_clicks'),
    Input('CountryFilter', 'value'),
    Input('YearFilter', 'value'),
    Input('CoalInput', 'value'),
    Input('OilInput', 'value'),
    Input('GasInput', 'value'),
    Input('SolarInput', 'value'),
    Input('WindInput', 'value'),
    Input('HydroInput', 'value'),
    Input('NuclearInput', 'value'),
    Input('BiofuelInput', 'value'),
    Input('OtherRenewInput', 'value'),
    Input('PredictionInput', 'value'),
    Input('co2_graph', 'figure'))
def MainControl(button1,
                 button2,
                 button3,
                 button4,
                 CountryValue,
                 YearValue,
                 CoalInput,
                 OilInput,
                 GasInput,
                 SolarInput,
                 WindInput,
                 HydroInput,
                 NuclearInput,
                 BiofuelInput,
                 OtherRenewInput,
                 PredictionInput,
                 CO2GraphInput):

    print('Entered function:',CountryValue,YearValue)
    # ActionMsg='Hi there'

    # -----------------------------------------------
    # set up variables
    #------------------------------------------------

    # Set Output EM values to Inout EM values
    CoalValue = np.round(CoalInput, 0)
    OilValue = np.round(OilInput, 0)
    GasValue = np.round(GasInput, 0)
    SolarValue = np.round(SolarInput, 0)
    WindValue = np.round(WindInput, 0)
    HydroValue = np.round(HydroInput, 0)
    NuclearValue = np.round(NuclearInput, 0)
    BiofuelValue = np.round(BiofuelInput, 0)
    OtherRenewValue = np.round(OtherRenewInput, 0)

    NewPrediction = {}

    #Previous graph is passed back and so previous graph will be redisplayed if EM values are changed

    CO2Fig = CO2GraphInput
    ActionMsg = 'Welcome to the Matrix'
    # -----------------------------------------------



    if CountryValue == 'Global':
        # On loading the app, the default country is global
        GlobalHide=True
        ActionMsg = 'Plotting Global Data'
        print('Ploting CO2 Global')
        CO2Fig = px.line(data_loader.get_global_co2(CountryValue), x='Year', y='CO2EQ',
                      title=CountryValue + " CO2 Emission")
        CO2Fig.update_layout(template='ggplot2')
        if ('PredictionClick' == ctx.triggered_id):
            ActionMsg = 'Select a country BEFORE making a prediction!'
    else:
        GlobalHide = False
        if 'ResetZeroClick' == ctx.triggered_id:
            CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue = SetZero()
            ActionMsg = 'All values reset to 0'

        elif 'ResetRandomClick' == ctx.triggered_id:
            CoalValue1 = np.random.randint(0, 100)
            OilValue1 = np.random.randint(0, 100)
            GasValue1 = np.random.randint(0, 100)
            SolarValue1 = np.random.randint(0, 100)
            WindValue1 = np.random.randint(0, 100)
            HydroValue1 = np.random.randint(0, 100)
            NuclearValue1 = np.random.randint(0, 100)
            BiofuelValue1 = np.random.randint(0, 100)
            OtherRenewValue1 = np.random.randint(0, 100)

            Total = SumTotal(CoalValue1,
                             OilValue1,
                             GasValue1,
                             SolarValue1,
                             WindValue1,
                             HydroValue1,
                             NuclearValue1,
                             BiofuelValue1,
                             OtherRenewValue1)

            if (Total == 0):  # No data exists so set all to 0
                CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue = SetZero()
                print("inside random, but set to 0")

            else:  # Data exists  - Normalize percentages
                CoalValue = np.round((CoalValue1 / Total) * 100, 0)
                OilValue = np.round((OilValue1 / Total) * 100, 0)
                GasValue = np.round((GasValue1 / Total) * 100, 0)
                SolarValue = np.round((SolarValue1 / Total) * 100, 0)
                WindValue = np.round((WindValue1 / Total) * 100, 0)
                HydroValue = np.round((HydroValue1 / Total) * 100, 0)
                NuclearValue = np.round((NuclearValue1 / Total) * 100, 0)
                BiofuelValue = np.round((BiofuelValue1 / Total) * 100, 0)
                OtherRenewValue = np.round((OtherRenewValue1 / Total) * 100, 0)

                CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue = CorrectSum( CoalValue,
                                                                                                                                        OilValue,
                                                                                                                                        GasValue,
                                                                                                                                        SolarValue,
                                                                                                                                        WindValue,
                                                                                                                                        HydroValue,
                                                                                                                                        NuclearValue,
                                                                                                                                        BiofuelValue,
                                                                                                                                        OtherRenewValue)

            print("inside random")
            ActionMsg = 'All reset to random values'

        elif ('CountryFilter' == ctx.triggered_id): #('ResetCountryClick' == ctx.triggered_id):
            if (CountryValue in data.Country.unique()):
                CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue = SetEnergyMix(
                    CountryValue, DefaultYear) #data[data['Country'==CountryValue]].Year.max())

                CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue = CorrectSum(CoalValue,
                                                                                                                                           OilValue,
                                                                                                                                           GasValue,
                                                                                                                                           SolarValue,
                                                                                                                                           WindValue,
                                                                                                                                           HydroValue,
                                                                                                                                           NuclearValue,
                                                                                                                                           BiofuelValue,
                                                                                                                                           OtherRenewValue)

                ActionMsg = f'Values reset to {CountryValue} in {DefaultYear}'
                print('Ploting CO2 without predictions (country reset)')
                CO2Fig = px.line(data_loader.get_global_co2(CountryValue), x='Year', y='CO2EQ',
                                    title=CountryValue + " CO2 Emission")
                CO2Fig.update_layout(template='plotly')
                #fig=PlotCO2_NoPredictions(CountryValue)
            else:  # No data exists so set all to 0
                 CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue = SetZero()
                 ActionMsg = 'Please select another Country'
        elif ('ResetYearClick' == ctx.triggered_id):
            if (CountryValue in data.Country.unique() and YearValue in data.Year.unique()):
                CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue = SetEnergyMix(
                    CountryValue, YearValue)

                CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue = CorrectSum( CoalValue,
                                                                                                                                            OilValue,
                                                                                                                                            GasValue,
                                                                                                                                            SolarValue,
                                                                                                                                            WindValue,
                                                                                                                                            HydroValue,
                                                                                                                                            NuclearValue,
                                                                                                                                            BiofuelValue,
                                                                                                                                            OtherRenewValue)

                print('Inside reset year')
                ActionMsg = f'Values reset to {CountryValue} in {YearValue}'

            else:  # No data exists so set all to 0
                CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue = SetZero()
                ActionMsg = 'Please select a Country and Year'
        elif ('PredictionClick' == ctx.triggered_id) and CountryValue != 'Global':
            Last_Year = LastYear(CountryValue)
            ActionMsg = f"Making Prediction"
            print('making prediction',CountryValue,YearValue,PredictionInput)
            print('EM:',CoalInput/100,OilInput/100,GasInput/100,SolarInput/100,WindInput/100,HydroInput/100,NuclearInput/100,BiofuelInput/100,OtherRenewInput/100)
            print('Sum EM:', CoalInput / 100 + OilInput / 100+ GasInput / 100+ SolarInput / 100+ WindInput / 100+
                  HydroInput / 100+ NuclearInput / 100+ BiofuelInput / 100+ OtherRenewInput / 100)
            NewPredictionDF = data_loader.get_co2_prediction(Last_Year+PredictionInput,
                                                     CountryValue,
                                                     coal=CoalInput/100,
                                                     oil=OilInput/100,
                                                     gas=GasInput/100,
                                                     solar=SolarInput/100,
                                                     wind=WindInput/100,
                                                     hydro=HydroInput/100,
                                                     nuclear=NuclearInput/100,
                                                     biofuel=BiofuelInput/100,
                                                     other_renewable_exc_biofuel=OtherRenewInput/100)
            ActionMsg = f"Making Prediction"

            #fig = PlotCO2_WithPredictions(NewPredictionDF,CountryValue)
            NewPrediction = NewPredictionDF.to_dict()
            print("Here is the new one:",NewPrediction)
            #print(fig)
            CO2Fig = px.line(NewPredictionDF, x='Year', y='CO2EQ', title=CountryValue + " CO2 Emission")
            CO2Fig.update_layout(template='plotly_dark')

        # Input box change => change slider values
        elif  ('CoalInput' == ctx.triggered_id):
            CoalValue = np.round(CoalInput, 0) #if CoalInput else 0
            ActionMsg = 'Coal value adjusted'
        elif ('OilInput' == ctx.triggered_id):
            OilValue = np.round(OilInput, 0) #if OilInput else 0
            ActionMsg = 'Oil value adjusted'
        elif ('GasInput' == ctx.triggered_id):
            GasValue = np.round(GasInput, 0) #if GasInput else 0
            ActionMsg = 'Gas value adjusted'
        elif ('SolarInput' == ctx.triggered_id):
            SolarValue = np.round(SolarInput, 0) #if SolarInput else 0
            ActionMsg = 'Solar value adjusted'
        elif ('WindInput' == ctx.triggered_id):
            WindValue = np.round(WindInput, 0) #if WindInput else 0
            ActionMsg = 'Wind value adjusted'
        elif ('HydroInput' == ctx.triggered_id):
            HydroValue = np.round(HydroInput, 0) #if HydroInput else 0
            ActionMsg = 'Hydro value adjusted'
        elif ('NuclearInput' == ctx.triggered_id):
            NuclearValue = np.round(NuclearInput, 0) #if NuclearInput else 0
            ActionMsg = 'Nuclear value adjusted'
        elif ('BiofuelInput' == ctx.triggered_id):
            BiofuelValue = np.round(BiofuelInput, 0) #if BiofuelInput else 0
            ActionMsg = 'Biofuel value adjusted'
        elif ('OtherRenewInput' == ctx.triggered_id):
            OtherRenewValue = np.round(OtherRenewInput, 0) #if OtherRenewInput else 0
            ActionMsg = 'Other Renewables value adjusted'


    print(ActionMsg, CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue, PredictionInput)
    print('Sum EM:',CoalValue+ OilValue + GasValue + SolarValue+ WindValue+ HydroValue+ NuclearValue+ BiofuelValue+ OtherRenewValue)
    return CoalValue, OilValue, GasValue, SolarValue, WindValue, HydroValue, NuclearValue, BiofuelValue, OtherRenewValue, \
           PredictionInput, CO2Fig, GlobalHide, GlobalHide


@app.callback(Output('HelpText','hidden'),
              Output('HelpCollection','style'),
              Input('HelpToggleSwitch', 'value'))
def update_energy_mix_chart(HelpToggle):
    if (HelpToggle):
        HideHelpText = False
        HelpStyle = {'width': BorderWidth,
                 'height': '250px',
                 'border': BorderStyle,
                 'border-radius': BorderRadius}
    else:
        HideHelpText = True
        HelpStyle = {'width': BorderWidth,
                     'height': '80px',
                     'border': BorderStyle,
                     'border-radius': BorderRadius}
    print('Help text: ', HideHelpText, 'HelpToggle: ', HelpToggle)
    return HideHelpText,HelpStyle

@app.callback(
    Output("energy_mix_graph", "figure"),
    Input("CountryFilter", "value"))
def update_energy_mix_chart(country):
    EnergyMixFig = px.area(data_loader.prepare_energy_mix_df(country),
                  x="Year",
                  y=lp.ENERGY_MIX_PCT,
                  title=f"{country} Energy Mix",
                  )
    EnergyMixFig.update_layout(yaxis_title="Energy Production Mix [%]", template='plotly_white')
    return EnergyMixFig

if __name__ == "__main__":
    app.run_server()



