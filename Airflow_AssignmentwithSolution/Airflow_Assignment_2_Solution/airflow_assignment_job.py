from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator

# Define default_args dictionary to pass default parameters to the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026,5, 9),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG with the specified default_args
dag = DAG(
    'fetch_json_and_loadto_hive',
    default_args=default_args,
    description='DAG to fetch a daily JSON file from GCP bucket and load into Hive table on Dataproc',
    schedule_interval=timedelta(days=1),  # Set the DAG to run daily
)

# Define the GCS bucket and JSON file details
gcs_bucket = 'ak-airflow-bucket2'
gcs_object = 'data/Employee.json'

# Define the Hive table details


hive_table = 'employee'
hive_table_schema = 'emp_id INT, emp_name STRING, dept_id INT, salary INT'
hive_table_location = 'gs://ak-airflow-bucket2/hive_data/'

# Define the Hive query to load JSON data into the Hive table
hive_query = """
CREATE EXTERNAL TABLE IF NOT EXISTS employee (
    emp_id INT,
    emp_name STRING,
    dept_id INT,
    salary INT
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
STORED AS TEXTFILE
LOCATION 'gs://ak-airflow-bucket2/hive_data/';

"""

# Task 1: Use GCSToLocalFilesystemOperator to download the daily JSON file
download_task = GCSToLocalFilesystemOperator(
    task_id='download_from_gcs',
    bucket=gcs_bucket,
    object_name=gcs_object,
    filename='/tmp/daily_file.json',
    dag=dag,
    
)
# Task 3: Upload to Hive Table
upload_task = LocalFilesystemToGCSOperator(
    task_id='upload_to_hive_location',
    src='/tmp/daily_file.json',
    dst='hive_data/daily_file.json',
    bucket='ak-airflow-bucket2'
)

# Task 2: Use DataprocSubmitJobOperator to submit a Hive job on Dataproc
submit_hive_job = DataprocSubmitJobOperator(
    task_id='submit_hive_job',
    job={
        'reference': {'project_id': 'project-aedd3f2d-4596-4437-9dd'},
        'placement': {'cluster_name': 'spark-clusterak'},
        'hive_job': {'query_list': {'queries': [hive_query]}},
    },
    region='europe-central2',  # Specify the Dataproc region
    project_id='project-aedd3f2d-4596-4437-9dd',
    gcp_conn_id='google_cloud_default',
    dag=dag,
)

# Set task dependencies
download_task >> upload_task >> submit_hive_job