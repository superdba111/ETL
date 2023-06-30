# Description: Export two mv views from Redshift to sftp S3 for external users
# Author: Maxwell Li
# Version: 3.0
# Created Date: May 21, 2022

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
#sc._jsc.hadoopConfiguration().set("fs.s3.maxRetries","20")
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node customers
AuctionActivitySummary_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="data_warehouse",
    redshift_tmp_dir="s3://ftp.edealer.prod.e.inc/temp/",
    table_name="data_warehouse_public_mv_ZOHOCRM_AuctionActivitySummary_All_Fields_AuctionFilter",
    transformation_ctx="customers_node1",
)

ActivitybyAuction_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="data_warehouse",
    redshift_tmp_dir="s3://ftp.edealer.prod.e.inc/temp/",
    table_name="data_warehouse_public_mv_ZOHOCRM_ActivitybyAuction_All_Fields_AuctionFilter",
    transformation_ctx="ActivitybyAuction_node1",
)

AuctionActivitySummary_node1.toDF().write.mode("overwrite").format("json").save("s3://ftp.edealer.prod.e.inc/ZohoCRM/outgoing/json/AuctionActivitySummary/",header='true')
AuctionActivitySummary_node1.toDF().write.mode("overwrite").format("csv").save("s3://ftp.edealer.prod.e.inc/ZohoCRM/outgoing/csv/AuctionActivitySummary/",header='true')

ActivitybyAuction_node1.toDF().write.mode("overwrite").format("json").save("s3://ftp.edealer.prod.e.inc/ZohoCRM/outgoing/json/ActivitybyAuction/",header='true')
ActivitybyAuction_node1.toDF().write.mode("overwrite").format("csv").save("s3://ftp.edealer.prod.e.inc/ZohoCRM/outgoing/csv/ActivitybyAuction/",header='true')

s3_client = boto3.client('s3')

#function to list the objects in an s3
def get_s3_objects(bucket, prefix, suffix):
    """
    Generate objects in an S3 bucket.
    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with this prefix.
     """
    while True:
        # The S3 API response is a large blob of metadata.
        # 'Contents' contains information about the listed objects.
        
        kwargs = {'Bucket': bucket, 'Prefix' : prefix}
        resp = s3_client.list_objects(**kwargs)
        try:
            contents = resp['Contents']
        except KeyError:
            return
        
        for obj in contents:
            key = obj['Key']
            if key.endswith(suffix):
                yield obj
        # The S3 API is paginated, returning up to 1000 keys at a time.
        # Pass the continuation token into the next response, until we
        # reach the final page (when this field is missing).
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break
        
def get_s3_keys(bucket, prefix, suffix):
    """
    Generate the keys in an S3 bucket.
    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix.
    :param suffix: Only fetch keys that end with this suffix.
    """
    for obj in get_s3_objects(bucket, prefix, suffix):
        yield obj['Key']

def rename_files(bucket, prefix,rename_prefix, suffix):
    """
    rename the keys in an S3 bucket.
    :param bucket: Name of the S3 bucket.
    :param prefix: prefix to be used.
    :param suffix: Only fetch keys that end with this suffix.
    """
    files = get_s3_keys(bucket, prefix, suffix) 
    incr=1
    for each in files:
        new_file = prefix + '/' + rename_prefix + str(incr) + suffix 
        print("Copying: ", new_file)
        copy_source = {'Bucket': bucket, 'Key': each}
        s3_client.copy(CopySource = copy_source, Bucket = bucket, Key = new_file)
        s3_client.delete_object(Bucket = bucket, Key = each) 
        incr += 1

bucket_name = 'ftp.edealer.prod.e.inc'
PREFIX_JSON_AuctionActivitySummary ='ZohoCRM/outgoing/json/AuctionActivitySummary'
PREFIX_JSON_ActivitybyAuction ='ZohoCRM/outgoing/json/ActivitybyAuction'
PREFIX_CSV_AuctionActivitySummary ='ZohoCRM/outgoing/csv/AuctionActivitySummary'
PREFIX_CSV_ActivitybyAuction ='ZohoCRM/outgoing/csv/ActivitybyAuction'

rename_files(bucket_name, PREFIX_JSON_AuctionActivitySummary, 'AuctionActivitySummary_', '.json')
rename_files(bucket_name, PREFIX_JSON_ActivitybyAuction, 'ActivitybyAuction_', '.json')
rename_files(bucket_name, PREFIX_CSV_AuctionActivitySummary, 'AuctionActivitySummary_', '.csv')
rename_files(bucket_name, PREFIX_CSV_ActivitybyAuction, 'ActivitybyAuction_', '.csv')

job.commit()
