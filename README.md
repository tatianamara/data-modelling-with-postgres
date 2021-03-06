# Data Modeling with Postgres

## Table of Contents

- [Data Modeling with Postgres](#data-modeling-with-postgres)
  - [Table of Contents](#table-of-contents)  
  - [Introduction](#introduction)
    - [Objectives](#objectives)  
    - [Star Schema Model](#star-schema-model)  
  - [What this repo contains](#what-this-repo-contains)
    - [Data](#data)
    - [Create_Table.py](#create_tablepy)
    - [ETL.py](#etlpy)
    - [Sql_queries.py](#sql_queriespy)
    - [ETL.ipynb](#etlipynb)
    - [Test.ipynb](#testipynb)
    - [Star_schema_model.png](#star_schema_modelpng)
    - [Requirements.txt](#requirementstxt)
  - [Get Started](#get-started)
    - [Prerequisites](#prerequisites)
    - [Step one: Creating the database and tables](#step-one-creating-the-database-and-tables)
    - [Step two: Processing the Song and Log Datasets](#step-two-processing-the-song-and-log-datasets)
  - [Project Datasets](#project-datasets)
    - [Song Dataset](#song-dataset)
    - [Log Dataset](#log-dataset)

## Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

### Objectives  

- Apply what I've learned on data modeling with Postgres 

- Build an ETL pipeline using Python

- Define fact and dimension tables for a star schema for a particular analytic focus

- Write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL  

### Star Schema Model  
![Star Schema Model](https://github.com/tatianamara/data-modelling-with-postgres/blob/main/star_schema_model.png)

- The fact table `songplays` stores the records in log data associated with song plays i.e. records with page.

- The dimension table `users` stores the users in the app.

- The dimension table `songs` stores the songs in the music database.

- The dimension table `artists` stores the artists the in music database.

- The dimension table `time` stores the timestamps of records in songplays broken down into specific units.

## What this repo contains
```
data/
    log_data
    song_data
create_tables.py
etl.py
sql_queries.py
etl.ipynb
test.ipynb
star_schema_model.png
requirements.txt
```

#### Data
This folder contains the log files and songs that will be processed and transformed into the project's five tables (songplays, songs, artists, users, time)

#### Create_Table.py
This script contains the code to drops and creates your tables. You run this file to reset your tables before each time you run your ETL scripts.

#### ETL.py
This script contains the code to reads and processes files from song_data and log_data and loads them into your tables.

#### Sql_queries.py
This script contains all your sql queries, and is used by `create_tables.py`, `etl.py`, and `etl.ipynb`.

#### ETL.ipynb
Reads and processes a single file from song_data and log_data and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables.

#### Test.ipynb
Displays the first few rows of each table to let you check your database.

#### Star_schema_model.png
The star schema model used to create the tables for this project

#### Requirements.txt 
Contains all the dependencies to the project

## Get Started  

`git clone https://github.com/tatianamara/data-modelling-with-postgres.git`

### Prerequisites

- Python3 installed (you can download [here](https://www.python.org/downloads/))
- Postgresql local connection. Please see detailed instructions in the [PostgreSQL documentation](https://www.postgresql.org/docs/current/runtime.html).
- Install requirements with pip3 install -r requirements.txt.

### Step one: Creating the database and tables

To create the required database and tables, modify the `create_tables.py` code by passing your database attributes
Then execute the script using this command in your terminal

`python3 create_tables.py`

### Step two: Processing the Song and Log Datasets

To processing the datasets and insert the data into the corresponding tables, run the `etl.py` script with the command below on your terminal

`python3 etl.py`

## Project Datasets  

### Song Dataset  

The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

```
song_data/A/B/C/TRABCEI128F424C983.json  
song_data/A/A/B/TRAABJL12903CDCF1A.json
```

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

### Log Dataset  

The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

The log files in the dataset are partitioned by year and month. For example, here are filepaths to two files in this dataset.

```
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json
```
