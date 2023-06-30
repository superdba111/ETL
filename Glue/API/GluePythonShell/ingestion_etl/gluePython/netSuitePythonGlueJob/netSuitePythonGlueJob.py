import logging
import sys
from datetime import datetime, timedelta

import awswrangler as wr
import pandas as pd

DELTA_DAY = 3

FIRST_INTERVAL_DATE = '2020-09-01 00:00:00'
INTERVAL_DATES_LIST = [
    ('2022-09-01 00:00:00', '2023-01-01 00:00:00'),
    ('2022-05-01 00:00:00', '2022-09-01 00:00:00'),
    ('2022-01-01 00:00:00', '2022-05-01 00:00:00'),
    ('2021-09-01 00:00:00', '2022-01-01 00:00:00'),
    ('2021-06-01 00:00:00', '2021-09-01 00:00:00'),
    ('2021-01-01 00:00:00', '2021-06-01 00:00:00'),
    ('2020-09-01 00:00:00', '2021-01-01 00:00:00')
]
LAST_INTERVAL_DATE = '2023-01-01 00:00:00'


def refresh_token():
    if(use_auth == 'N'):
        global token, api
        token = None
        api = RestApiClient()
        if api.getNetsuiteJdbcAccessToken(secrets=secrets) is not None:
            token = api.getNetsuiteJdbcAccessToken(secrets=secrets)
        else:
            logging.error("Token is None")


def get_file_name():
    from datetime import datetime
    now = datetime.now()
    file_format = 'json'
    file_date = now.strftime(
        "%Y-%m-%d-%H-%M-%S-%f")[:-3]  # [:-3] => Removing the 3 last characters as %f is for millis.
    file_name = f'{file_date}_utc.{file_format}'
    return file_name


def get_source_df(query=''):
    ##Use the CData JDBC driver to read Zoho CRM data from the Accounts table into a DataFrame
    ##Note the populated JDBC URL and driver class name
    conn_string = f"jdbc:ns://{account_id}.connect.api.netsuite.com:1708;ServerDataSource=NetSuite2.com;Encrypted=1;NegotiateSSLClose=false;CustomProperties=(AccountID={account_id};RoleID=1300);"
    if(use_auth == 'N'):
        conn_string = f"jdbc:ns://{account_id}.connect.api.netsuite.com:1708;ServerDataSource=NetSuite2.com;Encrypted=1;NegotiateSSLClose=false;CustomProperties=(AccountID={account_id};RoleID=1300;OAuth2Token={token});"

    if (query):
        return (
            sparkSession.read.format("jdbc")
            .option("url", conn_string)
            .option("user", netsuite_user_email)
            .option("password", netsuite_user_password)
            .option("driver", "com.netsuite.jdbc.openaccess.OpenAccessDriver")
            .option("query", query)
            .load()
        )
    else:
        return (
            sparkSession.read.format("jdbc")
            .option("url", conn_string)
            .option("user", netsuite_user_email)
            .option("password", netsuite_user_password)
            .option("dbtable", table)
            .option("driver", "com.netsuite.jdbc.openaccess.OpenAccessDriver")
            .load()
        )


def write_to_redshift(source_df, mode, primary_keys=[], non_cols=[], dtypes_col_list=[]):
    count_df = source_df.count()
    logger.info(f'{{"Number of rows for {table}": "{count_df}"}}')
    logger.info(f'{{"Show {table}"}}')
    source_df.show()
    if (count_df > 0):
        ##Convert DataFrames to AWS Glue's DynamicFrames Object
        dynamic_dframe = DynamicFrame.fromDF(source_df, glueContext, "dynamic_df")
        # Convert sparkDF to Panda
        df = dynamic_dframe.toDF().toPandas()
        # add ingestion date as partition date
        df['partition_date'] = pd.to_datetime('today').strftime("%Y-%m-%d")
        ingestion_timestamp = pd.to_datetime('now', utc=True).strftime("%Y-%m-%d %H:%M:%S")
        df['_ingestion_timestamp'] = ingestion_timestamp

        if (not df.empty):
            ingestion_date = pd.to_datetime('now', utc=True).strftime("%Y-%m-%d")
            #change type of all null columns to string
            for each_col in non_cols:
                df[each_col] = df[each_col].astype('string')
            logger.info(f'{{"Redshift Write Starting..."}}')
            writer.redshift_copy(df, seq_number=1, ingestion_date=ingestion_date, dtypes_col_list=dtypes_col_list, mode=mode,
                                 primary_keys=primary_keys)
            logger.info(f'{{"Number of rows for {table} ingested": "{len(df.index)}"}}')
            logger.info(f'{{"Redshift Write End..."}}')
    else:
        logger.info(f'{{"Empty DataFrame"}}')
        source_df.show()


if __name__ == "__main__":

    from awsglue.utils import getResolvedOptions
    from awsglue.transforms import *
    from pyspark.context import SparkContext
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame
    from awsglue.job import Job
    from awsglue.dynamicframe import DynamicFrame

    use_auth = 'N'
    args = getResolvedOptions(sys.argv, [
        'JOB_NAME',
        'aws_secret_manager_region',
        'bucket_name',
        'table',
        'secret_name',
        'database',
        'redshift_glue_connector',
        'run_mode',
        's3_raw_bucket_name',
        'env',
        'use_auth'
    ])
    job_name = str(args["JOB_NAME"]).strip()
    aws_secret_manager_region = str(args['aws_secret_manager_region']).strip()
    bucket_name = str(args['bucket_name']).strip()
    table = str(args['table']).strip()
    secret_name = str(args['secret_name']).strip()
    database = str(args['database']).strip()
    redshift_glue_connector = str(args['redshift_glue_connector']).strip()
    run_mode = str(args['run_mode']).strip()
    s3_raw_bucket_name = str(args['s3_raw_bucket_name']).strip()
    env = str(args['env']).strip()
    use_auth = str(args['use_auth']).strip()

    from commonPythonGlueLib.src.aws.acm.AwsSecretManager import AwsSecretManager
    from commonPythonGlueLib.src.apis.rest.RestApiClient import RestApiClient
    from commonPythonGlueLib.src.constants.NetsuiteDDLConstants import NetsuiteDDLConstants
    from commonPythonGlueLib.src.writer.Writer import Writer

    sm = AwsSecretManager(region_name=aws_secret_manager_region)
    secrets = sm.get_secret(secret_name)
    account_id = secrets["netsuite_account_id"]
    netsuite_user_email = secrets["netsuite_user_email"]
    netsuite_user_password = secrets["netsuite_user_password"]
    refresh_token()

    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    sparkContext = SparkContext()
    glueContext = GlueContext(sparkContext)
    sparkSession = glueContext.spark_session
    job = Job(glueContext)
    job.init(job_name, args)

    # Set redshift connection
    con = wr.redshift.connect(redshift_glue_connector)
    # Writer instance
    source_name = 'netsuite'
    if (table == 'transaction_delta'):
        table = 'transaction'
    if (table == 'transactionline_delta'):
        table = 'transactionline'
    writer = Writer(
        bucket_name=bucket_name,
        s3_raw_bucket_name=s3_raw_bucket_name,
        env=env,
        source_name=source_name,
        database=database,
        table=table,
        con=con
    )

    logger.info(f'{{"starting_job": "{args["JOB_NAME"]}"}}')

    constants = NetsuiteDDLConstants()
    src_columns = constants.get_item_src_col(tbl=table)
    redshift_dtypes = constants.get_dtypes(tbl=table)

    jdbc_source = get_source_df()
    jdbc_source_select = jdbc_source
    if(src_columns):
        jdbc_source_select = jdbc_source.select(*src_columns)
    count_jdbc_source = jdbc_source_select.count()
    logger.info(f'{{"Number of rows for {table}": "{count_jdbc_source}"}}')
    jdbc_source_select.show()
    jdbc_source_select.printSchema()

    if (table == 'transactionline' or table == 'transaction'):

        delta_column = 'linelastmodifieddate' if (table == 'transactionline') else "trandate"
        primary_keys = ['uniquekey'] if (table == 'transactionline') else ['id']

        if (run_mode == 'dl'):
            d = datetime.today() - timedelta(days=DELTA_DAY)
            delta = d.strftime("%Y-%m-%d") + ' 00:00:00'
            q_delta = """CAST({} AS INT) >= unix_timestamp('{}', 'yyyy-MM-dd HH:mm:ss')""".format(delta_column, delta)
            df_part_delta = jdbc_source_select.where(q_delta)
            df_part_delta.show()
            logger.info(f'{{"Write Delta {delta_column} >= {delta}"}}')
            # Set writer mode (str) – Append, overwrite or upsert.
            write_to_redshift(source_df=df_part_delta, primary_keys=primary_keys, mode='upsert', dtypes_col_list=redshift_dtypes)
        elif (run_mode == 'fl'):
            jdbc_source_df = jdbc_source_select.persist()
            # Last interval ingest
            query_last_interval = """CAST({} AS INT) >= unix_timestamp('{}', 'yyyy-MM-dd HH:mm:ss')""".format(
                delta_column,
                LAST_INTERVAL_DATE)
            df_part = jdbc_source_df.where(query_last_interval)
            ##Convert DataFrames to AWS Glue's DynamicFrames Object
            d_dframe = DynamicFrame.fromDF(df_part, glueContext, "d_dframe")
            df_cols = d_dframe.toDF().toPandas()
            # list of all columns that are all nulls
            non_cols = df_cols.columns[df_cols.isna().all()].tolist()

            # Out[74]: ['a', 'b']
            logger.info(f'{{"Write Last Interval {delta_column} >= {LAST_INTERVAL_DATE}"}}')
            write_to_redshift(source_df=df_part, primary_keys=primary_keys, mode='overwrite', non_cols=non_cols, dtypes_col_list=redshift_dtypes)

            for dates in INTERVAL_DATES_LIST:
                # between dates interval ingest
                refresh_token()
                query_interval_dates = f"""CAST({delta_column} AS INT) >= unix_timestamp('{dates[0]}', 'yyyy-MM-dd HH:mm:ss')
                AND CAST({delta_column} AS INT) < unix_timestamp('{dates[1]}', 'yyyy-MM-dd HH:mm:ss')"""
                df_part = jdbc_source_df.where(query_interval_dates)
                logger.info(f'{{"Write Interval {delta_column} >= {dates[0]} and {delta_column} < {dates[1]}"}}')
                write_to_redshift(source_df=df_part, primary_keys=primary_keys, mode='upsert', non_cols=non_cols, dtypes_col_list=redshift_dtypes)

            # First interval ingest
            refresh_token()
            query_first_interval = """CAST({} AS INT) < unix_timestamp('{}', 'yyyy-MM-dd HH:mm:ss')""".format(
                delta_column,
                FIRST_INTERVAL_DATE)
            df_part = jdbc_source_df.where(query_first_interval)
            logger.info(f'{{"Write First Interval {delta_column} < {FIRST_INTERVAL_DATE}"}}')
            write_to_redshift(source_df=df_part, primary_keys=primary_keys, mode='upsert', non_cols=non_cols, dtypes_col_list=redshift_dtypes)

        else:
            logger.error(f'{{"Please specify run mode.."}}')
    else:
        ##Convert DataFrames to AWS Glue's DynamicFrames Object
        d_dframe = DynamicFrame.fromDF(jdbc_source_select, glueContext, "d_dframe")
        df_cols = d_dframe.toDF().toPandas()
        # list of all columns that are all nulls
        non_cols = df_cols.columns[df_cols.isna().all()].tolist()
        write_to_redshift(jdbc_source_select, mode='overwrite', non_cols=non_cols)

    job.commit()
