from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args={
    'retries':5,
    'retry_delay':timedelta(minutes=5),
    'owner':'lavanya'
}

with DAG(
    dag_id='catchup_backfil_v2',
    default_args=default_args,
    description='first dag',
    start_date=datetime(2024,5,1),
    schedule_interval='@daily',
    catchup=False
    )as dag:
    task1=BashOperator(
        task_id='task1',
        bash_command='echo simple bash operator task'
    )