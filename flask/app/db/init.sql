CREATE DATABASE IF NOT EXISTS learning;

CREATE OR REPLACE TABLE  learning.hired_employees (
  id             INT
  ,name          VARCHAR(130)
  ,datetime      DATETIME
  ,department_id INT
  ,job_id        INT
);

CREATE OR REPLACE TABLE  learning.departments (
  id          INT
  ,department VARCHAR(130)

);

CREATE OR REPLACE TABLE  learning.jobs (
  id   INT
  ,job VARCHAR(130)
);

CREATE OR REPLACE TABLE  learning.backups(
  table_name   VARCHAR(130)
  ,schema_name LONGTEXT
  ,created     DATETIME
  ,file        VARCHAR(130)
);
