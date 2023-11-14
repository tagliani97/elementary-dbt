from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount
from dynamic_task import DbtDagParser
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
    'network_mode': 'default',
    'image': "dbt_img:latest",
    'api_version': '1.37',
    'docker_url': 'TCP://docker-socket-proxy:2375',
    'mounts': [
        Mount(
            source="/home/serasa.intranet/c11170q/git/coe_localstack/devops/airflow/dbt",
            target=f"{DBT_PROJECT_DIR}",
            type="bind"
        )
    ],
}


def prepare_timestamp(dag_run: Optional[dict] = None) -> str:
    try:
        day_off: int = Variable.get("day_off", deserialize_json=True)
        delta: timedelta = timedelta(days=day_off)
    except KeyError:
        delta: timedelta = timedelta(days=1)

    if dag_run and 'execution_date' in dag_run.conf:
        return dag_run.conf['execution_date']
    else:
        return (datetime.now() - delta).strftime("%Y-%m-%d")

dag = DAG('my_dag',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    user_defined_macros={'prepare_timestamp': prepare_timestamp},
)

teste = DockerOperator(
    task_id='dbt_seed',
    command="echo {{ prepare_timestamp(dag_run) }}",
    dag=dag,
)


# dbt_seed = DockerOperator(
#     task_id='dbt_seed',
#     command=f'dbt {DBT_GLOBAL_CLI_FLAGS} seed --project-dir {DBT_PROJECT_DIR}',
#     dag=dag,
# )

# dag_parser = DbtDagParser(
#     dag=dag,
#     dbt_global_cli_flags=DBT_GLOBAL_CLI_FLAGS,
#     dbt_project_dir=DBT_PROJECT_DIR,
#     dbt_profiles_dir=DBT_PROFILE_DIR,
#     dbt_target=DBT_TARGET,
#     dbt_manifest=DBT_MANIFEST,
# )

# dag_parser.initialize_task_groups()

# dbt_run_group = dag_parser.get_dbt_run_group()
# dbt_test_group = dag_parser.get_dbt_test_group()

# dbt_seed >> dbt_run_group >> dbt_test_group

teste

