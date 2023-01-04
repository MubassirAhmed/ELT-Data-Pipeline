# Custom ETL Pipeline

Many jobs on Linkedin, tagged as entry-level roles, ask for several years of experience (YoE). Sorting through these is inefficient. The issue is further exacerbated when hundreds of new entry-level tagged jobs are posted everyday; going through **all** of them manually then becomes unfeasible. 

This project began as a way to automate this.  

## Overview

![Alt Text](https://github.com/MubassirAhmed/ELT-Data-Pipeline/blob/main/include/Assets/ELT%20Pipeline.gif) 


#### *This pipeline scrapes new jobs from Linkedin every hour, then cleans & transforms the data in a warehouse, creating tables, that are then conveniently queried by a [dashboard for further analysis](https://easy-bottles-grin-34-125-254-54.loca.lt).* 


## Technical Description

**1. Orchestration:**
* Scraping, staging, and ELT are automated and scheduled to run every hour using an Airflow DAG.

**2. Scraping:**
* A Scrapy spider recursively crawls Linkedin, collecting job postings and uploading the data to a S3 bucket.

**3. Stage/Datalake:** 
* Stores a historical snapshot of the source data, allowing any data discrepencies downstream to be traced back to the source. This data lineage is useful when debugging the pipeline. 

**4. ELT:**
* Data from S3 is cleaned, & loaded into a temporary staging table; during this the data is cast into appropriate data types, before being copied into one wide mastertable in snowflake. 
* SQL transformations are then executed on the mastertable to create fact and dimension tables like so :~

![Alt Text](https://github.com/MubassirAhmed/ELT-Data-Pipeline/blob/main/include/Assets/Fact%20%26%20dimension%20tables.png) 

**5. Visualization:**  
* A [dashboard](https://github.com/MubassirAhmed/Dash) finally queries these tables to visualize and present the organized data.


## Deploying The Pipeline Locally  

1. Install astro CLI with brew by running:
```
brew install astro
```
2. Clone the repo, then run:
```
cd ELT-Data-Pipeline && pip3 install -r requirements.txt
```
3. Run the following to start Airflow on localhost:
```
astro dev init && astro dev start
```

## Known Issues
* Some transformations scripts are not idempotent and so backfilling currently creates duplicate records.

