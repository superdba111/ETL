import datetime
import json
import logging
import sys
import time
import zipfile
from io import BytesIO

import awswrangler as wr
import pandas as pd
import requests

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)
pd.set_option('display.float_format', '{:20,.2f}'.format)
pd.set_option('display.max_colwidth', None)

local_mode = False


def refresh_token():
    global token, api
    token = None
    api = RestApiClient()
    if api.getZohoAccessToken(secrets=secrets) is not None:
        token = api.getZohoAccessToken(secrets=secrets)
    else:
        logging.error("Token is None")


def createZohoBulkExportJob(token, module, page=1):
    """
    Get API calls for data ingestion

    Parameters
    ----------
    expanders: additional columns to add based on documentation
    xref_string: List of xrefs to pull as a single string comma separated
    Returns
    ----------
    response: json response of API
    """
    # url = "https://www.zohoapis.com/crm/bulk/v3/read"
    payload = json.dumps({
        "query": {
            "module":
                {
                    "api_name": module
                }
            #            "module" : "Accounts"
        },
        "page": page
    }
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Zoho-oauthtoken {token}'
    }
    print(f"Url request: {url}")
    response = requests.request("POST", url,
                                headers=headers,
                                data=payload)
    response.encoding = 'utf-8'
    print(response)
    response_json = response.json()
    print(response_json)
    print(response.status_code)
    json_object = json.dumps(response_json)

    job_id = response_json['data'][0]['details']['id']
    return job_id


def createZohoDownloadResponse(token, job_id):

    status_download_url = url + "/" + job_id
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Zoho-oauthtoken {token}'
    }
    more_records = False
    while True:
        status_response = requests.request("GET",
                                           status_download_url,
                                           headers=headers)
        state = status_response.json()['data'][0]['state']
        if state == 'COMPLETED':
            more_records = status_response.json()['data'][0]['result']['more_records']
            break
        else:
            print("Status" + " as of " + str(datetime.datetime.now()) + " : " + state)

        time.sleep(5)
    headers = {
        'Authorization': f'Zoho-oauthtoken {token}'
    }
    status_download_url = url + "/" + job_id + "/result"

    response = requests.get(url=status_download_url, stream=True, headers=headers)

    return response, more_records


def get_csv_df(response):
    filebytes = BytesIO(response.content)
    myzipfile = zipfile.ZipFile(filebytes)
    df_list = list()
    for file_name in myzipfile.namelist():
        print(file_name)
        foofile = myzipfile.open(name=file_name)
        df_csv = pd.read_csv(foofile)
        df_list.append(df_csv)
    return df_list

def call_writer(table):
    global writer
    writer = Writer(
        bucket_name=bucket_name,
        s3_raw_bucket_name=s3_raw_bucket_name,
        env=env,
        source_name="zoho_crm",
        database=database,
        table=table,
        con=con
    )


if __name__ == "__main__":

    aws_secret_manager_region = "us-east-1"
    bucket_name = 'ingestion-api-test-fuat'
    tables = """Accounts,Contacts,zrouteiqzcrm__Routes,Dealer_Discount_Requests,fusion__SMS_Messages,Territory_Assigments,Dealer_Applications,Leads,Subform_1"""
    secret_name = "dev/zoho/user/pass/secrets"
    database = "zoho_crm_test_db"
    s3_raw_bucket_name = 'ingestion-api-test-fuat'
    env = 'dev'
    redshift_glue_connector = "redshift-fuat"

    # select Table columns
    url = "https://www.zohoapis.com/crm/bulk/v4/read"
    # True when running on local computer-requires executing python3 aws_pmi.py, otherwise False
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
            's3_raw_bucket_name',
            'env',
            'redshift_glue_connector'
        ])
        aws_secret_manager_region = str(args['aws_secret_manager_region']).strip()
        bucket_name = str(args['bucket_name']).strip()
        tables = str(args['table']).strip()
        secret_name = str(args['secret_name']).strip()
        database = str(args['database']).strip()
        s3_raw_bucket_name = str(args['s3_raw_bucket_name']).strip()
        env = str(args['env']).strip()
        redshift_glue_connector = str(args['redshift_glue_connector']).strip()

    from commonPythonGlueLib.src.aws.acm.AwsSecretManager import AwsSecretManager
    from commonPythonGlueLib.src.aws.acm.AwsSecretManager import AwsSecretManager
    from commonPythonGlueLib.src.transform.TableProps import TableProps
    from commonPythonGlueLib.src.writer.Writer import Writer
    from commonPythonGlueLib.src.apis.rest.RestApiClient import RestApiClient

    sm = AwsSecretManager(region_name=aws_secret_manager_region)
    secrets = sm.get_secret(secret_name)

    ingestion_timestamp = pd.to_datetime('now', utc=True).strftime("%Y-%m-%d %H:%M:%S")
    ingestion_date = pd.to_datetime('now', utc=True).strftime("%Y-%m-%d")
    source_name = 'zohocrm'

    table_props = TableProps(source_name=source_name)

    # Set writer mode (str) – Append, overwrite or upsert.

    # Set redshift connection
    con = wr.redshift.connect(redshift_glue_connector)
    tables_list = tables.strip().split(',')
    # Writer instance
    for table in tables_list:
        print(table)
        dtypes_col_list = table_props.get_dtypes_columns(table_name=table)
        print(dtypes_col_list)
        primary_keys = table_props.get_primary_keys(table_name=table)
        print(primary_keys)
        call_writer(table)
        writer_mode = 'upsert' if not table == 'invoice_data' else 'append'
        seq_number = 1
        # dtypes_col_list = []
        primary_keys = []
        more_records = True
        page = 1
        while (more_records):
            refresh_token()
            job_id = createZohoBulkExportJob(token=token, module=table, page=page)
            response, more_records = createZohoDownloadResponse(token=token, job_id=job_id)
            df_list = get_csv_df(response)
            for each_df in df_list:
                print(each_df.head())

                each_df['partition_date'] = pd.to_datetime('today').strftime("%Y-%m-%d")
                each_df['_ingestion_timestamp'] = ingestion_timestamp

                if (not each_df.empty):
                    landing_path = writer.s3_to_json(each_df, seq_number, ingestion_date, dtypes_col_list)

                    each_df = writer.read_json_from_s3(landing_path)

                    print(f'******** {table} ************')
                    print(each_df.dtypes)
                    # overwrite
                    # writer.s3_to_parquet(df, seq_number, ingestion_date, dtypes_col_list, 'append')
                    # overwrite is only for page = 1, else it should be append or upsert with primary_keys, so that not overwrite.
                    writer.s3_to_parquet(each_df, seq_number, ingestion_date, dtypes_col_list, 'overwrite')

                    # print(each_df.head())

                    writer.redshift_copy(each_df, seq_number, ingestion_date, dtypes_col_list, mode='upsert',
                                         primary_keys=primary_keys)
                    seq_number = seq_number + 1
            page = page + 1
