from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='spark_streaming_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@once',
    catchup=False
) as dag:

    run_spark = BashOperator(
        task_id='run_spark_job',
        bash_command='spark-submit /home/train/airflow_project/dags/spark_kafka_streaming.py'
    )
