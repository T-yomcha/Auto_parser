from prefect import flow, task
from drom.drom_links import collect_drom_links
from drom.drom_data import parse_drom_data
from drom.drom_transform import transform_drom_data

from load_to_database import migrate_data_postgresql, drop_table_postgresql


@task
def collect_links_task():
    collect_drom_links()


@task
def parse_data_task():
    parse_drom_data()


@task
def transform_data_task():
    return transform_drom_data()


@task
def load_to_db_task(df):
    user = "postgres"
    password = "root"
    host = "localhost"
    port = "5432"
    database = "parser"
    table_name = "drom"

    drop_table_postgresql(user, password, host, port, database, table_name)
    migrate_data_postgresql(user, password, host, port, database, df, table_name)


@flow(name="Drom ETL Flow")
def etl_flow():
    collect_links_task()
    parse_data_task()
    df = transform_data_task()
    load_to_db_task(df)


if __name__ == "__main__":
    etl_flow()
