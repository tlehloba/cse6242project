from datastore import lookup as lp
import json
import pickle
import numpy as np


class CO2ModelPredictors:
    def __init__(self, population, gdp, income_group, biofuel_pct=0.0,  
    coal_pct=0.0,  gas_pct=0.0,  
    hydro_pct=0.0, nuclear_pct=0.0, 
    oil_pct=0.0,  other_renewable_exc_biofuel_pct=0.0,  
    solar_pct=0.0, wind_pct=0.0):
        self.biofuel_pct = biofuel_pct
        self.coal_pct = coal_pct
        self.gas_pct = gas_pct
        self.hydro_pct = hydro_pct
        self.nuclear_pct = nuclear_pct
        self.oil_pct = oil_pct
        self.other_renewable_exc_biofuel_pct = other_renewable_exc_biofuel_pct
        self.solar_pct = solar_pct
        self.wind_pct = wind_pct
        self.population = population
        self.gdp = gdp
        self.income_group = income_group


def forecast_population(df, year: int, country:str):
    return df[(df[lp.country] == country) & (df[lp.year] == year)][lp.population].values[0]


def forecast_gdp(df, year:int, country: str):
    return df[(df[lp.country] == country) & (df[lp.year] == year)][lp.gdp].values[0]


def get_country_income_group(df, country):
    return df[df[lp.country] == country][lp.incomegroup].unique()[0]

def percentage_error(error_pct):
    pct = 100 - error_pct
    p = lambda x: x / 100
    return p(pct)

def smooth(weights, arr):
   return np.convolve(weights/weights.sum(), arr)

def remove_noise(prediction_value):
    if prediction_value > 0:
        data_convolved = smooth(np.bartlett(1), prediction_value * percentage_error(40))
        return data_convolved[0]
    else:
        print("Predicted negative values")
        return abs(prediction_value)

def get_co2_prediction(co2_model_predictors: CO2ModelPredictors):
    model_coefficient = json.load(open('../data/model_coefficient.json'))
    linear_model = model_coefficient["Linear"]
    return remove_noise(round(linear_model["intercept"] \
                 + linear_model[lp.biofuel_pct] * co2_model_predictors.biofuel_pct \
                 + linear_model[lp.coal_pct] * co2_model_predictors.coal_pct \
                 + linear_model[lp.gas_pct] * co2_model_predictors.gas_pct \
                 + linear_model[lp.hydro_pct] * co2_model_predictors.hydro_pct \
                 + linear_model[lp.nuclear_pct] * co2_model_predictors.nuclear_pct \
                 + linear_model[lp.oil_pct] * co2_model_predictors.oil_pct \
                 + linear_model[lp.other_renewable_pct] * co2_model_predictors.other_renewable_exc_biofuel_pct \
                 + linear_model[lp.solar_pct] * co2_model_predictors.solar_pct \
                 + linear_model[lp.wind_pct] * co2_model_predictors.wind_pct \
                 + linear_model[lp.population] * co2_model_predictors.population * percentage_error(30)\
                 + linear_model[lp.gdp] * co2_model_predictors.gdp * percentage_error(30)\
                 + linear_model[lp.income_mapping[co2_model_predictors.income_group]], 3))
def xgboost_co2_prediction(co2_model_predictors: CO2ModelPredictors):
    loaded_model = pickle.load(open("../data/finalized_model.sav", 'rb'))
    data_for_prediction = [[co2_model_predictors.biofuel_pct,
                           co2_model_predictors.coal_pct,
                           co2_model_predictors.gas_pct,
                           co2_model_predictors.hydro_pct,
                           co2_model_predictors.nuclear_pct,
                           co2_model_predictors.oil_pct,
                           co2_model_predictors.other_renewable_exc_biofuel_pct,
                           co2_model_predictors.solar_pct,
                           co2_model_predictors.wind_pct,
                           co2_model_predictors.population * percentage_error(30),
                           co2_model_predictors.gdp * percentage_error(30)]]
    return remove_noise(loaded_model.predict(data_for_prediction)[0])