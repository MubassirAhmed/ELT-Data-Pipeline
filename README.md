# Custom ELT Pipeline

Many jobs on Linkedin, tagged as entry-level roles, ask for several years of experience (YoE). Sorting through these is inefficient. The issue is further exacerbated when hundreds of new entry-level tagged jobs are posted everyday; going through **all** of them manually then becomes unfeasible. 

This project began as a way to automate this.  

## Overview

#### *Please press the play button on the top right of the flowchart below to start the animation.*

![Alt Text](https://github.com/MubassirAhmed/ELT-Data-Pipeline/blob/main/include/Assets/ELT%20Pipeline.gif) 


#### *To view the live dashboard, [click here](https://linkedin-job-tracker.onrender.com).* 


## Technical Description

**1. Scraping:**
* A Scrapy spider recursively crawls Linkedin, collecting job postings and uploading the data to a S3 bucket.

**2. ELT:**
* Data from S3 is cleaned, & loaded into a temporary staging table; during this the data is cast into appropriate data types, before being copied into one wide mastertable in snowflake. 
* SQL transformations will then be executed on the mastertable to create fact and dimension tables like so :~

![Alt Text](https://github.com/MubassirAhmed/ELT-Data-Pipeline/blob/main/include/Assets/Fact%20%26%20dimension%20tables.png) 

**3. Visualization:**  
* A [dashboard](https://github.com/MubassirAhmed/Dash) finally queries these tables to visualize and present the organized data.

**4. Orchestration:**
* Scraping, staging, and ELT are automated and scheduled to run every hour using an Airflow DAG.

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
* Some transformations are currently done with pandas. The equivalent SQL transformations are under development.
* Some transformations scripts are not idempotent and so backfilling currently creates duplicate records.

