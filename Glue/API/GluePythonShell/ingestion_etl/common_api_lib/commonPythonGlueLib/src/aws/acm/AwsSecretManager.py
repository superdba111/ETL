import json

import boto3
import base64
from botocore.exceptions import ClientError

class AwsSecretManager:

    def __init__(self, region_name = "us-east-1" ):
        self.session = boto3.session.Session()
        self.client = self.session.client(
            service_name='secretsmanager',
            region_name=region_name,
        )

    def get_secret(self,secret_name):
        text_secret_data = ""
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )

        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("The requested secret " + secret_name + " was not found")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                print("The request was invalid due to:", e)
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                print("The request had invalid params:", e)
            elif e.response['Error']['Code'] == 'DecryptionFailure':
                print("The requested secret can't be decrypted using the provided KMS key:", e)
            elif e.response['Error']['Code'] == 'InternalServiceError':
                print("An error occurred on service side:", e)
            else:
                print("An error occurred :", e)
        else:
            # Secrets Manager decrypts the secret value using the associated KMS CMK
            # Depending on whether the secret was a string or binary, only one of these fields will be populated
            if 'SecretString' in get_secret_value_response:
                text_secret_data = get_secret_value_response['SecretString']
            else:
                text_secret_data = get_secret_value_response['SecretBinary']

        return json.loads(text_secret_data)
            # Your code goes here.

