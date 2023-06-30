"""
Main Class , Python Glue Jobs Data Ingestor
"""

import sys

import awswrangler as wr
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

local_mode = False

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


if __name__ == "__main__":

    aws_secret_manager_region = "us-east-1"
    bucket_name = 'zoho-api-test-fuat'
    table = "accounts"
    secret_name = "dev/zoho/user/pass/secrets"
    database = "zoho_test_fuat_db"
    #select Table columns
    select_cols = "Account_Name, leadslocator__Account_ID,Employees,Ownership, Account_Number, Phone, Fax, Rating,Description"

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


    from commonPythonGlueLib.src.apis.initilizer.initializer import SDKInitializer
    from commonPythonGlueLib.src.apis.initilizer.query.query import Query
    from commonPythonGlueLib.src.aws.acm.AwsSecretManager import AwsSecretManager

    sm = AwsSecretManager(region_name=aws_secret_manager_region)
    secrets = sm.get_secret(secret_name)

    SDKInitializer().initialize(region_name=aws_secret_manager_region, secrets=secrets)
    q = Query()
    query = f"SELECT {select_cols} FROM {table}"
    res = q.get_records(query=query)
    print(res)
    print(type(res))

    flatten_json_data = get_flatten_json_data(res)
    df = convert_json_to_df(flatten_json_data)
    print(df.head())

    print(f'Write date to s3://{bucket_name}/zoho/zoho_{table}/, Database: {database}, Table: {table}')
    wr.s3.to_parquet(
        df=df,
        # path=f's3://{bucket_name}/{filename}',
        path=f's3://{bucket_name}/zoho/zoho_{table}/',
        dataset=True,
        mode="append",
        database=database,
        table=table
    )
