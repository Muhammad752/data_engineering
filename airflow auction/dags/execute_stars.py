import json

from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime,timedelta # time delta is for repetitive tasks

def _print_stargazers(github_stats:str,date:str):
        github_stats_json=json.loads(github_stats)
        airflow_stars=github_stats_json.get('stargazers_count')

        print(f'As of date {date} Apache airflow has {airflow_stars} stars')
        

with DAG('extract_stars', 
         schedule_interval='@daily', 
         start_date=datetime(2022, 1, 1), 
         catchup=False) as dag:
               
               get_date = BashOperator(
                    task_id="get_date",
                    bash_command="date"
               )

               query_github_results=SimpleHttpOperator(
                    task_id="query_github_results",
                    endpoint='{{var.value.endpoint}}',
                    method='GET',
                    http_conn_id='github_api',
                    log_response=True
               )

               print_stargazers=PythonOperator(
                       task_id='print_stargazers',
                       python_callable=_print_stargazers,
                       op_args=[
                               "{{ti.xcom_pull(task_ids='query_github_results')}}",
                               "{{ti.xcom_pull(task_ids='get_date')}}"
                       ]
               )

               get_date>>query_github_results>>print_stargazers