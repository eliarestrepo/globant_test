# Aplicación web basada en Flask y MySQL, y despliegue con Docker y docker-compose en Digital Ocean

![Portada](images/portada6.png)

<h2>This repository configures 4 endpoints to interact with the learning database where the departments, hired_employees and jobs tables are.</h2>
<p>
The endpoints found are:

Endpoints:
-  /historical
-  /insert 
-  /backup
-  /first_report
-  /second_report
-  /dashboard
</p>

<h3>/historical:</h3>
<p>only inserts data from the csv files into the jobs, hired_employees and departments tables
args: None</p>

<h3>/insert:</h3>
<p>insert row into any of the mentioned tables
args: table_name and row_dict
postman eg: ```http://localhost:8003/insert?table_name=jobs&row_dict=[{"id":0,"job":"test"},{"id":0,"job":"test"}]```</p>

<h3>/backup:</h3>
<p>create, consult and restore backups
args: table_name, type, created, name_to_save
postman eg: 
```http://localhost:8003/backup?table_name=hired_employees&type=create_backup```
```http://localhost:8003/backup?table_name=hired_employees&type=get_backups```
```http://localhost:8003/backup?table_name=hired_employees&type=restore_backup&created=2023-08-22 04:24:52&name_to_save=restore_hired_employees```

<h3>/first_report:</h3>
<p>Sample table of those hired for the year 2021
by department and position, for each quartile
args: None</p>

<h3>/second_report:</h3>
<p>Sample table of those hired for the year 2021
for departments that were above average
args: None</p>

