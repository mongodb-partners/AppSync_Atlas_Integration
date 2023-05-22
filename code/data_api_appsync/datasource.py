import pymongo
import requests
import json
import boto3
import base64
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "lambda_appync_partner"       ## update to the secret name 
    region_name = "us-east-1"                   ## update to the AWS region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)['API_KEY']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            

def handler(event, context):
    '''
    Handler function for using Atlas Data API in AppSync Lambda resolver
    '''
    try:
        #URL endpoint to the Atlas
        url = "https://data.mongodb-api.com/app/data-pwazq/endpoint/data/v1/action/findOne"         ## update to the data api endpoint
        #Reading the arguments
        feilds = event.get("arguments")
        id = feilds.get("product_id")                  ## update the field according to the query functions (if required)
        #Fabricating payload for end-point call
        payload = json.dumps({
            "collection": "Details",                    ## update the collection name
            "database": "Hotels",                       ## update the Database name
            "dataSource": "PartnerSagemaker",           ## update the datasource name
            #Can include multiple filters based on arguments received 
            "filter": {
                "product_id": id
            },
        })
        #Adding necessary headers for API call
        headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': get_secret(), 
        }
        #Make the API call
        response = requests.request("POST", url, headers=headers, data=payload)
        #Return document data from the response of the API call
        print(">> Response : ", type(response))
        return response.json()['document']
    except Exception as e:
        print(">> Exception : {}".format(e))
        return None

handler({"arguments": {"product_id" : "P01"}}, {})              ## update the field and sample value accordingly to the document value to be queried
