from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dbt_debug_dag',
    default_args=default_args,
    description='A simple DAG to run dbt debug',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 1, 1),
    catchup=False,
)

dbt_debug = BashOperator(
    task_id='dbt_debug',
    bash_command='cd /opt/airflow/dags/dbt/jaffle && dbt debug --profiles-dir /opt/airflow/dags/dbt/jaffle --project-dir /opt/airflow/dags/dbt/jaffle',
    dag=dag,
)
