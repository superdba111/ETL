"""
Main Class , Python Glue Jobs Data Ingestor
"""
import logging
import sys
import json

import awswrangler as wr
import pandas as pd
from datetime import datetime, timedelta
# limit is between 1 and 1000
local_mode = False

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)
pd.set_option('display.float_format', '{:20,.2f}'.format)
pd.set_option('display.max_colwidth', None)

def parse_start_date(arg_start_date):
    start = datetime.today() - timedelta(days=3)
    if arg_start_date.strip() == "start_date":
        start_date = pd.Timestamp(start.strftime("%Y-%m-%d") + ' 00:00:00')
        print(f"No date supplied use default start date {start_date}")
    else:
        try:
            start_date = datetime.strptime(arg_start_date + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
            print(f"Using source argument date {start_date}")
        except:
            start_date = pd.Timestamp(start.strftime("%Y-%m-%d") + ' 00:00:00')
            print(f"No valid date use default start date {start_date}")
    return start_date

def parse_end_date(arg_end_date):
    end = datetime.today() - timedelta(days=1)
    print(end)
    print(f"Trying to parse end date {arg_end_date.strip()}")
    if arg_end_date.strip() == "end_date":
        end_date = pd.Timestamp(end.strftime("%Y-%m-%d") + ' 23:59:59')
        print(f"No date supplied use default end date {end_date}")
    else:
        try:
            end_date = datetime.strptime(arg_end_date + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
            print(f"Using source argument date {end_date}")
        except:
            end_date = pd.Timestamp(end.strftime("%Y-%m-%d") + ' 00:00:00')
            print(f"No valid date use default end date {end_date}")
    return end_date

def run_ingestion():

    start_date = parse_start_date(args_start_date)
    end_date = parse_end_date(args_end_date)
    print(type(start_date))
    print(start_date)
    print(type(end_date))
    print(end_date)
    ingestion_period = end_date - start_date
    print("ingestion_period: " + str(ingestion_period.days))
    if ingestion_period.days >= 32:
        raise Exception("Parameter input error: " + " date range is greater than 31 days ")


    query_result = api.getDayForceEmployeePayrollSummaryData(token=token,pay_summary_api_url=pay_summary_api_url,start_date=start_date,end_date=end_date)
    if (query_result is not None):
        try:
            print("Attempting to convert to a pandas DataFrame : " + str(datetime.now()))

            df = pd.DataFrame(query_result)
            print(df.count())
            print(df.info())
            if df.empty == True:
                raise Exception("Exception raised: Non data at source ")
            print("DF before dropping columns")
            print(df.dtypes)
            print("--------")
            # Drop Columns
            df = RawToDF.drop_columns(df, drop_cols)

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
            df = RawToDF.rename_mapped_columns(df=df, column_map=actual_rename_mapping_cols)
            empty_df = pd.DataFrame(columns=dest_cols)
            df['partition_date'] = pd.to_datetime('today').strftime("%Y%m%d")
            df['_ingestion_timestamp'] = ingestion_timestamp
            df['filter_pay_summary_start_date'] = start_date
            df['filter_pay_summary_end_date'] = end_date
            empty_df['partition_date'] = pd.to_datetime('today').strftime("%Y%m%d")
            empty_df['_ingestion_timestamp'] = ingestion_timestamp
            print("start_date")
            print(start_date)
            print(type(start_date))
            print("end date")
            print(end_date)
            print(type(end_date))
            empty_df['filter_pay_summary_start_date'] = start_date
            empty_df['filter_pay_summary_end_date'] = end_date
            empty_df.head()

            df = pd.concat([df, empty_df])
            print("Final DF ")
            df.info(verbose=True)
            if (not df.empty):
                print("Write to processed zone")
                processed_writer.s3_to_parquet(df=df, seq_number=seq_number, ingestion_date=ingestion_date, mode="overwrite_partitions", dtypes_col_list=dtypes_col_list)
                print("finished writing to processed zone, writing to redshift")
                processed_writer.redshift_copy(df=df, seq_number=seq_number, ingestion_date=ingestion_date, dtypes_col_list=dtypes_col_list, mode="upsert", primary_keys=["employee_xref_code","position_xref_code","department_xref_code","job_xref_code","pay_code_xref_code","pay_category_xref_code","business_date"])
                print("finished writing to redshift")

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
            'pay_summary_api_url',
            'env',
            'token_api_url',
            'start_date',
            'end_date'
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
        pay_summary_api_url = str(args['pay_summary_api_url']).strip()
        s3_raw_bucket_name = str(args['s3_raw_bucket_name']).strip()
        env = str(args['env']).strip()
        args_start_date = str(args['start_date']).strip()
        args_end_date = str(args['end_date']).strip()

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
    print(actual_rename_mapping_cols)
    dest_cols = table_props.get_dest_columns(table_name=table.lower())
    drop_cols = table_props.get_drop_columns(table_name=table.lower())
    dtypes_col_list = table_props.get_dtypes_columns(table_name=table.lower())
    #  last_update_column = table_props.get_last_update_column(table_name=table.lower())


    if (token is not None):
        print("Start Full Load: "+ str(datetime.now()))
        condition = ""
        #refresh_token()
        run_ingestion()
        print("End Full Load: "+ str(datetime.now()))
    else:
        print("Token is not extracted check secrets")