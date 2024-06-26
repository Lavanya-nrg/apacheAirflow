from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.python import PythonOperator
default_args={
    'owner': 'lavanya',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}
def greet(ti):
    # name=ti.xcom_pull(task_ids='get_name')
    firstname=ti.xcom_pull(task_ids='get_name',key='first_name')
    lastname=ti.xcom_pull(task_ids='get_name',key='last_name')
    age=ti.xcom_pull(task_ids='get_age',key='age')
    print(f"hello my name is {firstname}{lastname}, "
          f"and i am {age} years old")
    
def get_name(ti):
    ti.xcom_push(key='firstname', value='Jerry')
    ti.xcom_push(key='lastname',value='fridman')

def get_age(ti):
    ti.xcom_push(key='age',value='19')
    
with DAG(
    default_args=default_args,
    dag_id='python_operator_first_dag_v6',
    description='first python operator',
    start_date=datetime(2024,5,6),
    schedule_interval='@daily'
) as dag:
    task1=PythonOperator(
        task_id='greet',
        python_callable=greet
        # op_kwargs={'age':2}
    )
    task2=PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )
    task3=PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )
[task2,task3]>>task1