import pymongo
import boto3
import base64
from botocore.exceptions import ClientError
import json
from bson import json_util
import logging

def get_secret():

    secret_name = "MdbtoRedshift_partner"                   ## update the secret name
    region_name = "us-east-1"                               ## update the aws region

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
            print e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            print e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            print e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            print e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            print e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            secrets_json = json.loads(secret)
            return (secrets_json['USERNAME'], secrets_json['PASSWORD'], secrets_json['SERVER_ADDR'])
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret

user_name, password, server_addr = get_secret()


def handler(event, context):
    try:
        user_name, password, server_addr = get_secret()

        #Constants
        MONGO_ENDPOINT= "mongodb+srv://{}:{}@{}.mongodb.net/?retryWrites=true&w=majority".format(user_name, password, server_addr)
        REGION_NAME = "us-east-1"           ## update the aws region
        MONGO_DB = "futurebank"            ## update the database name
        MONGO_COL = "counter_party_risk"               ## update the collection name

        logging.debug(event)
        input_fields = event.get("arguments")
        counter_party_id = input_fields.get("counter_party_id")   ## update the field name as per the document to be filtered

        logging.debug(input_fields)
        #Connect to MongoDB Atlas
        client = pymongo.MongoClient(MONGO_ENDPOINT)
        db = client[MONGO_DB]
        
        # Check: Does person already exists
        find_person = db[MONGO_COL].find_one({"counter_party_id": counter_party_id})     ## update the field name as per the document to be filtered
        person_not_exist = find_person is None

        if person_not_exist:
            # Create a new document, and insert to MongoDB Cluster
            result = db[MONGO_COL].insert_one(input_fields)
            return {
                "status" : 201,
                "msg" : "Added to MongoDB Atlas"
            }
        else:
            return {
                "status" : 400,
                "msg" : "Person ID already exists"
            }

    except Exception as e:
        return {
            "status" : 500,
            "msg" : str(e)
        }
