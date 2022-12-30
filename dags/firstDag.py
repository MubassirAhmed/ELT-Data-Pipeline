from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import include.extract as scraper
import include.transform_1 as tf1
import include.transform_2 as tf2
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

args = {
    'owner': 'Me',
    'start_date': days_ago(1) # make start date in the past
}
f_dag = DAG( dag_id='elt_dev', default_args=args, schedule_interval="@hourly",catchup=False)



def runner1(ti):
    #here I'm defining s3 stuff for central source of control
    s3Bucket = 'linkedin-scraper-1/'
    s3FolderRun1 = 'runner_1_dev/'
    TimeObject = (datetime.utcnow()+timedelta(hours=-5))
    TimeScraped = TimeObject.strftime('%Y-%m-%d_Time-%H-%M')
    snow_col_timestamp = TimeObject.strftime('%Y-%m-%d %H:%M:%S')
    Hour = TimeObject.strftime('%H')
    dayOfWeek = TimeObject.strftime('%a')
    dayOfTheMonth = TimeObject.strftime('%d')
    NameOfMonth = TimeObject.strftime('%b')
    MonthNumber = TimeObject.strftime('%m')
    #print(Hour, dayOfWeek, dayOfTheMonth, NameOfMonth, MonthNumber)
    s3Run1FileName =  s3Bucket + s3FolderRun1 + TimeScraped + '.csv'

    scraper.run1(s3Run1FileName,TimeScraped,
                snow_col_timestamp,
                Hour,
                dayOfWeek,
                dayOfTheMonth,
                NameOfMonth,
                MonthNumber)

    ti.xcom_push(key='s3Bucket', value=s3Bucket)
    ti.xcom_push(key='s3FolderRun1', value=s3FolderRun1)
    ti.xcom_push(key='TimeScraped', value=TimeScraped)
    ti.xcom_push(key='s3Run1FileName', value=s3Run1FileName)

runner_1 = PythonOperator(
    task_id='runner1',
    python_callable=runner1,
    dag = f_dag
)


def transform1(ti):
    s3Bucket = ti.xcom_pull(key='s3Bucket', task_ids='runner1')
    s3FolderRun1 = ti.xcom_pull(key='s3FolderRun1', task_ids='runner1')
    TimeScraped = ti.xcom_pull(key='TimeScraped', task_ids='runner1')
    s3FileName_key = s3FolderRun1 + TimeScraped +  ".csv"
    tf1.main(s3Bucket, s3FileName_key)

transform_1 = PythonOperator(
    task_id='transform1',
    python_callable = transform1,
    dag=f_dag
)


def runner2(ti):
    s3Bucket = ti.xcom_pull(key='s3Bucket', task_ids='runner1')
    s3FolderRun2 = 'runner_2_dev/'
    TimeScraped = ti.xcom_pull(key='TimeScraped', task_ids='runner1')
    #here im defining s3 stuff for central source of control
    s3Run2FileName  = s3Bucket +  s3FolderRun2 + TimeScraped + '.csv'

    scraper.run2(s3Run2FileName,TimeScraped)

    ti.xcom_push(key='s3FolderRun2', value=s3FolderRun2)
    
runner_2 = PythonOperator(
    task_id='runner2',
    python_callable=runner2,
    dag=f_dag
)


def transform2(ti):
    s3Bucket = ti.xcom_pull(key='s3Bucket', task_ids='runner1')
    s3FolderRun2  =  ti.xcom_pull(key='s3FolderRun2', task_ids='runner2')
    TimeScraped = ti.xcom_pull(key='TimeScraped', task_ids='runner1')
    s3FileName_key = s3FolderRun2 + TimeScraped + '.csv' 

    tf2.main(s3Bucket, s3FileName_key)
    
transform_2 = PythonOperator(
    task_id='transform2',
    python_callable = transform2,
    dag=f_dag
)


runner_1 >> transform_1 >> runner_2 >> transform_2


"""bash_example =  BashOperator(
    task_id = 'print_python_packages',
    bash_command ='pip3 freeze',
    #dag=f_dag
)"""