import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def drop_table_postgresql(user, password, host, port, database, table_name):
    """
    Drops a table in PostgreSQL database.

    Args:
        user (str): PostgreSQL username
        password (str): PostgreSQL password
        host (str): PostgreSQL host
        port (str): PostgreSQL port
        database (str): Database name
        table_name (str): Name of the table to drop

    Returns:
        bool: True if table was dropped successfully, False otherwise
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)

    try:
        logger.info(f"Attempting to drop table '{table_name}'")

        with engine.connect() as connection:
            # Using text() for SQL injection safety
            connection.execute(text(f'DROP TABLE IF EXISTS {table_name}'))
            connection.commit()

        logger.info(f"Table '{table_name}' dropped successfully")
        return True

    except SQLAlchemyError as e:
        logger.error(f"Error dropping table '{table_name}': {e}")
        return False

    finally:
        engine.dispose()
        logger.info("Database connection closed")

def migrate_data_postgresql(user, password, host, port, database, df, table_name):
    """
    Migrate data from a pandas DataFrame to a PostgreSQL table.

    Returns:
        bool: True if migration is successful, False otherwise.
    """

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)

    try:
        logger.info(f"Starting data migration to PostgreSQL table '{table_name}'.")

        df.to_sql(table_name, engine, if_exists='replace', index=False)

        logger.info(f"Data successfully migrated to table '{table_name}'.")
        return True

    except SQLAlchemyError as e:
        logger.error(f"An error occurred while migrating data to PostgreSQL: {e}")
        return False

    finally:
        engine.dispose()
        logger.info("Database connection closed.")