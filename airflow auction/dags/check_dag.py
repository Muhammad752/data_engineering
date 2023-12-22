from airflow import DAG
from datetime import datetime,timedelta
from airflow.decorators import dag,task
from airflow.operators.bash import BashOperator

@dag(
    description='DAG to check data',
    schedule='@daily',
    tags=['date_engineering_team'],
    catchup=False
)
def check_dag():

    create_file=BashOperator(
        task_id='first_task',
        bash_command='echo "Hi there!" >/tmp/dummy'
    )

    check_file=BashOperator(
        task_id="second_task",
        bash_command="test -f /tmp/dummy",
    )

    @task
    def read_file():
        print(open('/tmp/dummy','rb').read())

    create_file>>check_file>>read_file()

check_dag()