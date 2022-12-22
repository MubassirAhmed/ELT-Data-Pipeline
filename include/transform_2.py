import boto3
import pandas as pd
from io import BytesIO
from word2number import w2n
import snowflake.connector
import os
from snowflake.connector.pandas_tools import write_pandas
from num2words import num2words
from transform_1 import load_csv_from_s3, get_snowflake_connector


def transform(df):
    df.columns = [col.upper() for col in df.columns]                
    return df

def new_table_from_df(con, df, table_name):
    con.cursor().execute(f"create or replace table {table_name.upper()} (" + " ".join([str(df.columns[i]).upper() + " string," for i in range(len(df.columns))])[:-1] + ");" )
    success, num_chunks, num_rows, output = write_pandas(con, df, f'{table_name.upper()}')
    return success, num_rows

def load_to_snowflake(df):
    con = get_snowflake_connector()
    #con.cursor().execute("create table job_apps_counter (" + " ".join([str(df.columns[i]) + " string," for i in range(len(df.columns))])[:-1] + ");" )
    success, num_chunks, num_rows, output = write_pandas(con, df, 'JOB_APPS_COUNTER')
    print(success,num_rows)  
    con.close()  


def main(s3FileName):
    s3FileName_key = f'runner_2/{s3FileName}' 
    df = load_csv_from_s3(s3FileName_key)
    transformed_df = transform(df)
    load_to_snowflake(transformed_df)
    
if __name__ == '__main__':
    main('2022-12-22_Time-08-02.csv')