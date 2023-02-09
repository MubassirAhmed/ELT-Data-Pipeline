import boto3
import pandas as pd
from io import BytesIO
from word2number import w2n
import snowflake.connector
import os
from snowflake.connector.pandas_tools import write_pandas
from num2words import num2words
import nltk
nltk.download('punkt')
#from nltk.tokenize import word_tokenize


def main(s3Bucket, s3FileName_key):
    df = load_csv_from_s3(s3Bucket, s3FileName_key)
    df = transform(df)
    create_stagingTable(df)
    load_to_stage(df)
    #get_jobsList_from_last3Days()



def load_csv_from_s3(s3Bucket, s3FileName_key):
    # Initialize s3
    s3 = boto3.resource('s3',
                        aws_access_key_id='AKIAYUJWZRTZXMMGGNFE',
                        aws_secret_access_key='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',)
    # Reading CSV into DF  
    obj = s3.Object(s3Bucket[:-1], s3FileName_key)
    with BytesIO(obj.get()['Body'].read()) as bio:
        df = pd.read_csv(bio)
    return df


def transform(df):
    counter = 0
    years_to_colum = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
#     tag_filters = ['sql','python','airflow','etl','snowflake','aws','azure','gcp','bigquery','spark',
#                         'hadoop','hive','lambda','dbt', 'google','amazon','microsoft','bi','tableau',
#                    'power','looker', 'excel','javascript','react','vue']
#     for tag in tag_filters:
#         df[tag]=0
    years = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',
             'one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve',
            'thirteen','fourteen','fifteen']
    for year in years_to_colum:
        df[year]=0
    for i in range(df.shape[0]):
        paraSplitted = df.loc[i,'description'].replace(","," ").replace('+'," ").replace('/'," ").replace("'"," ").replace("-"," ").replace('('," ").replace(')'," ").lower().split()
        paraSplitted = [word.replace(","," ").replace('+'," ").replace('/'," ").replace("'"," ").replace('-','') for word in paraSplitted]
        #         # Marking tags
        #         for word in paraSplitted:
        #             for tag in tag_filters:
        #                 if tag == word:
        #                     df.loc[i,tag]=1
        # Marking years
        expIndices = [i for i in range(len(paraSplitted)) if 'experience' == paraSplitted[i]]
        counter = counter + len(expIndices)
        for instance_of_exp in expIndices:
            count = 0
            for year in years:
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
        if 1 not in [df.loc[i,str(j)] for j in range(1,16)]:
            df.loc[i,'0']=1
    #remove_titles:
    rejectTitles = ['manager','summer','intern/co-op','co-op',
                    'coop', 'student', 'intership', 'vice president',
                    'vp','intern','senior','sr','sr.','director',
                    'principal','architect', 'lead']       
    df['remove_titles']=0
    for i in range(df.shape[0]):
        title_tokens = nltk.tokenize.word_tokenize(df.title[i].replace('-',''))
        title_tokens_clean = [word.lower() for word in title_tokens]
        if (any(word in title_tokens_clean for word in rejectTitles)):
            df.loc[i,'remove_titles']=1
    return df

def _transform(df):
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
    os.environ['SNOW_USER']='mvbasxhr'
    os.environ['SNOW_PWD']='ReLife!23'
    os.environ['SNOW_ACCOUNT']='kl20451.ca-central-1.aws'
    os.environ['SNOW_WH']='AIRFLOW_ELT_WH'
    os.environ['SNOW_DB']='AIRFLOW_ELT_DB'
    os.environ['SNOW_SCH']='AIRFLOW_ELT_SCHEMA'
    con = snowflake.connector.connect(
    user=os.getenv('SNOW_USER'),
    password=os.getenv('SNOW_PWD'),
    account=os.getenv('SNOW_ACCOUNT'),)
    # IDK y but snowflake makes me choose a schema before i can do anything
    con.cursor().execute(" CREATE WAREHOUSE if not exists AIRFLOW_ELT_WH;")
    con.cursor().execute(" CREATE DATABASE if not exists AIRFLOW_ELT_DB;")
    con.cursor().execute(" USE DATABASE AIRFLOW_ELT_DB;")
    con.cursor().execute(" CREATE SCHEMA if not exists AIRFLOW_ELT_SCHEMA;")
    con.cursor().execute(" USE SCHEMA AIRFLOW_ELT_SCHEMA;")
    return con


def create_stagingTable(df):
    con = get_snowflake_connector()

    for col in df.columns:
        if col.isnumeric():
            df = df.rename(columns = {col: num2words(col)})
    # UpperCasing all Col names                               
    df.columns = [col.upper() for col in df.columns]
    con.cursor().execute(f"CREATE OR REPLACE TABLE JOB_POSTINGS_STAGE (" + " ".join([str(df.columns[i]).upper() + " STRING," for i in range(len(df.columns))])[:-1] + ");" )
    con.close()


def load_to_stage(df):
    for col in df.columns:
        if col.isnumeric():
            df = df.rename(columns = {col: num2words(col)})
    # UpperCasing all Col names                               
    df.columns = [col.upper() for col in df.columns]
    con = get_snowflake_connector()
    success, num_chunks, num_rows, output = write_pandas(con, df, 'JOB_POSTINGS_STAGE')
    print(success,num_rows)  
    con.close()  


def get_jobsList_from_last3Days():
    con = get_snowflake_connector()
    job_links = con.cursor().execute("With unique_jobs as ( "
                                    "Select * "
                                    "from job_postings "
                                    "Qualify row_number() over (partition by job_id order by one) = 1 "
                                    ") "
                                    "Select "
                                    "    job_link"
                                    "From unique_jobs "
                                    ).fetchall()
    with open('job_links.txt', 'w') as f:
        for link in job_links:
            f.write(f"{link}\n")
    con.close()


if __name__ == '__main__':
    s3Bucket = 'linkedin-scraper-1/'
    s3FileName_key = 'runner_1_dev/2023-02-08_Time-10-47.csv'
    df = load_csv_from_s3(s3Bucket, s3FileName_key)
    df = transform(df)
    create_stagingTable(df)
    load_to_stage(df)    
