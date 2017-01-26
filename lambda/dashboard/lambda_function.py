from __future__ import print_function

import boto3
import json
import os

print('Loading function')

# set up client connection to DynamoDB outside of lambda_handler using an environment variable
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['lap_count_table'])
# this is my IoT button DSN
deviceId = os.environ['button_dsn']

def lambda_handler(event, context):

    response = table.get_item(
    Key={
        'deviceId': deviceId
        }
    )
    if 'Item' in response:
        item = response['Item']
        # cast the count as an int, not a decimal, so we can dumps it
        print(item)
        item['lapCount'] = int(item['lapCount'])
        # just going to hardcode statusCode & headers for now
        return {
            'statusCode': '200',
            'body': json.dumps(item),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
        }
    else:
        print("Item not found in table, so returning dummy data")
        item = {"lapCount": 0, "deviceId": deviceId}
        return {
            'statusCode': '200',
            'body': json.dumps(item),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
        }
