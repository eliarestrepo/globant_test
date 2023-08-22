CREATE DATABASE learning;
use learning;

CREATE TABLE hired_employees (
  id             INT
  ,name          VARCHAR(130)
  ,datetime      DATETIME
  ,department_id INT
  ,job_id        INT
);

CREATE TABLE departments (
  id          INT
  ,department VARCHAR(130)

);

CREATE TABLE jobs (
  id   INT
  ,job VARCHAR(130)
);

CREATE TABLE backups(
  table_name   VARCHAR(130)
  ,schema_name LONGTEXT
  ,created     DATETIME
  ,file        VARCHAR(130)
);
