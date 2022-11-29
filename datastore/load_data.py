import pandas as pd
from datastore import lookup as lp
from models.predictor import *


class LoadAllData:
    def __init__(self):
        self.population_gdp_forecast_df = pd.read_csv("../data/population_gdp_forecast_1960_2050.csv")
        self.all_df = pd.read_csv("../data/AllDataClean.csv")

        # tlehloba3: added the co2 per country data
        self.historical_co2_df = pd.read_csv("../data/co2WorldData.csv")

    def get_all_data(self) -> pd.DataFrame:
        return self.all_df

    def get_global_co2(self, country) -> pd.DataFrame:
        return self.all_df[self.all_df[lp.country] == country][[lp.year, lp.co2eq]]

    def get_all_data_for_country(self, country) -> pd.DataFrame:
        return self.all_df[self.all_df[lp.country] == country]

    def get_all_data_for_country_for_year(self, country, year) -> pd.DataFrame:
        return self.all_df[(self.all_df[lp.country] == country) & (self.all_df[lp.year] == year)]

    def get_all_countries(self):
        return self.all_df[lp.country].unique()

    def get_all_years(self):
        return self.all_df[lp.year].unique()

    def get_all_forecast_years(self):
        return self.population_gdp_forecast_df[lp.year].unique()

    def prepare_energy_mix_df(self, country) -> pd.DataFrame:
        """Return energy mix for the country"""
        return self.all_df.query("Country == @country")[["Year"] + lp.ENERGY_MIX_PCT]

    def get_coutry_co2(self)->pd.DataFrame: #tlehloba3 added the returm method of the co2 data
        return self.historical_co2_df

    def get_all_country_year_co2(self)-> pd.DataFrame:
        return self.all_df[(self.all_df[lp.country]),(self.all_df[lp.year]) , (self.all_df[lp.co2eq])]

    # This methods returns None if the country or year doesn't exist in list
    # returns per capita co2 emission and over all co2 emission
    def get_co2_prediction(self, year, country, biofuel=0.0, coal=0.0, gas=0.0, hydro=0.0, nuclear=0.0, oil=0.0,
                           other_renewable_exc_biofuel=0.0, solar=0.0, wind=0.0):

        if country == "Global":
            return self.all_df[self.all_df[lp.country] == "Global"][[lp.year, lp.co2eq]]

        if country not in self.get_all_countries():
            return None
        if year not in self.get_all_forecast_years():
            return None

        income_group = get_country_income_group(self.all_df, country=country)
        predicted_all_year = []
        if year > 2019:
            for y in range(2019, year):
                prediction = []
                year_to_predict = y+1
                prediction.append(year_to_predict)
                population = forecast_population(self.population_gdp_forecast_df, year=year_to_predict, country=country)
                gdp = forecast_gdp(self.population_gdp_forecast_df, year=year_to_predict, country=country)
                co2_predictors = CO2ModelPredictors(
                    population=population,
                    gdp=gdp,
                    income_group=income_group,
                    biofuel_pct=biofuel,
                    coal_pct=coal,
                    gas_pct=gas,
                    hydro_pct=hydro,
                    nuclear_pct=nuclear,
                    oil_pct=oil,
                    other_renewable_exc_biofuel_pct=other_renewable_exc_biofuel,
                    solar_pct=solar,
                    wind_pct=wind)

                co2 = get_co2_prediction(co2_predictors)
                prediction.append(co2)
                predicted_all_year.append(prediction)
        predicted_df = None
        if len(predicted_all_year) > 0:
            predicted_df = pd.DataFrame(predicted_all_year, columns=[lp.year, lp.co2eq])
        historical_co2 = self.all_df[(self.all_df[lp.country] == country) & (self.all_df[lp.year] <= 2019)][[lp.year, lp.co2eq]]
        return pd.concat([historical_co2, predicted_df])

if __name__ == "__main__":
    a = LoadAllData()
    print(a.prepare_energy_mix_df('Australia').columns)
