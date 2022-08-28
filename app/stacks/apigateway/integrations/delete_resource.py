import json
import boto3
import os


KEY =  os.environ.get('PARTITION_KEY')
TABLENAME =  os.environ.get('TABLE_NAME')
dynamodb_client = boto3.client("dynamodb")
SEPARATOR = " "


def lambda_handler(event, context):
    session_id = event["pathParameters"]["sessionId"]
    delete_item(session_id)
    return {
        "statusCode": 204
    }



# insert
def delete_item(session_id: str):
    dynamodb = boto3.client('dynamodb')

    response = dynamodb.delete_item(
        TableName=TABLENAME,
        Key={'session_id': {'S': session_id}}
    )
    print(response)


def get_item(session_id: str):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName=TABLENAME,
        Key={
            KEY: {'S': session_id}
        }
    )
    if 'Item' in response:
        print("response['Item']", response['Item'])
        return response['Item']
    else:
        return None


def exception_handler(status_code, msg):
    # exception to status code mapping goes here...
    error_json = {"message": msg}
    return {
        'statusCode': status_code,
        'body': json.dumps(error_json)
    }