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

q = sql.SQL('''CREATE TABLE IF NOT EXISTS dim_country (
    country_name VARCHAR,
    density FLOAT,
    land_area FLOAT,
    latitude FLOAT,
    longitude FLOAT
)''')

cursor.execute(q)
connection.commit()

# Read the CSV file
df = pd.read_csv('/opt/airflow/staging/df_country.csv')

# Convert DataFrame to a list of tuples
data_to_insert = df[['country_name', 'density', 'land_area', 'latitude', 'longitude']].values.tolist()

# Define the insert query
insert_query = "INSERT INTO dim_country (country_name, density, land_area, latitude, longitude) VALUES (%s, %s, %s, %s, %s)"

# Execute the query
cursor.executemany(insert_query, data_to_insert)

# # Commit the transaction
connection.commit()
