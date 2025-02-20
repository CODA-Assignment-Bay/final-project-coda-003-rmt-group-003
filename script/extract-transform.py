import pandas as pd

# extract dataset
file_path = "/opt/airflow/staging/global-data-on-sustainable-energy (1).csv"
df = pd.read_csv(file_path)

df.columns = df.columns.str.replace(r'\n', '', regex=False)
df.columns

# menyederhanakan penamaan kolom
df.rename(columns={"Entity": "country_name"}, inplace=True)
df.rename(columns={"Year": "year"}, inplace=True)
df.rename(columns={"Access to electricity (% of population)": "access_electricity"}, inplace=True)
df.rename(columns={"Access to clean fuels for cooking": "access_clean_fuels"}, inplace=True)
df.rename(columns={"Renewable-electricity-generating-capacity-per-capita": "renewable_electricity"}, inplace=True)
df.rename(columns={"Financial flows to developing countries (US $)": "financial_flows"}, inplace=True)
df.rename(columns={"Renewable energy share in the total final energy consumption (%)": "renewable_energy_share"}, inplace=True)
df.rename(columns={"Electricity from fossil fuels (TWh)": "electricity_fossil_fuels"}, inplace=True)
df.rename(columns={"Electricity from nuclear (TWh)": "electricity_nuclear"}, inplace=True)
df.rename(columns={"Electricity from renewables (TWh)": "electricity_renewables"}, inplace=True)
df.rename(columns={"Low-carbon electricity (% electricity)": "low_carbon_electricity"}, inplace=True)
df.rename(columns={"Primary energy consumption per capita (kWh/person)": "primary_energy_consumption"}, inplace=True)
df.rename(columns={"Energy intensity level of primary energy (MJ/$2017 PPP GDP)": "energy_intensity_level"}, inplace=True)
df.rename(columns={"Value_co2_emissions_kt_by_country": "value_co2_emissions"}, inplace=True)
df.rename(columns={"Renewables (% equivalent primary energy)": "renewables"}, inplace=True)
df.rename(columns={"Density(P/Km2)": "density"}, inplace=True)
df.rename(columns={"Land Area(Km2)": "land_area"}, inplace=True)
df.rename(columns={"Latitude": "latitude"}, inplace=True)
df.rename(columns={"Longitude": "longitude"}, inplace=True)

# merubah , menjadi . dan tipe data density menjadi float
df['density'] = df['density'].str.replace(',', '.').astype(float)

# Mengisi Missing Values
df[["access_electricity", "access_clean_fuels", "renewable_electricity", "financial_flows", "renewable_energy_share", "electricity_fossil_fuels", 
    "electricity_nuclear", "electricity_renewables", "low_carbon_electricity", "energy_intensity_level", "value_co2_emissions", 
    "renewables", "gdp_growth", "gdp_per_capita", "density", "land_area", "latitude", "longitude"]] = df[["access_electricity", "access_clean_fuels", "renewable_electricity", "financial_flows", 
                                                                                                         "renewable_energy_share", "electricity_fossil_fuels", "electricity_nuclear", "electricity_renewables", 
                                                                                                         "low_carbon_electricity", "energy_intensity_level", "value_co2_emissions", "renewables", "gdp_growth", 
                                                                                                         "gdp_per_capita", "density", "land_area", "latitude", "longitude"]].fillna(0)

# create fact table
df_fact = df[['country_name', 'year', 'access_electricity', 'access_clean_fuels', 'renewable_electricity',
             'financial_flows', 'renewable_energy_share', 'electricity_fossil_fuels', 'electricity_nuclear',
             'electricity_renewables', 'low_carbon_electricity', 'primary_energy_consumption', 'energy_intensity_level',
             'value_co2_emissions', 'renewables']]
# export fact table to csv
df_fact.to_csv('/opt/airflow/staging/df_fact.csv', index=False)

# create dim table country
df_dim1 = df[['country_name', 'density', 'land_area', 'latitude', 'longitude']].drop_duplicates(subset=['country_name'])
# export dim table to csv
df_dim1.to_csv('/opt/airflow/staging/df_country.csv', index=False)

# create dim table country_economic
df_dim2 = df[['country_name', 'year', 'gdp_growth', 'gdp_per_capita']]
# export dim table to csv
df_dim2.to_csv('/opt/airflow/staging/df_country_economic.csv', index=False)
