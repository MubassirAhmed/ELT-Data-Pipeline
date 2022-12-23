from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import include.extract as scraper
import include.transform_1 as tf1
import include.transform_2 as tf2
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

args = {
    'owner': 'Me',
    'start_date': days_ago(1) # make start date in the past
}
f_dag = DAG( dag_id='elt', default_args=args, schedule_interval="@hourly")



def runner1(ti):
    date_Time = datetime.now().strftime('%Y-%m-%d_Time-%H-%M')
    s3FileName = date_Time + '.csv'
    scraper.run1(s3FileName)
    ti.xcom_push(key='date_Time', value=date_Time)
    ti.xcom_push(key='s3FileName', value=s3FileName)

runner_1 = PythonOperator(
    task_id='runner1',
    python_callable=runner1,
    dag = f_dag
)


def transform1(ti):
    s3FileName = ti.xcom_pull(key='s3FileName', task_ids='runner1')
    tf1.main(s3FileName)

transform_1 = PythonOperator(
    task_id='transform1',
    python_callable = transform1,
    dag=f_dag
)


def runner2(ti):
    dateTime = ti.xcom_pull(key='date_Time', task_ids='runner1')
    s3FileName = ti.xcom_pull(key='s3FileName', task_ids='runner1')
    scraper.run2(s3FileName,dateTime)
    
runner_2 = PythonOperator(
    task_id='runner2',
    python_callable=runner2,
    dag=f_dag
)


def transform2(ti):
    s3FileName = ti.xcom_pull(key='s3FileName', task_ids='runner1')
    tf2.main(s3FileName)
    
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

