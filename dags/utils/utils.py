import boto3
import pandas as pd
from io import BytesIO
import snowflake.connector
import os

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


def load_csv_from_s3(s3Bucket, s3FileName_key):
    # Initialize s3
    s3 = boto3.resource('s3',
                        aws_access_key_id='AKIAYUJWZRTZZEA5BGU4',
                        aws_secret_access_key='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',
                        )
    
    # Reading CSV into DF  
    obj = s3.Object(s3Bucket[:-1], s3FileName_key)
    with BytesIO(obj.get()['Body'].read()) as bio:
        df = pd.read_csv(bio)

    return df