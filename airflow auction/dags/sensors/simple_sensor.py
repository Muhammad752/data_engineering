from airflow import DAG
from datetime import datetime
from airflow.sensors.python import PythonSensor

def _condition():
    return False

with DAG('simple_sencor',
         description="this is simple example",
         start_date=datetime(2023,12,20),
         schedule='@once',
         catchup=False,
         )as dag:

    waiting_for_codition=PythonSensor(
        task_id='waiting_for_task',
        python_callable=_condition,
        poke_interval=60,
        timeout=60
    )