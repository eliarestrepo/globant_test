from typing import List, Dict
from app.database import insert_csv, insert_row, read_df, to_avro, insert_avro
import json
import os
import sys
from app import app
from flask import request, render_template, send_file, make_response, url_for, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


@app.route("/historical")
def historical() -> str:
    """Inserts into the department, hired_employees and jobs tables the 
    data found in the csv files in the files folder
    Arguments: None
    Returns: List with the names of the tables successfully inserted"""
    path_root = os.getcwd()
    tables_path = {
        "hired_employees":"/app/files/hired_employees.csv",
        "departments":"/app/files/departments.csv",
        "jobs":"/app/files/jobs.csv"
    }
    success_list = []
    failed_list = []
    for table_name, path in tables_path.items():
        try:         
            insert_csv(table_name=table_name, file_path= f'{path_root}{path}')
            success_list.append(table_name)
        except Exception as e:
            failed_list.append({table_name:e.args})
            print(f"The historical insert in the {table_name} table failed {e.args}")
    
    return json.dumps({'success': success_list, 'failed': failed_list })

@app.route("/insert", methods=['GET', 'POST'])
def insert() -> str:
    """Inserts rows into the departments(id, department), 
        hired_employees(id, name, datetime, department_id, job_id), 
        and jobs(id, job) tables
        Arguments: table_name str, row_dict list[dict1, dict1]/dict
        Returns: a string indicating whether it was successful or not"""
    try:
        print(request.args)
        table_name = request.args.get('table_name')
        row_dict = request.args.get('row_dict')
        print('succesful in the params set up')
        insert_row(table_name=table_name, row= json.loads(row_dict))
        result = {'success': f'The values {row_dict} were inserted in the {table_name} table'}
    except Exception as e:
        result = {'failed': f'The values {row_dict} could not be inserted in the {table_name} table: {e}'}
       
    return json.dumps(result)

@app.route("/backup", methods=['GET', 'POST'])
def backup() -> str:
    """This function creates, consults or restores backups
        Arguments: 
            table_name str,
            type str value options :
                get_bakcups, create_backup, restore_backup,
            created: [ required if type is restore_backup] str
                This is the date the backup was created, 
            name_to_save: [required if type is restore_backup]
                Name with which the table will be created in the database, 
                the same initial name can be used
        Returns:
            If type was
            get_backups: returns json with the names of the tables 
                and the dates on which the backups were created
            create_backup: returns the name with which the backup was 
                saved
            restore_backup: returns the name with which the table was 
                restored in the database
        """
    return_dic = {}
    try:
        table_name = request.args.get('table_name')
        type = request.args.get('type')
        match type:
            case "get_backups":
                df = read_df(f"SELECT * FROM backups WHERE table_name ='{table_name}'")
                df["created"] = df["created"].dt.strftime('%Y-%m-%d %H:%M:%S')
                result = df[["table_name","created"]].to_json(orient="records")
            case "create_backup":
                result = to_avro(table_name=table_name)
            case "restore_backup":
                result = insert_avro(table_name = table_name, created = request.args.get('created'), name_to_save = request.args.get('name_to_save'))
        return_dic["success"] = result
            
    except Exception as e:
        return_dic["failed"]=e.args
    return json.dumps(return_dic)
    


   
@app.route("/")
def index():

    # Use os.getenv("key") to get environment variables
    app_name = os.getenv("APP_NAME")

    if app_name:
        return f"Hello from {app_name} running in a Docker container behind Nginx!"

    return "Hello from Flask"




