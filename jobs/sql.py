import pyodbc
import os
import pandas as pd

def execute_select_query_from_file(*paramaters,query_file,sqlserver,database,username,password):
    
    # Creates a connection string using environment variables
    cnxn = pyodbc.connect(
        r'DRIVER={SQL Server};'
        r'SERVER=' + sqlserver + ';'
        r'DATABASE=' + database + ';'
        r'UID=' + username + ';'
        r'PWD=' +  password
    )
    
    # Retrieves sql query from file
    fd = open(query_file, 'r')
    sql = fd.read()

    # Executes sql query and returns a copy of the results as a dataframe
    result = pd.read_sql(sql.format(*paramaters),cnxn)
    print(result)
    return(result)