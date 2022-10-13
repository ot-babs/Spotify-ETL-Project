from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from spotify_etl import run_spotify_etl
# from spotify_etl import check_if_valid_data
# from spotify_etl import newdf

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 10, 11),
    'email': ['airflows@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description='Spotify ETL Process',
    schedule_interval=timedelta(hours=5),
)

def just_a_function():
    print('Place holder')

run_etl = PythonOperator(
    task_id = 'whole_spotify_etl',
    python_callable = run_spotify_etl,
    dag=dag,
)

# run_etl2 = PythonOperator(
#     task_id = 'test',
#     python_callable = check_if_valid_data(newdf), 
#     dag=dag,
# )


run_etl 
#>> run_etl2
