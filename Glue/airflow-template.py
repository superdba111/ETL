from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from airflow.providers.amazon.aws.operators.lambda_function import LambdaFunctionOperator
from airflow.providers.amazon.aws.transfers.redshift_to_s3 import RedshiftToS3Operator
from airflow.utils.dates import days_ago

# Defining the default_args for your DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['youremail@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'aws_data_pipeline',
    default_args=default_args,
    description='A simple AWS data pipeline',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
) as dag:

    # Operator to start an AWS Glue job
    run_glue_job = AwsGlueJobOperator(
        task_id='run_glue_job',
        job_name='your-glue-job-name',
        script_location='s3://your-script-location-path',
        aws_conn_id='aws_default'
    )

    # Operator to run an AWS Lambda function
    run_lambda = LambdaFunctionOperator(
        task_id='run_lambda',
        aws_conn_id='aws_default',
        function_name='your-lambda-function-name',
        region_name='us-east-1',
        payload={"key": "value"},
        log_type='Tail'
    )

    # Operator to transfer data from Redshift to S3
    redshift_to_s3 = RedshiftToS3Operator(
        task_id='redshift_to_s3',
        aws_conn_id='aws_default',
        s3_bucket='your-s3-bucket',
        s3_key='data/key/location',
        redshift_conn_id='redshift_default',
        schema='public',
        table='your_table_name',
    )

    # Set up the pipeline
    run_glue_job >> run_lambda >> redshift_to_s3
