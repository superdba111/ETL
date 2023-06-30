"""
Main Class , Python Glue Jobs Data Ingestor
"""
import ast
import sys, requests, json, logging, pandas as pd, awswrangler as wr

from botocore.exceptions import ClientError
from datetime import datetime, timedelta

# limit is between 1 and 1000
limit = 1000
local_mode = True
delta_day = 1

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)
pd.set_option('display.float_format', '{:20,.2f}'.format)
pd.set_option('display.max_colwidth', None)

def refresh_token():
    global token, api
    token = None
    api = RestApiClient()
    if api.getZohoCampaignAccessToken(secrets=secrets) is not None:
        token = api.getZohoCampaignAccessToken(secrets=secrets)
    else:
        logging.error("Token is None")

def get_recent_campaigns():

    url = "https://campaigns.zoho.com/api/v1.1/recentcampaigns"

    headers = {
        "Authorization": f"Zoho-oauthtoken {token}"
    }

    parameters = {
        "resfmt": "json"
    }
    from datetime import datetime
    dt = datetime.today()
    data = requests.get(url=url, headers=headers, params=parameters)
    #print(data.text)
    data = data.json()["recent_campaigns"]
    json_data = json.dumps(data)

    keys = json.loads(json_data)
    key_list = []
    for j in keys:
        key_list.append(j["campaign_key"])
        # print("campaign key:")
        # print(j["campaign_key"])
    return key_list

def has_key(key, json_load):
    if key in json_load:
        return True
    else:
        return False
def get_getcampaign_details():

    import requests
    import json

    url = "https://campaigns.zoho.com/api/v1.1/getcampaigndetails"

    headers = {
        "Authorization": f"Zoho-oauthtoken {token}"
    }

    campaign_details = []
    #count = 0
    for j in key_list:
        # print(type(j))
        # print(j)
        # count = count + 1
        # if count == 10:
        #     break
        parameters = {
            "resfmt": "JSON",
            "campaignkey": f"{j}",
            "campaigntype": "abtesting"
        }
        data = requests.get(url=url, headers=headers, params=parameters)
        #json_data = json.dumps(data)
        data.encoding = 'utf-8'
        json_load = data.json()
        campaign_details.append(json_load)

    return campaign_details


def call_writer(table):
    global writer
    writer = Writer(
        bucket_name=bucket_name,
        s3_raw_bucket_name=s3_raw_bucket_name,
        env=env,
        source_name= "zoho_campaign",
        database=database,
        table=table,
        con=con
    )


def sub_table_writer(table_key):
    #global campaign_details_df, key
    call_writer(table_key)
    # add ingestion date as partition date
    campaign_details_df = main_df[table_key].dropna()
    campaign_details_list = campaign_details_df.values.tolist()
    campaign_details_df = pd.DataFrame()
    for e in campaign_details_list:
        # Converting string to list
        res = ast.literal_eval(e)
        campaign_details_list_df = pd.DataFrame(res)
        campaign_details_df = pd.concat([campaign_details_df, campaign_details_list_df])
    campaign_details_df['partition_date'] = pd.to_datetime('today').strftime("%Y-%m-%d")
    campaign_details_df['_ingestion_timestamp'] = ingestion_timestamp
    return campaign_details_df


def write_useragents(df_list, table_key):
    _df = pd.DataFrame(df_list).dropna()
    call_writer(table_key)
    _path = writer.s3_to_json(_df, seq_number, ingestion_date, dtypes_col_list)
    _df = writer.read_json_from_s3(_path)
    # add ingestion date as partition date
    _df['partition_date'] = pd.to_datetime('today').strftime("%Y-%m-%d")
    _df['_ingestion_timestamp'] = ingestion_timestamp
    writer.s3_to_parquet(_df, seq_number, ingestion_date, dtypes_col_list, 'append')
    writer.redshift_copy(_df, seq_number, ingestion_date, dtypes_col_list, writer_mode, [])


if __name__ == "__main__":

    aws_secret_manager_region = "us-east-1"
    bucket_name = 'ingestion-api-test-fuat'
    s3_raw_bucket_name = 'ingestion-api-test-fuat'
    env = 'dev'
    table = "campaign_details"
    secret_name = "dev/zoho_campaign/user/pass/secrets"
    database = "zoho_campaign_test_fuat_db"
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
    key_list = get_recent_campaigns()
    map_data = get_getcampaign_details()

    ingestion_timestamp = pd.to_datetime('now', utc=True).strftime("%Y-%m-%d %H:%M:%S")
    ingestion_date = pd.to_datetime('now', utc=True).strftime("%Y-%m-%d")

    #Set writer mode (str) – Append, overwrite or upsert.
    writer_mode = 'upsert' if not table == 'invoice_data' else 'append'
    #Set redshift connection
    con = wr.redshift.connect(redshift_glue_connector)

    # Get Table Properties.
    # table_props = TableProps()
    # actual_rename_mapping_cols = table_props.get_mapped_columns(table_name=table.lower())
    # drop_cols = table_props.get_drop_columns(table_name=table.lower())
    # # run_mode = table_props.get_mode(table_name=table.lower())
    # dest_col_list = table_props.get_dest_columns(table_name=table.lower())
    # dtypes_col_list = table_props.get_dtypes_columns(table_name=table.lower())
    # last_update_column = table_props.get_last_update_column(table_name=table.lower())
    # primary_keys = table_props.get_primary_keys(table_name=table.lower())

    #**************
    #{'useragentstats': useragentstats_list}
    # raw_json_payload = map_data['useragentstats']
    offset = 0
    seq_number = 0
    flatten_json_data = RawToDF.get_flatten_json_data(map_data)
    main_df = RawToDF.convert_json_to_df(flatten_json_data)

    dtypes_col_list = []
    if (not main_df.empty):

        call_writer('campaign_details_full')
        landing_path = writer.s3_to_json(main_df, seq_number, ingestion_date, dtypes_col_list)
        print(type(landing_path))
        print(landing_path)
        main_df = writer.read_json_from_s3(landing_path)
        # add ingestion date as partition date
        main_df['partition_date'] = pd.to_datetime('today').strftime("%Y-%m-%d")
        main_df['_ingestion_timestamp'] = ingestion_timestamp
        writer.s3_to_parquet(main_df, seq_number, ingestion_date, dtypes_col_list, 'append')
        #writer.redshift_copy(main_df, seq_number, ingestion_date, dtypes_col_list, writer_mode, [])

        #print(main_df.head())
        #writer.redshift_copy(main_df, seq_number, ingestion_date, dtypes_col_list, writer_mode, primary_keys)
        print('Main DF')
        print(main_df.dtypes)

        print('User Agent Stats')
        df_list = main_df['useragentstats'].dropna().values.tolist()
        emailclients_percent_list = []
        browsers_percent_list = []
        tablets_percent_list = []
        mobile_percent_list = []
        computer_percent_list = []
        print(df_list)
        for key in df_list:
            #print(key)
            if (key is not None or key != '<NA>'):
                data_dict = ast.literal_eval(key)
                emailclients_percent = data_dict['emailclients_percent']
                emailclients_percent_list.append(emailclients_percent)
                browsers_percent = data_dict['browsers_percent']
                browsers_percent_list.append(browsers_percent)
                tablets_percent = data_dict['tablets_percent']
                tablets_percent_list.append(tablets_percent)
                mobile_percent = data_dict['mobile_percent']
                mobile_percent_list.append(mobile_percent)
                computer_percent = data_dict['computer_percent']
                computer_percent_list.append(computer_percent)

        write_useragents(emailclients_percent_list, 'emailclients_percent')
        write_useragents(browsers_percent_list, 'browsers_percent')
        write_useragents(tablets_percent_list, 'tablets_percent')
        write_useragents(mobile_percent_list, 'mobile_percent')
        write_useragents(computer_percent_list, 'computer_percent')


        #write campaign-details
        campaign_details_df = sub_table_writer('campaign_details')
        print(campaign_details_df.head())
        writer.s3_to_parquet(campaign_details_df, seq_number, ingestion_date, dtypes_col_list, 'append')
        writer.redshift_copy(campaign_details_df, seq_number, ingestion_date, dtypes_col_list, writer_mode, [])

        #write associated_mailing_lists
        associated_mailing_lists_df = sub_table_writer('associated_mailing_lists')
        print(associated_mailing_lists_df.head())
        writer.s3_to_parquet(associated_mailing_lists_df, seq_number, ingestion_date, dtypes_col_list, 'append')
        writer.redshift_copy(associated_mailing_lists_df, seq_number, ingestion_date, dtypes_col_list, writer_mode, [])

        #write campaign-reports
        campaign_reports_df = sub_table_writer('campaign_reports')
        print(campaign_reports_df.head())
        writer.s3_to_parquet(campaign_reports_df, seq_number, ingestion_date, dtypes_col_list, 'append')
        writer.redshift_copy(campaign_reports_df, seq_number, ingestion_date, dtypes_col_list, writer_mode, [])

        #write campaign-reach
        campaign_reach_df = sub_table_writer('campaign_reach')
        print(campaign_reach_df.head())
        writer.s3_to_parquet(campaign_reach_df, seq_number, ingestion_date, dtypes_col_list, 'append')
        writer.redshift_copy(campaign_reach_df, seq_number, ingestion_date, dtypes_col_list, writer_mode, [])

        # #write campaign_status
        # call_writer('campaign_status')
        # campaign_status_path = writer.s3_to_json(main_df['campaign_status'], seq_number, ingestion_date, dtypes_col_list)
        # campaign_status_df = writer.read_json_from_s3(campaign_status_path)
        # # add ingestion date as partition date
        # campaign_status_df['partition_date'] = pd.to_datetime('today').strftime("%Y-%m-%d")
        # campaign_status_df['_ingestion_timestamp'] = ingestion_timestamp
        # writer.s3_to_parquet(campaign_status_df, seq_number, ingestion_date, dtypes_col_list, 'append')
        # #write segments_info
        # call_writer('segments_info')
        # segments_info_path = writer.s3_to_json(main_df['segments_info'], seq_number, ingestion_date, dtypes_col_list)
        # segments_info_df = writer.read_json_from_s3(segments_info_path)
        # # add ingestion date as partition date
        # segments_info_df['partition_date'] = pd.to_datetime('today').strftime("%Y-%m-%d")
        # segments_info_df['_ingestion_timestamp'] = ingestion_timestamp
        # writer.s3_to_parquet(segments_info_df, seq_number, ingestion_date, dtypes_col_list, 'append')
        # #write campaign-by-location
        # call_writer('campaign_by_location')
        # # add ingestion date as partition date
        # campaign_by_location_df = main_df['campaign_by_location']
        # print(campaign_by_location_df.head())
        # campaign_by_location_df['partition_date'] = pd.to_datetime('today').strftime("%Y-%m-%d")
        # campaign_by_location_df['_ingestion_timestamp'] = ingestion_timestamp
        # campaign_by_location_df = sub_table_writer('campaign_by_location')
        # print(campaign_reach_df.head())
        # writer.s3_to_parquet(campaign_by_location_df, seq_number, ingestion_date, dtypes_col_list, 'append')
        # ********************