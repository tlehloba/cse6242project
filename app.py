from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px


app = Dash(__name__)


app.layout = html.Div(children=[
     html.Div([#-----------FIRST LAYOUT-----------------------------------
    html.H1('TEAM102',style={'textAlign': 'center'}),
    html.H3('CO2 Emision Model'),

    html.Label([
        "Select_Country",
    dcc.Dropdown(
        id='country_dropdown', clearable=False,
            value='Afghanistan', options=[
                {'label': c, 'value': c}
                for c in 
        ['Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda','Argentina','Armenia','Aruba','Australia','Austria','Azerbaijan','Bahamas (the)','Bahrain','Bangladesh','Barbados',\
'Belarus','Belgium','Belize','Benin','Bermuda','Bhutan','Bolivia (Plurinational State of)','Bosnia and Herzegovina','Botswana','Brazil','Brunei Darussalam','Bulgaria','Burkina Faso','Burundi','Cabo Verde','Cambodia',\
'Cameroon','Canada','Central African Republic (the)','Chad','Chile','China','Colombia','Comoros (the)','Congo (the Democratic Republic of the)','Congo (the)','Costa Rica','Croatia','Cuba','Cyprus','Czechia',"Côte d'Ivoire",\
'Denmark','Djibouti','Dominica','Dominican Republic (the)','Ecuador','Egypt','El Salvador','Equatorial Guinea','Eritrea','Estonia','Eswatini','Ethiopia','Fiji','Finland','France','Gabon','Gambia (the)','Georgia','Germany',\
'Ghana','Greece','Greenland','Grenada','Guatemala','Guinea','Guinea-Bissau','Guyana','Haiti','Honduras','Hong Kong','Hungary','Iceland','India','Indonesia','Iran (Islamic Republic of)','Iraq','Ireland','Israel','Italy','Jamaica',\
'Jaan','Jordan','Kazakhstan','Kenya','Kiribati',"Korea (the Democratic People's Republic of)",'Korea (the Republic of)','Kuwait','Kyrgyzstan',"Lao People's Democratic Republic (the)",'Latvia','Lebanon','Lesotho','Liberia','Libya',\
'Liechtenstein','Lithuania','Luxembourg','Macao','Madagascar','Malawi','Malaysia','Maldives','Mali','Malta','Marshall Islands (the)','Mauritania','Mauritius','Mexico','Micronesia (Federated States of)','Moldova (the Republic of)','Monaco',\
'Mongolia','Montenegro','Morocco','Mozambique','Myanmar','Namibia','Nauru','Nepal','Netherlands (the)','New Caledonia','New Zealand','Nicaragua','Niger (the)','Nigeria','North Macedonia','Norway','Oman','Pakistan','Palau','Palestine, State of','Panama',\
'Papua New Guinea','Paraguay','Peru','Philippines (the)','Poland','Portugal','Puerto Rico','Qatar','Romania','Russian Federation (the)','Rwanda','Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines','Samoa','San Marino','Sao Tome and Principe',\
'Saudi Arabia','Senegal','Serbia','Seychelles','Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia','South Africa','South Sudan','Spain','Sri Lanka','Sudan (the)','Suriname','Sweden','Switzerland','Syrian Arab Republic (the)','Tajikistan',\
'Tanzania, the United Republic of','Thailand','Timor-Leste','Togo','Tonga','Trinidad and Tobago','Tunisia','Turkmenistan','Tuvalu','Türkiye','Uganda','Ukraine','United Arab Emirates (the)','United Kingdom of Great Britain and Northern Ireland (the)','United States of America (the)',\
'Uruguay','Uzbekistan','Vanuatu','Venezuela (Bolivarian Republic of)','Viet Nam','Yemen','Zambia','Zimbabwe']], 
    placeholder="Afghanistan",
                style=dict(
                    width='40%',
                    verticalAlign="left",
                    margin = "4px",
                    padding ="4px"
                )),
    dcc.Graph(id="graph"),], style={"height": "60%", "width": "70%", "margin-left":"10px", "margin-top":"19px"})
   
   
    ]),
])

#     html.Div([#-----------SECOND LAYOUT-----------------------------------
#     html.H3('Population growth Model'),

#     html.Label([
#         "###",
#     dcc.Dropdown(
#         id='energy_dropdown2', clearable=False,
#             value='###', options=[
#                 {'label': c, 'value': c}
#                 for c in 
#         ['BiofuelConsumption', 'BiofuelElectricity', 'CoalConsumption','GasConsumption','GasElectricity','HydroConsumption']], 
#     placeholder="###",
#                 style=dict(
#                     width='40%',
#                     verticalAlign="left",
#                     margin = "4px",
#                     padding ="4px"
#                 )),
#     dcc.Graph(id="graph2"),], style={"height": "60%", "width": "70%", "margin-left":"10px", "margin-top":"19px"})
   
   
#     ]),

#     html.Div([#-----------THIRD LAYOUT-----------------------------------
#     html.H3('GDP growth Model'),

#     html.Label([
#         "###",
#     dcc.Dropdown(
#         id='energy_dropdown3', clearable=False,
#             value='###', options=[
#                 {'label': c, 'value': c}
#                 for c in 
#         ['BiofuelConsumption', 'BiofuelElectricity', 'CoalConsumption','GasConsumption','GasElectricity','HydroConsumption']], 
#     placeholder="###",
#                 style=dict(
#                     width='40%',
#                     verticalAlign="left",
#                     margin = "4px",
#                     padding ="4px"
#                 )),
#     dcc.Graph(id="graph3"),], style={"height": "60%", "width": "70%", "margin-left":"10px", "margin-top":"19px"})
   
   
#     ]),
#     html.Div([#-----------FOURTH LAYOUT-----------------------------------
#     html.H3('CO2 Prediction'),

#     html.Label([
#         "###",
#     dcc.Dropdown(
#         id='energy_dropdown4', clearable=False,
#             value='###', options=[
#                 {'label': c, 'value': c}
#                 for c in 
#         ['BiofuelConsumption', 'BiofuelElectricity', 'CoalConsumption','GasConsumption','GasElectricity','HydroConsumption']], 
#     placeholder="###",
#                 style=dict(
#                     width='40%',
#                     verticalAlign="left",
#                     margin = "4px",
#                     padding ="4px"
#                 )),
#     dcc.Graph(id="graph4"),], style={"height": "60%", "width": "70%", "margin-left":"10px", "margin-top":"19px"})
   
   
#     ])
# ])


@app.callback(
    Output("graph", "figure"), 
    Input("country_dropdown", "value"))

def update_line_chart(Select_Energy_Source):
    df = pd.read_csv("co2WorldData.csv")
    fig = px.line(df,  x="Year", y="CO2 Emmisions in Billion metric tons")
    # fig.update_layout(template='plotly_dark')
    return fig




app.run_server(debug=True)