import pyodbc
import logging
import config

def create_connection():
    try:
        # set up connection and connect to server
        connection = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}}; SERVER={config.server}; DATABASE={config.database};UID={config.username};PWD={config.password}")
        return connection
    except pyodbc.Error as err:
        logging.error("Database Connectivity Failed. %s", err) 
        raise err
    except Exception as ex:
        logging.error("An error occurred while connecting to the database. %s", ex)
        raise ex
