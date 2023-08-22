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

def to_avro(table_name:str):
    """Save a table from the db to an avro file
        Arg: table_name str
        Return: name_to_save str: avro file name str """
    df = read_df(f"SELECT * FROM {table_name}")
    df, fields_list = df_columns_format(df, table_name = table_name, type = 'to_avro')
    schema = {
    'doc': 'Avro Schema',
    'name': table_name,
    'namespace': 'test',
    'type': 'record',
    'fields': fields_list
    }
    sufix = datetime.now()
    sufix_file_name = sufix.strftime("%Y_%m_%d_%H%M%S")
    sufix_record = sufix.strftime("%Y-%m-%d %H:%M:%S")
    name_to_save = f'{table_name}_{sufix_file_name}.avro'
    
    with open(f'{name_to_save}', 'wb') as out:
        writer(out, schema, df.to_dict('records'))
    insert_row(table_name = 'backups', row = {"table_name" : table_name, "schema_name ": json.dumps(schema), "created" : sufix_record, "file" : name_to_save})
    return name_to_save

def insert_avro(table_name:str, created:str, name_to_save:str):
    """Save a table to the db from an avro file
        Args: table_name str: name of the table to be restored, 
            created str: date the avro file was made, 
            name_to_save str: name with which to save the table
        Return: name_to_save str"""
    conn = engine_connection()
    avro_log = read_df(f"SELECT * FROM backups where table_name = '{table_name}' and created = '{created}'").to_dict('records')
    backup_name = avro_log[0]["file"]
    schema = json.loads(avro_log[0]["schema_name"])
    with open(f'{backup_name}', 'rb') as fo:
        avro_reader = reader(fo, schema)
        records = [r for r in avro_reader]
        df = pd.DataFrame.from_records(records)
    df = df_columns_format(df, table_name = table_name, type = 'to_sql')
    df.to_sql(name = name_to_save, con = conn,  if_exists= "replace" )
    return name_to_save
    



