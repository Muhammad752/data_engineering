from airflow.decorators import dag,task
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.sqlite.operators.sqlite import SqliteOperator

default_args={"owner":'Muhammadjon'}

@dag(
    description='dag to import values from one database to another',
    schedule='@daily',
    start_date=days_ago(1),
    default_args=default_args,
    tags=['copy_data','to_postgres']
)
def postgres_etl():

    sqlite_data_retrive=SqliteOperator(
        task_id='import_to_postgres', 
        sqlite_conn_id='input_sqlite',
        sql=r"SELECT * FROM customer")
    
    @task
    def transform(tables:dict):
        print(tables)

postgres_etl()

