"""
Main Class , Python Glue Jobs Data Ingestor
"""
import json
import logging
import sys

import awswrangler as wr
import pandas as pd
import requests
from botocore.exceptions import ClientError

# limit is between 1 and 1000
limit = 1000
local_mode = True

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def getRefreshToken(secrets):
    # from commonPythonGlueLib.src.aws.acm.AwsSecretManager import AwsSecretManager
    from commonPythonGlueLib.src.apis.rest.RestApiClient import RestApiClient
    # secret_name = "dev/netsuite/secrets"
    rest_api = RestApiClient()

    url = "https://5195388-sb1.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token"

    payload = f'grant_type=refresh_token&refresh_token={secrets["netsuite_refresh_token"]}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Authorization': f'Basic {secrets["netsuite_basic_auth"]}',
        'Authorization': f'Basic {rest_api.get_basic_auth(secrets["netsuite_username"], secrets["netsuite_password"])}',
        'Cookie': 'NS_ROUTING_VERSION=LAGGING'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if (response.status_code == 200):
        # print(response.text)
        return response.json()['access_token']
    else:
        logging.error(f'Response: {response.status_code}')
        return None


def getSubRequest(url):
    headers = {
        'Content-Type': 'application/json',
        'prefer': 'transient',
        'Authorization': f'Bearer {token}',
        'Cookie': 'NS_ROUTING_VERSION=LAGGING'
    }

    print("make request")
    response = requests.request("GET", url, headers=headers)
    if (response.status_code == 200):
        # print(response.text)
        response.encoding = 'utf-8'
        return response.json()
    else:
        return None


def getRequest(table, token, offset=0):
    url = f"https://5195388-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/{table}?limit={limit}&offset={offset}"
    ##url = f"https://5195388-sb1.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql?limit={limit}&offset={offset}"

    ##payload = json.dumps({ "q": f"SELECT * FROM {table}"})

    parameters = """q=lastModifiedDate AFTER "10/20/2020" """
    print(parameters)
    import datetime
    current_day = datetime.date.today()
    print(current_day)
    formatted_date = datetime.date.strftime(current_day, "%m/%d/%Y")
    print(formatted_date)
    headers = {
        'Content-Type': 'application/json',
        'prefer': 'transient',
        'Authorization': f'Bearer {token}',
        'Cookie': 'NS_ROUTING_VERSION=LAGGING'
    }
    #print("make request")
    response = requests.request("GET", url, headers=headers, params=parameters)
    #print(response.json())
    if (response.status_code == 200):
        # print(response.text)
        response.encoding = 'utf-8'
        return response.json()
    else:
        return None


def convert_json_to_df(json):
    """
    Convert json data to DataFrame
    :param json: json input
    :return: dataframe
    """
    # flattened_json  = [x for x in json]
    flattened_json = json
    df_json = pd.DataFrame(flattened_json)
    return df_json


def get_flatten_json_data(json_data):
    """
    Flatten the nested Json Data
    :param json_data: input nasted json response
    :param table_name: table input for custom fields.
    :return: the flatten json data
    """
    flatten_json_data = []
    # c_fields = get_table_custom_fields(table_name)
    try:
        json_list = json_data  # ['result']

        for json_element in json_list:
            if len(json_element) > 0:
                flatten_json = {}
                for key in json_element:
                    flatten_json = {**flatten_json, **{str(key): str(json_element[key])}}

                flatten_json_data.append(flatten_json)
    except Exception as e:
        print(f"Error  {e}. ")

    return flatten_json_data

if __name__ == "__main__":

    aws_secret_manager_region = "us-east-1"
    bucket_name = 'ingestion-api-test-fuat'
    #table = "CashRefund"
    tables = [
           "CashRefund",
           "CreditMemo",
           # "Invoice", #very large
           "PurchaseOrder",
           "SalesOrder",
           "VendorBill",
           "VendorCredit",
           "VendorPayment"
    ]
    secret_name = "dev/netsuite/user/pass/secrets"
    database = "netsuite_test_fuat_db"
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
            'database'
        ])
        aws_secret_manager_region = str(args['aws_secret_manager_region']).strip()
        bucket_name = str(args['bucket_name']).strip()
        table = str(args['table']).strip()
        secret_name = str(args['secret_name']).strip()
        database = str(args['database']).strip()


    from commonPythonGlueLib.src.apis.rest.RestApiClient import RestApiClient
    from commonPythonGlueLib.src.aws.acm.AwsSecretManager import AwsSecretManager
    # secret_name = "dev/netsuite/secrets"


    # secret_name = "dev/netsuite/secrets"

    sm = AwsSecretManager(region_name=aws_secret_manager_region)
    secrets = sm.get_secret(secret_name)

    token = None
    if (getRefreshToken(secrets=secrets) is not None):
        token = getRefreshToken(secrets=secrets)
    else:
        logging.error("Token is None")

    if (token is not None):
        offset = 0
        records = []
        for table in tables:
            offset = 0
            query_result = getRequest(table=table, token=token, offset=offset)
            # print("Query Result")
            # print(query_result)
            seq_number = 1
            has_more = True
            con = wr.redshift.connect("redshift-fuat")
            while has_more:

                if (query_result is not None and has_more):

                    try:
                        json_data = query_result['items']
                        # print("Items")
                        # print(json_data)

                        flatten_json_data = get_flatten_json_data(json_data)
                        df = convert_json_to_df(flatten_json_data)


                        #drop links
                        df = df.drop(columns=['links'])

                        #rename columns
                        #df = df.rename(columns={"links": "urls", "id": "id"})
                        # print(df.head(5))
                        # print(seq_number)
                        # print(json_data)

                        #add ingestion date as partition date
                        df['table_name'] = str(table)
                        df['partition_date'] = pd.to_datetime('today').strftime("%Y%m%d")
                        #print(df.head(100))
                        print(f'Count: {seq_number}')
                        print(df[df.columns[0]].count())

                        print(
                            f'Write seq_number:{seq_number} data to s3://{bucket_name}/netsuite/netsuite_record_{table}/, Database: {database}, Table: record_{table}')

                        wr.s3.to_json(
                            df=df,
                            path=f's3://{bucket_name}/netsuite/netsuite_record_{table}/record_{table}_{seq_number}.json',

                        )

                        print("read readshift")

                        wr.redshift.copy(
                            df=df,
                            path=f's3://{bucket_name}/netsuite/netsuite_record_{table}/record_{table}_{seq_number}.json',
                            con=con,
                            schema=database,
                            table=table,
                            mode="upsert",
                            #iam_role=iam_role,
                            primary_keys=["id","table_name"]
                        )

                        df = wr.redshift.read_sql_table(table="my_table", schema="public", con=con)
                        df.head()

                        # with con.cursor() as cursor:
                        #     cursor.execute('SELECT * FROM netsuite_test_fuat_db.public.test_table')
                        #     print(cursor.fetchall())
                        #
                        # df = wr.redshift.read_sql_query(
                        #     sql='SELECT * FROM "dev"."public"."test_fuat"',
                        #     con=con
                        # )
                        # df.head()

                        # df = wr.redshift.read_sql_table(
                        #     table='"public"."test_fuat"',
                        #     schema="dev",
                        #     con=con
                        # )

                        print('write to redshift')

                        # wr.redshift.to_sql(
                        #     df=df,
                        #     table=f'netsuite_record_{table}',
                        #     schema=f'{database}',
                        #     con=con
                        # )


                        # wr.s3.to_parquet(
                        #     df=df,
                        #     # path=f's3://{bucket_name}/{filename}',
                        #     path=f's3://{bucket_name}/netsuite/netsuite_record_{table}/',
                        #     dataset=True,
                        #     # partition_cols="partition_date",
                        #     mode="append",
                        #     database=database,
                        #     table=f'record_{table}'
                        # )


                        # for l in json_data:
                        #     #print("level 2 extraction ")
                        #     url_list = l['links']
                        #     id = l['id']
                        #     url = l['links'][0]['href']
                        #
                        #     #response2 = getSubRequest(url)
                        #
                        #     from datetime import datetime
                        #
                        #     dt = datetime.today()
                        #     # out_data = json.dumps(response2)
                        #     # print("Respose 2")
                        #     # print(out_data)
                        #     from commonPythonGlueLib.src.aws.s3.S3BucketService import S3BucketService

                            #s3BucketService = S3BucketService(bucket_name="landing.datalake.reporting-dev.e.inc")
                            #s3BucketService.write_to_s3(out_data, f"netsuite/{table}/{id}.json")
                            # print("completed write to landing")
                        has_more = query_result['hasMore']
                        if (has_more == True):
                            offset = offset + limit
                            query_result = getRequest(table=table, token=token, offset=offset)
                            # print("Query Result")
                            # print(query_result)
                            seq_number = seq_number + 1

                            if (seq_number % 99 == 0):
                                if (getRefreshToken(secrets=secrets) is not None):
                                    token = getRefreshToken(secrets=secrets)
                                else:
                                    logging.error("Access token is None")
                            # if (seq_number == 1000):
                            #     seq_number = 1
                        else:
                            con.close()
                            break
                        print(has_more)
                    except ClientError as e:
                        if e.response['Error']['Code'] == 'ExpiredToken':
                            print("Token is expired")
                        else:
                            print("Unexpected error: %s" % e)
                            con.close()
                        break
                else:
                    print("Query is empty or None!")
                    con.close()
                    break