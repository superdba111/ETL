import boto3
import json
from datetime import datetime

class S3BucketService:
    def __init__(self, bucket_name):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket_name

    def generate_raw_filename(self, source_name, table_name, environment, seq_number, upload_time, load_type,
                              file_format):
        """
        Generate correct raw file name

        Parameters
        ----------
        source_name : name of the destination source
        table_name : name of table
        environment : current environment
        seq_number : sequence number
        upload_time : upload time (datetime object)
        load_type : fl | il | dl
        file_format : extension of a file

        Returns
        ----------
        string:Correct raw bucket object name
        """
        file_date = upload_time.strftime(
            "%Y-%m-%d-%H-%M-%S-%f")[:-3]  # [:-3] => Removing the 3 last characters as %f is for millis.
        res = f'{source_name}/{source_name}_{table_name}/' \
              f'{source_name}_{environment}_{table_name}_{str(seq_number).zfill(3)}_' \
              f'{file_date}_utc_{load_type}.{file_format}'
        res = res.lower()

        # Check if no illegal chars were passed
        #test = FileNameStandardConvention(res)
        #test.check_naming_convention()
        return res




    # json_object = [{'leadslocator__Account_ID': None, 'Account_Name': 'Benton (Sample)', 'id': 4776181000000457200}, {'leadslocator__Account_ID': None, 'Account_Name': 'Chanay (Sample)', 'id': 4776181000000457201}, {'leadslocator__Account_ID': None, 'Account_Name': 'Chemel (Sample)', 'id': 4776181000000457202}, {'leadslocator__Account_ID': None, 'Account_Name': 'Feltz Printing Service (Sample)', 'id': 4776181000000457203}, {'leadslocator__Account_ID': None, 'Account_Name': 'Printing Dimensions (Sample)', 'id': 4776181000000457204}, {'leadslocator__Account_ID': None, 'Account_Name': 'Chapman (Sample)', 'id': 4776181000000457205}, {'leadslocator__Account_ID': None, 'Account_Name': 'Morlong Associates (Sample)', 'id': 4776181000000457206}, {'leadslocator__Account_ID': None, 'Account_Name': 'Commercial Press (Sample)', 'id': 4776181000000457207}, {'leadslocator__Account_ID': None, 'Account_Name': 'Truhlar And Truhlar (Sample)', 'id': 4776181000000457208}, {'leadslocator__Account_ID': None, 'Account_Name': 'King (Sample)', 'id': 4776181000000457209}, {'leadslocator__Account_ID': None, 'Account_Name': 'test', 'id': 4776181000000638027}]
    #
    # filename = generate_raw_filename(source_name='zoho', table_name='accounts', environment='testenv',seq_number=1,load_type='dl', file_format='json', upload_time=datetime.now())
    #
    # bucket_name = 'zoho-api-test-fuat'


    def write_to_s3(self, json_object, filename):
        s3object = self.s3.Object(self.bucket_name, filename)
        print(f'Writing file to s3://{self.bucket_name}/{filename}')
        print(f'Json Object {json_object}')
        print(f'Json Object {json.dumps(json_object)}')
        self.s3.Object(self.bucket_name, filename).put(Body=json_object)
        # s3object.put(
        #     #Body=(bytes(json.dumps(json_object).encode('UTF-8-SIG')))
        #     Body = (bytes(json.dumps(json_object).encode('UTF-8-SIG')))
        # )

    # write_to_s3(json_object, filename)

    # for bucket in s3.buckets.all():
    #     print(bucket)