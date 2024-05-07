from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.bash import BashOperator
default_args={
    'owner':'lavanya',
    'retries':5,
    'retry_delay':timedelta(minutes=2)
}
with DAG(
    dag_id="first_dag_v5",
    default_args=default_args,
    description="first dag",
    start_date=datetime(2024,5,29,2),
    schedule_interval='@daily'
) as dag:
    task1=BashOperator(
        task_id='first_task',
        bash_command="echo hello world"
    )
    task2=BashOperator(
        task_id='second_task',
        bash_command='echo i am 2nd task'
    )
    task3=BashOperator(
        task_id='third_task',
        bash_command="echo task three"
    )
    # task1.set_downstream(task2)
    # task1.set_downstream(task3)
    
    
    
    # task1>>task2
    # task1 >> task3
    task1 >> [task2, task3]