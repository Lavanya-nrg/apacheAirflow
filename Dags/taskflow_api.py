from airflow.decorators import dag,task
from datetime import datetime, timedelta

default_args={
    'owner': 'lavanya',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

@dag(dag_id='taskflow_v2',
     default_args=default_args,
     start_date=datetime(2024,5,6),
     schedule_interval='@daily')

def hello_world_etl():
    
    @task(multiple_outputs=True)
    def get_name():
        return {
            'firstname':'jerry',
            'lastname':'fridman'
        }
    
    @task
    def get_age():
        return 19
    
    @task
    def greet(firstname,lastname,age):
        print(f"hello my name is {firstname}{lastname} "
              f"and age is {age}")
        
    name_dict=get_name()
    age=get_age()
    greet(firstname=name_dict['firstname'],
          lastname=name_dict['lastname'],
          age=age)
    
greet_dag=hello_world_etl()