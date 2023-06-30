import awswrangler as wr
from datetime import datetime

import awswrangler as wr


class Writer:

    def __init__(self, bucket_name, s3_raw_bucket_name, env, source_name, database, table, con,
                 job_status_table='jobstatus_'):
        # df = df
        self.bucket_name = bucket_name
        self.s3_raw_bucket_name = s3_raw_bucket_name
        self.env = env
        self.database = database
        self.table = 'business_unit' if table == 'customrecord_csegcseg_eb_bu' else table
        self.table = 'vehicle' if table == 'CUSTOMRECORD_VEHICLE_SELECTION' else table
        # ingestion_date = ingestion_date
        # seq_number = seq_number
        self.con = con
        self.source_name = source_name
        self.job_status_table = job_status_table + table

    def s3_to_json(self, df, seq_number, ingestion_date, dtypes_col_list):
        file_name = self._get_file_name()
        path = f's3://{self.s3_raw_bucket_name}/{self.env}/{self.source_name}/raw/{self.source_name}_record_{self.table}/{ingestion_date}/record_{self.table}_{seq_number}_{file_name}'
        print(
            f'Write json raw data {seq_number} data to s3://{self.s3_raw_bucket_name}/{self.env}/{self.source_name}/raw/{self.source_name}_record_{self.table}/{ingestion_date}/record_{self.table}_{seq_number}_{file_name} '
        )
        wr.s3.to_json(
            df=df,
            path=path,
            #dtype=dtypes_col_list

        )
        return path
    def s3_to_json_basic(self, df, seq_number, ingestion_date):

        file_name = self._get_file_name()
        print(
            f'Write json raw data {seq_number} data to s3://{self.bucket_name}/{self.source_name}/raw/{self.source_name}_record_{self.table}/{ingestion_date}/record_{self.table}_{seq_number}_{file_name} '
        )
        wr.s3.to_json(
            df=df,
            path=f's3://{self.bucket_name}/{self.source_name}/{self.env}/{self.source_name}_record_{self.table}/{ingestion_date}/record_{self.table}_{seq_number}_{file_name}'
        )

    def _get_file_name(self):
        now = datetime.now()
        file_format = 'json'
        file_date = now.strftime(
            "%Y-%m-%d-%H-%M-%S-%f")[:-3]  # [:-3] => Removing the 3 last characters as %f is for millis.
        file_name = f'{file_date}_utc.{file_format}'
        return file_name

    def read_json_from_s3(self, path):
        #df = wr.s3.read_json(path=[path], dataset=True)
        df = wr.s3.read_json(path)
        return df

    def s3_to_parquet(self, df, seq_number, ingestion_date, dtypes_col_list, mode):
        print(
            f'Write seq_number:{seq_number} data to s3://{self.bucket_name}/{self.env}/{self.source_name}/{self.source_name}_{self.table}/, Database: {self.database}, Table: {self.table}'
        )
        wr.s3.to_parquet(
            df=df,
            # path=f's3://{bucket_name}/{filename}',
            path=f's3://{self.bucket_name}/{self.env}/{self.source_name}/{self.source_name}_{self.table}/',
            dataset=True,
            partition_cols=["partition_date"],
            mode=mode,
            database=self.database,
            table=self.table,
            dtype=dtypes_col_list
        )

    def redshift_copy(self, df, seq_number, ingestion_date, dtypes_col_list, mode, primary_keys):
        s3_path = f's3://{self.bucket_name}/{self.env}/{self.source_name}/raw/{self.source_name}_record_{self.table}_redshift_tmp/'
        print(
            f'Write Redshift Copy to {s3_path}'
            f'to database:{self.database}, table: {self.table}')

        wr.s3.delete_objects(s3_path[:-1])
        wr.redshift.copy(
            df=df,
            path=s3_path,
            con=self.con,
            schema=self.database,
            table=self.table,
            mode=mode,
            varchar_lengths_default=10000,
            dtype=dtypes_col_list,
            use_column_names=True,
            # iam_role=iam_role,
            primary_keys=primary_keys
        )

    def redshift_to_sql(self, df, seq_number, ingestion_date, dtypes_col_list):
        s3_path = f's3://{self.bucket_name}/{self.env}/{self.source_name}/raw/{self.source_name}_record_{self.table}_redshift_tmp/'
        print(
            f'Write Redshift Copy to {s3_path}'
            f'to database:{self.database}, table: {self.table}')

        # wr.s3.delete_objects(s3_path[:-1])
        wr.redshift.to_sql(
            df=df,
            # path=s3_path,
            con=self.con,
            schema=self.database,
            table=self.table,
            mode="append",
            varchar_lengths_default=10000,
            dtype=dtypes_col_list,
            use_column_names=True
            # iam_role=iam_role,
            # primary_keys=["id", "table_name"]
        )

    def s3_read_parquet_status_table(self):
        df = wr.s3.read_parquet_table(
            database=self.database,
            table=self.job_status_table
        )
        return df

    def s3_to_parquet_status_table(self, df):
        print(
            f'Write status data to s3://{self.bucket_name}/{self.env}/{self.source_name}/{self.source_name}_{self.job_status_table}/, Database: {self.database}, Table: {self.job_status_table}'
        )
        wr.s3.to_parquet(
            df=df,
            # path=f's3://{bucket_name}/{filename}',
            path=f's3://{self.bucket_name}/{self.env}/{self.source_name}/{self.source_name}_{self.job_status_table}/',
            dataset=True,
            mode="overwrite",
            database=self.database,
            table=self.job_status_table
        )
