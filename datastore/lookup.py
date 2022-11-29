country = "Country"
year = "Year"
isocode = "IsoCode"
biofuel = "Biofuel"
coal = "Coal"
gas = "Gas"
hydro = "Hydro"
nuclear = "Nuclear"
oil = "Oil"
other_renewable = "OtherRenewableExcBiofuel"
solar = "Solar"
wind = "Wind"
region = "Region"
incomegroup = "Incomegroup"
co2_emission_per_capita = "CO2EQEmissionPerCapita"
co2eq = "CO2EQ"
total_energy_production = "TotalEnergyProduction"
biofuel_pct = "Biofuel_%"
coal_pct = "Coal_%"
gas_pct = "Gas_%"
hydro_pct = "Hydro_%"
nuclear_pct = "Nuclear_%"
oil_pct = "Oil_%"
other_renewable_pct = "OtherRenewableExcBiofuel_%"
solar_pct = "Solar_%"
wind_pct = "Wind_%"
population = "Population"
gdp = "GDP"


# Additional Model params 

upper_middle_income = "Incomegroup_Upper middle income"
lower_middle_income = "Incomegroup_Lower middle income"
low_income = "Incomegroup_Low income"
high_income = "Incomegroup_High income"

income_mapping = {
    "Upper middle income" : upper_middle_income,
    "Lower middle income" : lower_middle_income,
    "Low income": low_income,
    "High income": high_income
}

ENERGY_MIX = [biofuel, coal, gas, hydro, nuclear, oil, other_renewable, solar, wind]
ENERGY_MIX_PCT = [biofuel_pct, coal_pct, gas_pct, hydro_pct, nuclear_pct, oil_pct, other_renewable_pct, solar_pct, wind_pct]