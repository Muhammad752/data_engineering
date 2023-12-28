import time
from airflow.decorators import dag,task
from airflow.utils.dates import days_ago
from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine

default_args={"owner":'Muhammadjon'}

@dag(
    description='dag to import values from one database to another',
    schedule='@daily',
    start_date=days_ago(1),
    default_args=default_args,
    tags=['copy_data','to_postgres'],
    catchup=False
)
def postgres_etl():

    # sqlite_data_retrive=SqliteOperator(
    #     task_id='import_to_postgres', 
    #     sqlite_conn_id='input_sqlite',
    #     sql=r"SELECT * FROM customer")
    
    @task
    def get_src_tables():
        hook=SqliteHook(sqlite_conn_id="input_sqlite")
        sql= """SELECT name as table_name
                FROM sqlite_schema
                WHERE type ='table' 
                AND name NOT LIKE 'sqlite_%'; """
        df=hook.get_pandas_df(sql)
        print(df)
        tbl_dict=df.to_dict('dict')
        return tbl_dict

    @task
    def load_src_data(tbl_dict:dict):
        conn=BaseHook.get_connection('output_postgres')
        engine=create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
        print(f'\n\n\t{conn.schema}\n\n')
        all_tbl_name = []
        start_time = time.time()

        for k, v in tbl_dict['table_name'].items():
            hook=SqliteHook(sqlite_conn_id="input_sqlite")
            all_tbl_name.append(v)
            rows_imported = 0
            sql = f'select * FROM {v}'
            df = hook.get_pandas_df(sql)
            print(df.head())
            # print(f'importing rows {rows_imported} to {rows_imported + len(df)}... for table {v} ')
            result=df.to_sql(f'src_{v}', engine, if_exists='replace', index=False)
            print(f"\n\n\nRestult is in {conn.schema} \n\n\n")
            rows_imported += len(df)
            print(f'Done. {str(round(time.time() - start_time, 2))} total seconds elapsed')
        print("Data imported successful")
        return all_tbl_name
    
    @task
    def print_result():
        hook=PostgresHook('output_postgres')
        sql= """SELECT * FROM src_customer LIMIT 5"""
        df=hook.get_pandas_df(sql)
        print(df)

    
    @task
    def delete_tables(tbl_dict:dict):
        all_tbl_name = []
        start_time = time.time()

        for k, v in tbl_dict['table_name'].items():
            all_tbl_name.append(v)
            sql = f'DROP TABLE IF EXISTS src_{v}'
            hook=PostgresHook('output_postgres')
            hook.run(sql=sql)
            print(f'Done. {str(round(time.time() - start_time, 2))} total seconds elapsed')
        print("Data tables deleted successful")
        return all_tbl_name
    
    tbl_names=get_src_tables()
    delete_tables(tbl_names)>>load_src_data(tbl_names)>>print_result()

postgres_etl()

