"""
Main Class , Python Glue Jobs Data Ingestor
"""
import logging
import sys

import awswrangler as wr
import pandas as pd
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

# limit is between 1 and 1000
limit = 1000
local_mode = False
delta_day = 1

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)
pd.set_option('display.float_format', '{:20,.2f}'.format)
pd.set_option('display.max_colwidth', None)


def run_ingestion():
    global limit
    offset = 0
    query_result, status_code = api.getNetSuiteRequest(secrets=secrets, built_in_columns=built_in_columns,
                                                       table=table, token=token, limit=limit,
                                                       condition=condition, offset=offset)
    while (query_result is None and status_code == 429):
        print("--------------------------------------")
        print(f"Attempts after status code = 429")
        query_result, status_code = api.getNetSuiteRequest(secrets=secrets, built_in_columns=built_in_columns,
                                                           table=table, token=token, limit=limit,
                                                           condition=condition, offset=offset)
    if (query_result is None):
        print("--------------------------------------")
        print(f"Limit set to 500, after 1. attempt after None result response")
        limit = 500
        query_result = api.getNetSuiteRequest(secrets=secrets, built_in_columns=built_in_columns,
                                              table=table, token=token, limit=limit,
                                              condition=condition, offset=offset)
    if (query_result is None):
        print("--------------------------------------")
        print(f"Limit set to 100, after 2. attempt after None result response")
        limit = 100
        query_result, status_code = api.getNetSuiteRequest(secrets=secrets, built_in_columns=built_in_columns,
                                                           table=table, token=token, limit=limit,
                                                           condition=condition, offset=offset)
    seq_number = 1
    has_more = True
    while has_more:

        if (query_result is not None and has_more):

            try:

                raw_json_payload = query_result['items']

                flatten_json_data = RawToDF.get_flatten_json_data(raw_json_payload)
                df = RawToDF.convert_json_to_df(flatten_json_data)
                # df = RawToDF.convert_json_to_df(raw_json_payload)
                print(df.dtypes)

                # Rename columns
                df = RawToDF.rename_mapped_columns(df=df, column_map=actual_rename_mapping_cols)
                # Drop Columns
                df = RawToDF.drop_columns(df, columns=drop_cols)

                # Create standart DF with fix column size to eliminate column mismatch failure
                empty_df = pd.DataFrame(columns=dest_col_list)

                df = pd.concat([df, empty_df])

                # add ingestion date as partition date
                df['partition_date'] = pd.to_datetime('today').strftime("%Y-%m-%d")
                df['_ingestion_timestamp'] = ingestion_timestamp

                if (not df.empty):
                    landing_path = writer.s3_to_json(df, seq_number, ingestion_date, dtypes_col_list)

                    df = writer.read_json_from_s3(landing_path)

                    writer.s3_to_parquet(df, seq_number, ingestion_date, dtypes_col_list, 'append')

                    print(df.head())

                    writer.redshift_copy(df, seq_number, ingestion_date, dtypes_col_list, writer_mode, primary_keys)
                # writer.redshift_to_sql(df, seq_number, ingestion_date, {})

                has_more = query_result['hasMore']

                if (has_more == True):
                    offset = offset + limit

                    query_result, status_code = api.getNetSuiteRequest(secrets=secrets,
                                                                       built_in_columns=built_in_columns,
                                                                       table=table, token=token, limit=limit,
                                                                       condition=condition, offset=offset)

                    while (query_result is None and status_code == 429):
                        print("--------------------------------------")
                        print(f"Attempts after status code = 429")
                        query_result, status_code = api.getNetSuiteRequest(secrets=secrets,
                                                                           built_in_columns=built_in_columns,
                                                                           table=table, token=token, limit=limit,
                                                                           condition=condition, offset=offset)

                    if (query_result is None):
                        print("--------------------------------------")
                        print(f"1. attempt after None result response")
                        query_result, status_code = api.getNetSuiteRequest(secrets=secrets,
                                                                           built_in_columns=built_in_columns,
                                                                           table=table, token=token, limit=limit,
                                                                           condition=condition, offset=offset)
                    if (query_result is None):
                        print("--------------------------------------")
                        print(f"2. attempt after None result response")
                        query_result, status_code = api.getNetSuiteRequest(secrets=secrets,
                                                                           built_in_columns=built_in_columns,
                                                                           table=table, token=token, limit=limit,
                                                                           condition=condition, offset=offset)
                    if (query_result is None):
                        print("--------------------------------------")
                        print(f"3. attempt after None result response")
                        query_result, status_code = api.getNetSuiteRequest(secrets=secrets,
                                                                           built_in_columns=built_in_columns,
                                                                           table=table, token=token, limit=limit,
                                                                           condition=condition, offset=offset)
                    seq_number = seq_number + 1

                else:
                    print("Has no more Data")
                    break
            except ClientError as e:
                if e.response['Error']['Code'] == 'ExpiredToken':
                    print("Token is expired")
                else:
                    print("Unexpected error: %s" % e)
                break
        else:
            print("Query is empty or None!")
            break


def refresh_token():
    global token, api
    token = None
    api = RestApiClient()
    if api.getNetSuiteAccessToken(secrets=secrets) is not None:
        token = api.getNetSuiteAccessToken(secrets=secrets)
    else:
        logging.error("Token is None")


if __name__ == "__main__":

    aws_secret_manager_region = "us-east-1"
    bucket_name = 'ingestion-api-test-fuat'
    s3_raw_bucket_name = 'ingestion-api-test-fuat'
    env = 'dev'
    table = "item"  # subsidiary,customsegment, currencyrate, currency, "customrecord_csegcseg_eb_bu", "transactionline" #item, subsidiary, classification,account,accounttype, invoice_data
    secret_name = "dev/netsuite/user/pass/secrets"
    database = "netsuite_test_fuat_db"
    redshift_glue_connector = "redshift-fuat"
    run_mode = "fl"
    # condition = "WHERE linelastmodifieddate = '04/02/2020'"
    condition = ""
    start_date = "2022-03-02"
    end_date = "2022-12-31"

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
            'run_mode',
            'start_date',
            'end_date',
            's3_raw_bucket_name',
            'env'
        ])
        aws_secret_manager_region = str(args['aws_secret_manager_region']).strip()
        bucket_name = str(args['bucket_name']).strip()
        table = str(args['table']).strip()
        secret_name = str(args['secret_name']).strip()
        database = str(args['database']).strip()
        redshift_glue_connector = str(args['redshift_glue_connector']).strip()
        run_mode = str(args['run_mode']).strip()
        start_date = str(args['start_date']).strip()
        end_date = str(args['end_date']).strip()
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
    ingestion_date = pd.to_datetime('now', utc=True).strftime("%Y-%m-%d")
    source_name = 'netsuite'

    #Set writer mode (str) – Append, overwrite or upsert.
    writer_mode = 'upsert' if not table == 'invoice_data' else 'append'
    #Set redshift connection
    con = wr.redshift.connect(redshift_glue_connector)
    #Writer instance
    writer = Writer(
        bucket_name=bucket_name,
        s3_raw_bucket_name = s3_raw_bucket_name,
        env = env,
        source_name='netsuite',
        database=database,
        table=table,
        con=con
    )
    # Get Table Properties.
    table_props = TableProps(source_name=source_name)
    actual_rename_mapping_cols = table_props.get_mapped_columns(table_name=table.lower())
    drop_cols = table_props.get_drop_columns(table_name=table.lower())
    # run_mode = table_props.get_mode(table_name=table.lower())
    dest_col_list = table_props.get_dest_columns(table_name=table.lower())
    dtypes_col_list = table_props.get_dtypes_columns(table_name=table.lower())
    last_update_column = table_props.get_last_update_column(table_name=table.lower())
    primary_keys = table_props.get_primary_keys(table_name=table.lower())
    # start_date = table_props.get_start_date(table_name=table.lower())
    # end_date = table_props.get_end_date(table_name=table.lower())

    if (token is not None):

        built_in_columns = table_props.get_built_in_columns(table_name=table.lower())

        if (run_mode == 'il'):
            assert len(
                last_update_column) > 0, "condition column must exist for incremental initial load in tables_props.yml"
            print("Start Initial Load")
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            print('Start Date')
            print(start_date.strftime('%Y-%m-%d'))
            print('----------')
            while (start_date < end_date):
                delta_date = start_date + timedelta(days=delta_day)
                condition = f"WHERE  {last_update_column} BETWEEN TO_DATE( '{start_date.strftime('%Y-%m-%d')}', 'YYYY-MM-DD') AND TO_DATE( '{delta_date.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')"
                if (table == 'transaction'):
                    condition = f"WHERE  {last_update_column} = TO_DATE( '{start_date.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')"
                start_date = delta_date
                print(f"Condition: {condition}")
                run_ingestion()
                refresh_token()

            print('End Date')
            # end_date = start_date + timedelta(days=1)
            #condition = f"WHERE  {last_update_column} BETWEEN TO_DATE( '{start_date.strftime('%Y-%m-%d')}', 'YYYY-MM-DD') AND TO_DATE( '{end_date.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')"
            # if (table == 'transaction'):
            #     condition = f"WHERE  {last_update_column} = TO_DATE( '{start_date.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')"
            # print(f"Condition: {condition}")
            # run_ingestion()
            # last_run_date = pd.to_datetime('today').strftime("%Y-%m-%d")
            data = [str(start_date.strftime('%Y-%m-%d'))]
            status_df = pd.DataFrame(data=data, columns=['last_run_date'])
            writer.s3_to_parquet_status_table(status_df)
            print("End Initial Load")
        elif (run_mode == 'fl'):
            print("Start Full Load")
            condition = ""
            # Create the pandas DataFrame
            run_ingestion()
            refresh_token()
            print("End Full Load")
        elif (run_mode == 'dl'):
            assert len(last_update_column) > 0, "condition column must exist for delta load in tables_props.yml"
            print("Start Delta Load")
            status_df = writer.s3_read_parquet_status_table()
            linelastmodifieddate = str(status_df['last_run_date'].values[0])
            last_run_date = pd.to_datetime('today').strftime("%Y-%m-%d")
            condition = f"WHERE  {last_update_column} BETWEEN TO_DATE( '{linelastmodifieddate}', 'YYYY-MM-DD') AND TO_DATE( '{last_run_date}', 'YYYY-MM-DD')"
            if (table == 'transaction'):
                linelastmodifieddate = datetime.strptime(linelastmodifieddate, '%Y-%m-%d')
                last_run_date = datetime.strptime(last_run_date, '%Y-%m-%d')
                while (linelastmodifieddate < last_run_date):
                    condition = f"WHERE  {last_update_column} = TO_DATE( '{linelastmodifieddate.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')"
                    print(f"Condition: {condition}")
                    delta_date = linelastmodifieddate + timedelta(days=delta_day)
                    linelastmodifieddate = delta_date
                    run_ingestion()
                    refresh_token()
                data = [str(last_run_date.strftime('%Y-%m-%d'))]
                status_df = pd.DataFrame(data=data, columns=['last_run_date'])
                writer.s3_to_parquet_status_table(status_df)
                print("End Delta Load")
            else:
                print(f"Condition: {condition}")
                run_ingestion()
                refresh_token()
                data = [str(last_run_date)]
                status_df = pd.DataFrame(data=data, columns=['last_run_date'])
                writer.s3_to_parquet_status_table(status_df)
                print("End Delta Load")
