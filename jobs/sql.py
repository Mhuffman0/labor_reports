import pyodbc
import os
import pandas as pd


def execute_select_query_from_file(
    *paramaters, query_file, sqlserver, database, username, password
):
    """

    :param *paramaters:
    :param query_file:
    :param sqlserver:
    :param database:
    :param username:
    :param password:

    """

    # Creates a connection string using environment variables
    connection_string = "Driver={{ODBC Driver 17 for SQL Server}};Server={0};Database={1};UID={2};PWD={3}"
    cnxn = pyodbc.connect(
        connection_string.format(sqlserver, database, username, password)
    )

    # Retrieves sql query from file
    fd = open(query_file, "r")
    sql = fd.read()

    # Executes sql query and returns a copy of the results as a dataframe
    result = pd.read_sql(sql.format(*paramaters), cnxn)
    print(result)
    return result
