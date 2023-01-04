Custom ETL Pipeline Overview
========

This project is set up to scrape new job postings from Linkedin every hour and store all information about the jobs in a data warehouse. The data is then cleaned and organized into maneagable tables so that they can be later on convineantly queried [for analysis](https://easy-bottles-grin-34-125-254-54.loca.lt). 

![Alt Text](https://github.com/MubassirAhmed/ELT-Data-Pipeline/blob/main/include/Assets/ELT%20Pipeline.gif) 

Technical Description
================

1. Scraping: 
* A webcrawler (designed and written in python using the scrapy library) recursively crawls Linkedin to collect jobs posted from the last hour. It extracts various information from each posting, such as their job title, the job description, etc. and uploads the raw data to an AWS S3 bucket.

2. Staging: 
* The raw data is stored in a S3 bucket to provide a historical snapshot of the source data. This allows for running backfills from the source incase any transformation logic needs to be changed later on. 
* It also allows any data discrepencies down the line to be traced back to the source. This data lineage is useful when debugging the pipeline. 
* Finally, if (and when) Linkedin's front-end changes (or is updated), and say the columns ingested need to be changed, then the source data provides a simple way of handling this schema evolution using date-based if-else logic in the load script.

3. The ETL phase:
* Raw data from S3 is cleaned then loaded into a temporary staging table; during this the data is cast into appropriate data types, before being copied into one wide mastertable in snowflake. 
* SQL transformations will then be done on the mastertable to create fact and dimension tables.

![Alt Text](https://github.com/MubassirAhmed/ELT-Data-Pipeline/blob/main/include/Assets/Fact%20%26%20dimension%20tables.png) 

4. [Visualization](https://github.com/MubassirAhmed/Dash):  
* Finally, a [dashboard](https://github.com/MubassirAhmed/Dash) is built on top that queries the fact and dimension tables as an example end-user data product. 

5. Orchestration:
* Scraping, staging, and ETL are all automated and scheduled to run every hour using an Airflow DAG.


Deploy Your Project Locally
===========================

1. Start Airflow on your local machine by running 'astro dev start'.

This command will spin up 3 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks

2. Verify that all 3 Docker containers were created by running 'docker ps'.

Note: Running 'astro dev start' will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either stop your existing Docker containers or change the port.

3. Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with 'admin' for both your Username and Password.

You should also be able to access your Postgres Database at 'localhost:5432/postgres'.

Deploy Your Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://docs.astronomer.io/cloud/deploy-code/

Contact
=======

The Astronomer CLI is maintained with love by the Astronomer team. To report a bug or suggest a change, reach out to our support team: https://support.astronomer.io/# ELT-Data-Pipeline
