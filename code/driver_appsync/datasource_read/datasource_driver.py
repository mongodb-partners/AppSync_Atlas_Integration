import pymongo
import boto3
import base64
from botocore.exceptions import ClientError
import json
from bson import json_util

def get_secret():

    secret_name = "lambda_appync_partner"               ## update the secret name
    region_name = "us-east-1"                           ## update the aws region

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
            secrets_json = json.loads(secret)
            return (secrets_json['USER_NAME'], secrets_json['PASSWORD'], secrets_json['SERVER_ADDR'])
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret

def modify_format(data):
    # json_res = json.dumps(result,default=json_util.default)
    # return json.loads(json_res)
    data = json_util.dumps(data)
    mod_data = json.loads(data)
    return mod_data
    
def handler(event, context):
    try:
        user_name, password, server_addr = get_secret()

        #Constants
        MONGO_ENDPOINT= "mongodb+srv://{}:{}@{}.mongodb.net/?retryWrites=true&w=majority".format(user_name, password, server_addr)
        REGION_NAME = "us-east-1"       ## update the aws region
        MONGO_DB = "Credit_Risk"        ## update the database name
        MONGO_COL = "Details"           ## update the collection name

        feilds = event.get("arguments")
        id = feilds.get("person_id")    ## update the field according to the document to be queried
        #Connect to MongoDB Atlas
        client = pymongo.MongoClient(MONGO_ENDPOINT)
        db = client[MONGO_DB]
        #find one query
        result = db[MONGO_COL].find_one({"person_id": id})
        modified_result = modify_format(result)
        return modified_result
    
    except Exception as e:
        return {
            "status" : 400,
            "msg" : str(e)
        }
