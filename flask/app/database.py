from typing import List, Dict
from app.format import COLUMNS,df_columns_format
from pandas import DataFrame
import pandas as pd
import mariadb
from fastavro import writer, reader
import sqlalchemy
from datetime import datetime
import json

def engine_connection():
    """Create a db conection for pandas
        Args: None
        Return: sqlalchemy engine"""
    conn = sqlalchemy.create_engine("mariadb+pymysql://root:root@db:3306/learning")
    return conn

def connection():
    """Create a database conection to query directly over the db
        Args: None
        Return: DB conection"""
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': 3306,
        'database': 'learning',
        'autocommit':True
    }
    connection = mariadb.connect(**config)
    return connection

def insert_csv(table_name:str,file_path:str):
    """Insert data from a csv file into the db
        Args: table_name str, file_path: str
        Return: None """
    conn = engine_connection()
    columns = list(COLUMNS.get(table_name))
    df = pd.read_csv(file_path, names= columns )
    df = df_columns_format(df, table_name = table_name, type = 'to_sql')
    df.to_sql(name = table_name, con = conn,  if_exists= "append", index = False )

def insert_row(table_name:str, row):
    """Insert rows in a specific table
        Args:table_name str, row: list[dic1, dic2...]/dict
        Return: None"""
    conn = connection()
    cur = conn.cursor()
    if type(row) == dict:
        row_list = [row]
    else:
        row_list = row
    
    for row_i in row_list:
        query = f""" INSERT INTO {table_name} VALUES {tuple(row_i.values())}"""
        print(query)
        cur.execute(query)

    cur.close()

def read_df(query:str) -> DataFrame :
    """Creates a dataframe from a query
        Args: query str
        Return: df: pandas DataFrame"""
    conn = engine_connection()
    df =  pd.read_sql(query,conn)
    return df


    



