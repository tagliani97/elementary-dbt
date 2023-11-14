from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount
from datetime import datetime, timedelta
from airflow.models import Variable
from typing import Optional

DBT_MANIFEST = "/opt/airflow/dags/"
DBT_PROFILE_DIR = "/home/airflow/dbt/"
DBT_PROJECT_DIR = "/home/jaffle_shop/"
DBT_GLOBAL_CLI_FLAGS = "--no-write-json"
DBT_TARGET = "dev"
DBT_TAG = "tag_staging"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'network_mode': 'dbt-teste',
    'image': "dbt_img:latest",
    'api_version': '1.37',
    'docker_url': 'TCP://docker-socket-proxy:2375',
    'mounts': [
        Mount(
            source="/home/tagliani/git/elementary-dbt/jaffle",
            target=f"{DBT_PROJECT_DIR}",
            type="bind"
        )
    ],
}

dag = DAG('init_dbt',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    user_defined_macros={'prepare_timestamp': prepare_timestamp},
)

dbt_debug = DockerOperator(
    task_id='dbt_debug',
    command=f'dbt {DBT_GLOBAL_CLI_FLAGS} debug --project-dir {DBT_PROJECT_DIR}',
    dag=dag,
)

dbt_seed = DockerOperator(
    task_id='dbt_seed',
    command=f'dbt {DBT_GLOBAL_CLI_FLAGS} seed --project-dir {DBT_PROJECT_DIR}',
    dag=dag,
)

dbt_debug >> dbt_seed