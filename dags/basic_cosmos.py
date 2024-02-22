from datetime import datetime

from cosmos import DbtDag, ProjectConfig, ProfileConfig, RenderConfig, LoadMode, ProjectConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping


profile_config = ProfileConfig(
    profile_name="jaffle_shop",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="airflow_db",
        profile_args={"schema": "public"},
    ),
)

basic_cosmos_dag = DbtDag(
    project_config=ProjectConfig(manifest_path="/opt/airflow/dags/dbt/jaffle/target/manifest.json", project_name="jaffle_shop", dbt_project_path="/opt/airflow/dags/dbt/jaffle/"),
    render_config=RenderConfig(load_method=LoadMode.DBT_MANIFEST, ),
    profile_config=profile_config,
    operator_args={
        "install_deps": False,
        "full_refresh": False,
    },
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="basic_cosmos_dag",
    default_args={"retries": 2},
)

