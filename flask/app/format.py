import pandas as pd
COLUMNS_TYPES = {
    "hired_employees":{"id":"int","name":"string","datetime":"datetime", "department_id":"int", "job_id":"int"},
    "departments":{"id":"int","department":"string"},
    "jobs":{"id":"int","job":"string"}
}

COLUMNS = {
     "hired_employees":tuple(COLUMNS_TYPES.get("hired_employees").keys()),
    "departments":tuple(COLUMNS_TYPES.get("departments").keys()),
    "jobs":tuple(COLUMNS_TYPES.get("jobs").keys())
}

def df_columns_format(df, table_name, type):
    """Organizes dfs into more appropriate types when saving avro or restoring 
        from an avro
        Args: 
            df: pandas DataFrame, 
            table_name: str [jobs, hired_employees, departments]
            type: str [to_avro, to_sql]
            """
    date_columns = []
    str_columns = []
    int_columns = []
    fields_list = []
    for col_n, data_t in COLUMNS_TYPES[table_name].items():
        match data_t:
            case 'datetime':
                date_columns.append(col_n)
                rename_value = 'string'
            case 'int':
                int_columns.append(col_n)
                rename_value = 'float'
            case 'string':
                str_columns.append(col_n)
                rename_value = 'string'
            case _:
                rename_value = data_t
        fields_list.append({"name":col_n, "type": rename_value})

    match type:
        case 'to_avro':
            for to_convert in date_columns:
                df[to_convert] = df[to_convert].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('')
            for to_convert in int_columns:
                df[to_convert] = df[to_convert].astype('float')
            for to_convert in str_columns:
                df[to_convert] = df[to_convert].fillna('')
        case 'to_sql':
            for to_convert in date_columns:
                df[to_convert]= pd.to_datetime(df[to_convert])
            for to_convert in int_columns:
                df[to_convert] = df[to_convert].astype('Int64')
    result = df if type == 'to_sql' else (df,fields_list)
    return result

