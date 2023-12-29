import time
import polars as pl
from datetime import datetime
from airflow.decorators import task, dag
from airflow.hooks.base import BaseHook
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine

# to postgress i use connection that i created
postgres_dest_conn_name = "output_postgres"

# to sqlite I use relative path to create an engine
sqlite_source_conn_url = "/include/inputs.db"


# below two functions create engines for them
def prepare_target_engine(postgres_dest_conn_name):
    conn = BaseHook.get_connection(postgres_dest_conn_name)
    engine = create_engine(
        f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}")
    url = f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
    return [engine, url]


def prepare_source_engine(sqlite_conn):
    engine = create_engine(f"sqlite://{sqlite_conn}")
    return engine


postgres_dest_engine = prepare_target_engine(postgres_dest_conn_name)[0]
postgres_dest_url = prepare_target_engine(postgres_dest_conn_name)[1]
sqlite_source_engine = prepare_source_engine(sqlite_source_conn_url)

default_args = {
    "owner": "Muhammadjon",
}


@dag(
    description="using polars to transfor data",
    schedule="@daily",
    start_date=days_ago(1),
    default_args=default_args,
    tags=["polars", "postgres", "sqlite", "load"],
)
def load_task_using_pl():
    @task
    def get_tbl_names():
        query = """SELECT name as table_name
                FROM sqlite_schema
                WHERE type ='table' 
                AND name NOT LIKE 'sqlite_%'; """
        df = pl.read_database(query=query, connection=sqlite_source_engine)
        df_dict = df.to_dict(as_series=False)
        return df_dict

    @task
    def load_src_data(tbl_dict: dict):
        all_tbl_name = []
        start_time = time.time()
        for v in tbl_dict["table_name"]:
            all_tbl_name.append(v)
            rows_imported = 0
            sql = f"SELECT * FROM {v}"
            df = pl.read_database(query=sql, connection=sqlite_source_engine)
            #add time of migration with formatting
            df = df.with_columns(SYS_DATE = pl.lit(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))).lazy()
            df.write_database(
                table_name=f"src2_{v}",
                connection=postgres_dest_url,
                if_table_exists="replace",
            )
            rows_imported += len(df)
            print(
                f"Done. {str(round(time.time() - start_time, 2))} total seconds elapsed"
            )
        print("Data imported successful")
        return all_tbl_name

    load_src_data(get_tbl_names())


load_task_using_pl()
