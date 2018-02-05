"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


# example_configuration = {
#     "job_id": 123,
#     "s3_path": "...",
#     "table_schema": {
#         "id": 123,
#         "name": "...",
#         "adv_id": 123,
#         "columns": [ # ordering is implicit
#             {
#                 "name": "...",
#                 "type": "...",
#                 "alias": "..."
#              }
#         ]
#     }
# }

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 31),
    # 'email' : ['dataops@videoamp.com'],
    'email': ['ryan@videoamp.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'ingest_audience',
    default_args=default_args)

audience_spark = BashOperator(
    task_id='audience_spark',
    bash_command='sh /usr/local/airflow/bin/start_audience_ingest.sh ',
    dag=dag)

notify_api = BashOperator(
    task_id='notify_complete',
    bash_command='echo {{ dag_run.conf["test_setting"]["inner"] }} ',
    retries=3,
    dag=dag)

audience_spark.set_downstream(notify_api)
