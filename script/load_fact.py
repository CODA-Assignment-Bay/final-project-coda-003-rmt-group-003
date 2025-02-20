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

q = sql.SQL('''CREATE TABLE IF NOT EXISTS fact_renewable (
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
    renewables FLOAT
)''')

cursor.execute(q)
connection.commit()

# Read the CSV file
df = pd.read_csv('/opt/airflow/staging/df_fact.csv')

# Convert DataFrame to a list of tuples
data_to_insert = df.values.tolist()

# Define the insert query
insert_query = "INSERT INTO fact_renewable (country_name,year,access_electricity,access_clean_fuels,renewable_electricity,financial_flows,renewable_energy_share,electricity_fossil_fuels,electricity_nuclear,electricity_renewables,low_carbon_electricity,primary_energy_consumption,energy_intensity_level,value_co2_emissions,renewables) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# Execute the query
cursor.executemany(insert_query, data_to_insert)

# # Commit the transaction
connection.commit()