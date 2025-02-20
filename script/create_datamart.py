import psycopg2
from psycopg2 import sql
import pandas as pd

# Replace these parameters with your actual database credentials
db_user = "neondb_owner"
db_password = "s9URtWjSK6IT" #Use your own password
db_host = "ep-snowy-art-a17wausj-pooler.ap-southeast-1.aws.neon.tech"  # Usually "localhost" if running locally
db_port = "5432"  # Default is 5432
db_name = "group-003" #db name

connection = psycopg2.connect(
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    dbname=db_name,
    sslmode='require'
)

cursor = connection.cursor()

select_query = '''SELECT
    f.country_name,
    f.year,
    f.access_electricity,
    f.access_clean_fuels,
    f.renewable_electricity,
    f.financial_flows,
    f.renewable_energy_share,
    f.electricity_fossil_fuels,
    f.electricity_nuclear,
    f.electricity_renewables,
    f.low_carbon_electricity,
    f.primary_energy_consumption,
    f.energy_intensity_level,
    f.value_co2_emissions,
    f.renewables,
    e.gdp_growth,
    e.gdp_per_capita,
    c.density,
    c.land_area,
    c.latitude,
    c.longitude,
    CASE
        WHEN e.gdp_per_capita >= 12000 THEN 'Developed Country'
        ELSE 'Developing Country'
    END AS country_classification
FROM fact_renewable f
LEFT JOIN dim_country_economic e
    ON f.country_name = e.country_name
    AND f.year = e.year
LEFT JOIN dim_country c
    ON f.country_name = c.country_name;
'''
df = pd.read_sql_query(select_query, connection)

cursor = connection.cursor()

q = sql.SQL('''CREATE TABLE IF NOT EXISTS datamart_energy (
    country_name VARCHAR,
    year INTEGER,
    access_electricity FLOAT,
    access_clean_fuels FLOAT,
    renewable_electricity FLOAT,
    financial_flows FLOAT,
    renewable_energy_share FLOAT,
    electricity_fossil_fuels FLOAT,
    electricity_nuclear FLOAT,
    electricity_renewables FLOAT,
    low_carbon_electricity FLOAT,
    primary_energy_consumption FLOAT,
    energy_intensity_level FLOAT,
    value_co2_emissions FLOAT,
    renewables FLOAT,
    gdp_growth FLOAT,
    gdp_per_capita FLOAT,
    density FLOAT,
    land_area FLOAT,
    latitude FLOAT,
    longitude FLOAT,
    country_classification VARCHAR
)''')

cursor.execute(q)
connection.commit()

# Convert DataFrame to a list of tuples
data_to_insert = df[['country_name', 'year', 'access_electricity', 'access_clean_fuels', 'renewable_electricity',
                  'financial_flows', 'renewable_energy_share', 'electricity_fossil_fuels', 'electricity_nuclear',
                  'electricity_renewables', 'low_carbon_electricity', 'primary_energy_consumption', 'energy_intensity_level',
                  'value_co2_emissions', 'renewables', 'gdp_growth', 'gdp_per_capita', 'density', 'land_area', 'latitude',
                  'longitude', 'country_classification']].values.tolist()

# Define the insert query
insert_query = "INSERT INTO datamart_energy (country_name, year, access_electricity, access_clean_fuels, renewable_electricity, financial_flows, renewable_energy_share, electricity_fossil_fuels, electricity_nuclear, electricity_renewables, low_carbon_electricity, primary_energy_consumption, energy_intensity_level, value_co2_emissions, renewables, gdp_growth, gdp_per_capita, density, land_area, latitude, longitude, country_classification) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# Execute the query
cursor.executemany(insert_query, data_to_insert)

# # Commit the transaction
connection.commit()