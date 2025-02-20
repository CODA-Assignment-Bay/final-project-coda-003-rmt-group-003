import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

import pandas as pd

default_args = {
    'owner': 'group-3',
    'start_date': dt.datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=30),
}


with DAG('Final-Project',
         default_args=default_args,
         schedule_interval='10 * 1 1 *',
         catchup=False
         ) as dag:

    extract_transform_data_energy = BashOperator(task_id='extract_transform_data', bash_command='python /opt/airflow/script/extract-transform.py')

    load_fact = BashOperator(task_id='load_fact', bash_command='python /opt/airflow/script/load_fact.py')

    load_dim_country = BashOperator(task_id='load_dim_country', bash_command='python /opt/airflow/script/load_dim_country.py')

    load_dim_country_economic = BashOperator(task_id='load_dim_country_economic', bash_command='python /opt/airflow/script/load_dim_country_economic.py')

    create_datamart = BashOperator(task_id='create_datamart', bash_command='python /opt/airflow/script/create_datamart.py')

# extract_transform_data_energy >> load_fact
extract_transform_data_energy >> load_fact >> load_dim_country >> load_dim_country_economic >> create_datamart