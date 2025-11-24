from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# UPDATE THIS PATH to your actual project folder
PROJECT_PATH = "/home/rodrigo/Desktop/data_mining_project/Airflow-Apriori-Pipeline"

default_args = {
    'owner': 'rodrigo',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 1, 1),
}

with DAG(
    dag_id='apriori_bookstore_pipeline',
    default_args=default_args,
    description='A data mining pipeline for bookstore transactions',
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task 1: Load and Clean Data
    t1_clean = BashOperator(
        task_id='load_and_clean',
        bash_command=f'python3 {PROJECT_PATH}/scripts/load_data.py'
    )

    # Task 2: Run Apriori Algorithm
    t2_mine = BashOperator(
        task_id='run_apriori',
        bash_command=f'python3 {PROJECT_PATH}/scripts/apriori.py'
    )

    # Task 3: Generate Reports
    t3_report = BashOperator(
        task_id='generate_report',
        bash_command=f'python3 {PROJECT_PATH}/scripts/generate_report.py'
    )

    # Define Dependency Flow
    t1_clean >> t2_mine >> t3_report
