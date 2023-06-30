"""
Main Class , Python Glue Jobs Data Ingestor
"""
import logging
import sys
import json

import awswrangler as wr
import pandas as pd
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

# limit is between 1 and 1000
local_mode = False

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)
pd.set_option('display.float_format', '{:20,.2f}'.format)
pd.set_option('display.max_colwidth', None)

def run_ingestion():

    ## get Xrefs
    print("Get employee Xref List: " + str(datetime.now()))
    xref_list = api.getDayForceEmployeeXrefs(token=token, employee_url=employee_api_url)
    ##Initiate bulk request
    print("Initiate bulk request : " + str(datetime.now()))
    expanders = 'EmployeeProperties'
    query_result = api.createRestBulkEmployeeJob(xref_string=xref_list, token=token, expanders=expanders, bulk_url=bulk_export_api_url)
    if (query_result is not None):
        try:
            raw_json_payload = query_result
            print("Attempting to convert to a pandas DataFrame : " + str(datetime.now()))
            try:
                df = RawToDF.convert_json_to_df(raw_json_payload)
            except Exception as e1:
                print("Failed to load JSON into DataFrame")
                print(e1)
            print("Columns to drop:")
            print(drop_cols)
            print("--------")
            print("DF before dropping columns")
            print(df.dtypes)
            print("--------")
            # Drop Columns

            df = RawToDF.drop_columns(df, columns=drop_cols)
            print("DF after dropping columns")
            print(df.dtypes)
            print("--------")
            # Create standart DF with fix column size to eliminate column mismatch failure
            # add ingestion date as partition date
            df['partition_date'] = pd.to_datetime('today').strftime("%Y%m%d")
            df['_ingestion_timestamp'] = ingestion_timestamp
            now = datetime.now()
            file_date = now.strftime("%Y-%m-%d-%H-%M-%S-%f")[:-3]  # [:-3] => Removing the 3 last characters as %f is for millis.
            file_name = f'{file_date}_utc.json'
            seq_number="1"

            landing_writer.s3_to_json_basic(df=df, seq_number=seq_number, ingestion_date=ingestion_date)

            print("finished writing to raw zone, start flattening for processed zone")
            json_file = df.to_json()
            loads_json = json.loads(json_file)
            flatten_json_data = RawToDF.get_flatten_dayforce_data(loads_json
                                                                  ,option_value_list
                                                                  ,properties_list)
            print("finished flattening json data")
            df = RawToDF.convert_json_to_df(flatten_json_data)
            df = RawToDF.drop_columns(df, columns=drop_cols)
            print("DF after flattening and column drop")
            print(df.dtypes)
            df.info(verbose=True)

            df = RawToDF.rename_mapped_columns(df=df, column_map=actual_rename_mapping_cols)
            empty_df = pd.DataFrame(columns=parquet_dest_col_list)
            df = pd.concat([df, empty_df])
            df['partition_date'] = pd.to_datetime('today').strftime("%Y%m%d")
            df['_ingestion_timestamp'] = ingestion_timestamp
            print("Final DF ")
            print(df.head())
            df.info(verbose=True)
            if (not df.empty):
                processed_writer.s3_to_parquet(df=df, seq_number=seq_number, ingestion_date=ingestion_date, mode="overwrite_partitions", dtypes_col_list=dtypes_col_list)
                processed_writer.redshift_copy(df=df, seq_number=seq_number, ingestion_date=ingestion_date, mode="upsert", dtypes_col_list=dtypes_col_list)

        except Exception as e:
            print("Unexpected error: %s" % e)

    else:
        print("Query is empty or None!")
        #break

def refresh_token():
    global token, api
    token = None
    api = RestApiClient()
    if api.getDayForceAccessToken(secrets=secrets, token_api_url=token_api_url) is not None:
        token = api.getDayForceAccessToken(secrets=secrets,token_api_url=token_api_url)
    else:
        logging.error("Token is None")

if __name__ == "__main__":

    aws_secret_manager_region = "us-east-1"
    bucket_name = 'landing.datalake.reporting-dev.e.inc'
    table = "dayforce_employee"
    secret_name = "dev/dayforce/user/pass/secrets"
    database = "dayforce_test_fuat_db"

    # True when running on local computer-requires aws creds setup, otherwise False
    if local_mode:
        sys.path.append(
            '../../common_api_lib/dist/commonPythonGlueLib-1.0.0-py3-none-any.whl')  # add lib file to directtory path
    else:
        from awsglue.utils import getResolvedOptions

        args = getResolvedOptions(sys.argv, [
            'aws_secret_manager_region',
            'bucket_name',
            'table',
            'secret_name',
            'database',
            'redshift_glue_connector',
            's3_raw_bucket_name',
            'employee_api_url',
            'bulk_export_api_url',
            'env',
            'token_api_url'
        ])
        aws_secret_manager_region = str(args['aws_secret_manager_region']).strip()
        processed_bucket_name = str(args['bucket_name']).strip()
        landing_bucket_name = str(args['s3_raw_bucket_name']).strip()
        table = str(args['table']).strip()
        secret_name = str(args['secret_name']).strip()
        database = str(args['database']).strip()
        redshift_glue_connector = str(args['redshift_glue_connector']).strip()
        token_api_url = str(args['token_api_url']).strip()
        employee_api_url = str(args['employee_api_url']).strip()
        bulk_export_api_url = str(args['bulk_export_api_url']).strip()
        s3_raw_bucket_name = str(args['s3_raw_bucket_name']).strip()
        env = str(args['env']).strip()

    from commonPythonGlueLib.src.apis.rest.RestApiClient import RestApiClient
    from commonPythonGlueLib.src.aws.acm.AwsSecretManager import AwsSecretManager
    from commonPythonGlueLib.src.transform.RawToDF import RawToDF
    from commonPythonGlueLib.src.transform.TableProps import TableProps
    from commonPythonGlueLib.src.writer.Writer import Writer
    from commonPythonGlueLib.src.apis.rest.RestApiClient import RestApiClient

    sm = AwsSecretManager(region_name=aws_secret_manager_region)
    secrets = sm.get_secret(secret_name)

    refresh_token()

    ingestion_timestamp = pd.to_datetime('now', utc=True).strftime("%Y-%m-%d %H:%M:%S")
    ingestion_date = pd.to_datetime('now', utc=True).strftime("%Y%m%d")
    source_name='dayforce'

    con = wr.redshift.connect(redshift_glue_connector)
    landing_writer = Writer(
        bucket_name=landing_bucket_name,
        s3_raw_bucket_name=s3_raw_bucket_name,
        env=env,
        source_name=source_name,
        database=database,
        table="raw_" + table,
        con=con
    )
    processed_writer = Writer(
        bucket_name=processed_bucket_name,
        s3_raw_bucket_name=s3_raw_bucket_name,
        env=env,
        source_name=source_name,
        database=database,
        table=table,
        con=con
    )
    # Get Table Properties.
    print("Getting table properties from YAML file: " + str(datetime.now()))
    table_props = TableProps(source_name=source_name)
    actual_rename_mapping_cols = table_props.get_mapped_columns(table_name=table.lower())
    drop_cols = table_props.get_drop_columns(table_name=table.lower())
    json_dest_col_list = table_props.get_json_dest_columns(table_name=table.lower())
    parquet_dest_col_list = table_props.get_parquet_dest_columns(table_name=table.lower())

    dtypes_col_list = table_props.get_dtypes_columns(table_name=table.lower())
    last_update_column = table_props.get_last_update_column(table_name=table.lower())

    properties_list = table_props.get_dayforce_properties_columns(table_name=table.lower())
    option_value_list = table_props.get_dayforce_option_value_columns(table_name=table.lower())

    if (token is not None):
        print("Start Full Load: "+ str(datetime.now()))
        condition = ""
        # Create the pandas DataFrame
        run_ingestion()
        refresh_token()
        print("End Full Load: "+ str(datetime.now()))
