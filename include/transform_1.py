import boto3
import pandas as pd
from io import BytesIO
from word2number import w2n
import snowflake.connector
import os
from snowflake.connector.pandas_tools import write_pandas
from num2words import num2words


def load_csv_from_s3(s3Bucket, s3FileName_key):
    
    # Setup variables
    """os.environ['AWS_ACCESS_KEY_ID']='AKIAYUJWZRTZRRGQ3JVV'
    os.environ['AWS_SECRET_ACCESS_KEY']='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'"""

    # Initialize s3
    s3 = boto3.resource('s3',
                        aws_access_key_id='AKIAYUJWZRTZRRGQ3JVV',
                        aws_secret_access_key='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',
                        )
    
    # Reading CSV into DF  
    obj = s3.Object(s3Bucket[:-1], s3FileName_key)
    with BytesIO(obj.get()['Body'].read()) as bio:
        df = pd.read_csv(bio)

    return df


#! Never drop anything in transform. Only transform.
def transform(df):
    counter = 0
    
    years_to_colum = ['0','1','2','3','4','5','6','7','8','9','10','12','13','14','15']
    
    tag_filters = ['sql','python','airflow','etl','snowflake','aws','azure','gcp','bigquery','spark',
                        'hadoop','hive','lambda','dbt', 'google','amazon','microsoft','bi','tableau',
                   'power','looker', 'excel','javascript','react','vue']
    
    years = ['1','2','3','4','5','6','7','8','9','10','12','13','14','15',
             'one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve',
            'thirteen','fourteen','fifteen']
        
    for year in years_to_colum:
        df[year]=0
        
    for tag in tag_filters:
        df[tag]=0
    
    for i in range(df.shape[0]):
        paraSplitted = df.loc[i,'description'].replace(","," ").replace('+'," ").replace('/'," ").replace("'"," ").replace("-"," ").replace('('," ").replace(')'," ").lower().split()

        # Marking tags
        for word in paraSplitted:
            for tag in tag_filters:
                if tag == word:
                    df.loc[i,tag]=1
        
        
        # Marking years
        expIndices = [i for i in range(len(paraSplitted)) if 'experience' == paraSplitted[i]]
        counter = counter + len(expIndices)
        blank_exp = 0
        for instance_of_exp in expIndices:
            count = 0
            for year in years:
                
                # counting to 2 because no line will mention more than 2 numbers, ex: " 2-5 of experience..."  
                if count == 2:
                    break
                
                # Marks years 1 -15
                if year in paraSplitted[instance_of_exp-10:instance_of_exp+10]:
                    
                    # Marks single digit years, 1 - 9
                    if len(year) == 1 or len(year)==2:
                        df.loc[i,str(year)]=1
                        count += 1
                        
                    # Marks years 10-15
                    else:
                        df.loc[i,str(w2n.word_to_num(year))]=1
                        count += 1
                
                # Marks jobs with no specific YoE req.
                else:
                    if year == years[-1]:
                        blank_exp += 1
                        if blank_exp == len(expIndices):
                            df.loc[i,'0']= 1
     
    print(df.columns)
    """
    ['title', 'appsPerHour', 'noApplicants', 'postedTimeAgo', 'company',
       'job_link', 'description', 'typeOfJob', 'job_id', '0', '1', '2', '3',
       '4', '5', '6', '7', '8', '9', '10', '12', '13', '14', '15', 'sql',
       'python', 'airflow', 'etl', 'snowflake', 'aws', 'azure', 'gcp',
       'bigquery', 'spark', 'hadoop', 'hive', 'lambda', 'dbt', 'google',
       'amazon', 'microsoft', 'bi', 'tableau', 'power', 'looker', 'excel',
       'javascript', 'react', 'vue']
    """
    for col in df.columns:
        if col.isnumeric():
            df = df.rename(columns = {col: num2words(col)})
            
    # UpperCasing all Col names                               
    df.columns = [col.upper() for col in df.columns]                
    return df
    
def get_snowflake_connector():
    os.environ['SNOW_USER']='mvbashxr'
    os.environ['SNOW_PWD']='ReLife!23'
    os.environ['SNOW_ACCOUNT']='ep66367.ca-central-1.aws'
    os.environ['SNOW_WH']='AIRFLOW_ELT_WH'
    os.environ['SNOW_DB']='AIRFLOW_ELT_DB'
    os.environ['SNOW_SCH']='AIRFLOW_ELT_SCHEMA'

    
    con = snowflake.connector.connect(
    user=os.getenv('SNOW_USER'),
    password=os.getenv('SNOW_PWD'),
    account=os.getenv('SNOW_ACCOUNT'),
    warehouse=os.getenv('SNOW_WH'),
    database=os.getenv('SNOW_DB'),
    schema=os.getenv('SNOW_DH')
    )
    # IDK y but snowflake makes me choose a schema before i can do anything
    con.cursor().execute("USE SCHEMA AIRFLOW_ELT_SCHEMA")
    return con


def load_to_snowflake(df):
    con = get_snowflake_connector()
    
    # Create a fresh table, dynamically defining columns from df.columns
    #con.cursor().execute("create if not exists table job_postings (" + " ".join([str(df.columns[i]) + " string," for i in range(len(df.columns))])[:-1] + ");" )
    #ALTER TABLE job_postings ADD PRIMARY KEY (job_id);
    success, num_chunks, num_rows, output = write_pandas(con, df, 'JOB_POSTINGS')
    print(success,num_rows)  
    
    con.close()  


def load_job_links():
    con = get_snowflake_connector()
    job_links = con.cursor().execute("With unique_jobs as ( "
                                    "Select * "
                                    "from job_postings "
                                    "Qualify row_number() over (partition by job_id order by one) = 1 "
                                    ") "
                                    "Select "
                                    "    job_link "
                                    "From unique_jobs "
                                    ).fetchall()
    with open('job_links.txt', 'w') as f:
        for link in job_links:
            f.write(f"{link}\n")
    con.close()


def main(s3Bucket, s3FileName_key):
    df = load_csv_from_s3(s3Bucket, s3FileName_key)
    transformed_df = transform(df)
    load_to_snowflake(transformed_df)
    load_job_links()



if __name__ == '__main__':
    #df = pd.read_csv('/Users/mvbasxhr/Downloads/2022-12-20_Time-21-35.csv')
    #transform(df)
    colNames = ['title', 'appsPerHour', 'noApplicants', 'postedTimeAgo', 'company',
       'job_link', 'description', 'typeOfJob', 'job_id', '0', '1', '2', '3',
       '4', '5', '6', '7', '8', '9', '10', '12', '13', '14', '15', 'sql',
       'python', 'airflow', 'etl', 'snowflake', 'aws', 'azure', 'gcp',
       'bigquery', 'spark', 'hadoop', 'hive', 'lambda', 'dbt', 'google',
       'amazon', 'microsoft', 'bi', 'tableau', 'power', 'looker', 'excel',
       'javascript', 'react', 'vue']
    buildColDynamically = " ".join([str(colNames[i]).upper() + " string," for i in range(len(colNames))])[:-1]
    con = get_snowflake_connector()
    con.cursor.execute(
    'create or replace transient table duplicate_holder as (select ' + buildColDynamically + ' from some_table group by '+ buildColDynamically +' having count(*)>1;')

