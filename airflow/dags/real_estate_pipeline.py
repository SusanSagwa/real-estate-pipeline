from datetime import datetime, timedelta

from airflow.sdk import dag
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.snowflake.operators.snowflake import SQLExecuteQueryOperator

DBT_DIR = "/usr/local/airflow/dbt_project"
DBT = "/usr/local/airflow/dbt_venv/bin/dbt"
PROFILES = "/usr/local/airflow/include/dbt_profile"

COPY_SQL = """
COPY INTO REAL_ESTATE.RAW.raw_house_sales (
  id, date, price, bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront,
  view, condition, grade, sqft_above, sqft_basement, yr_built, yr_renovated,
  zipcode, lat, long, sqft_living15, sqft_lot15, _source_file
)
FROM (
  SELECT $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,
         METADATA$FILENAME
  FROM @REAL_ESTATE.RAW.s3_raw_stage
)
PATTERN = '.*[.]csv'
"""


@dag(
    dag_id="real_estate_pipeline",
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
    tags=["real_estate", "dbt"],
)
def real_estate_pipeline():
    load_raw = SQLExecuteQueryOperator(
        task_id="load_raw",
        conn_id="snowflake_default",
        sql=COPY_SQL,
    )
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && {DBT} run --profiles-dir {PROFILES}",
    )
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && {DBT} test --profiles-dir {PROFILES}",
    )
    load_raw >> dbt_run >> dbt_test


real_estate_pipeline()
