
# Airflow auction


> This week I familirized myself with the apache airflow tool

> First I went through courses and grasped basic idea and got into way of learnin by doing

### 1. Created a DAG that can be combined to sqlite server, and made several tasks that are based on create, input and update

![alt graph](/airflow%20auction/graphs/execute%20sql%20pipeline.jpg)

-*there is a dependency that first a "create table" tasl is run and only after insert and update tasks run, or if table creation fails the other tasks do not run*



### 2. Then I went through xcom communications and went further with labels and task groups

![alt graph](/airflow%20auction/graphs/execute%20with%20branching.jpg)

-*the purpouse of the DAG(direct acyclic graph) is to filter or group given csv table based on a given condition* 

-*the dag first gets dataset values and cleanes from null values and performs specific tasks by using branching, based on a given variable*

-*tasks interact with each other by using xcom values*

### 3. Created a table scheme for intended application (created in 3NF)

![alt auction table schema](/airflow%20auction/auction%20database%20scheme.png)

-*Now on the process on the optimization*

-*Further I am going to implement and perform operations on it with integration to airflow*


# Week 2

### 1. Went through the courses on linkedin

finished the course “Learning Apache Airflow” by Janani Ravi! Check it out: https://www.linkedin.com/learning/certificates/526bdf263b0d2b5508bac5ef3595bf84f1eac22a138a2f6e665a3a3df4788043?trk=share_certificate #apacheairflow #itautomation.


### 2. Learned about postgresql and integrated db with airflow

Learned about cron operators and passing arguments throughtout tasks and using TaskFlow api



