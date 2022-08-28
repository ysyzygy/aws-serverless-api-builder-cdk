import json
import boto3
import time
import os

KEY =  os.environ.get('PARTITION_KEY')
TABLENAME =  os.environ.get('TABLE_NAME')

dynamodb_client = boto3.client("dynamodb")
task_definition_arn = os.environ.get('TASK_DEFINITION_ARN')
cluster_arn = os.environ.get('CLUSTER_ARN')
subnet_ids = os.environ.get('SUBNET_IDS')
SEPARATOR = " "

def lambda_handler(event, context):
    # try:
    print("Incoming event", event)
    resource_id = event["pathParameters"]["resourceId"]
    #1 day
    expiryTimestamp = int(time.time()+3600*24)
    item = get_item(resource_id)
    print("get_item(resource_id)", get_item(resource_id))
    if item is None:
        put_item(resource_id, expiryTimestamp)
    return {
        "statusCode": 201,
        "body": json.dumps({ "status": "Created"})
    }

# insert
def put_item(resource_id: str, expiryTimestamp: int):
    dynamodb = boto3.client('dynamodb')
    item = {
        KEY: {'S': resource_id},
        'ttl': {'N': str(expiryTimestamp)}
    }
    print(item)
    response = dynamodb.put_item(
        TableName=TABLENAME,
        Item=item
    )

    print(response)


def get_item(resource_id: str):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName=TABLENAME,
        Key={
            KEY: {'S': resource_id}
        }
    )

    print(response)

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