from __future__ import print_function

import boto3
#import json
import os

print('Loading function')

# set up client connection to DynamoDB outside of lambda_handler using an environment variable - this will speed up future calls by not reinitializing dynamo connections every time
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['lap_count_table'])
# this is my IoT button DSN
deviceId = os.environ['button_dsn']

def lambda_handler(event, context):
    # check to see if this event is from an IoT button press
    if 'clickType' in event:
        # create dynamoDB connection
        # is it a single press? if so, increment the lap counter
        # need to handle case where this is the first time someone is adding a record
        if event['clickType'] == 'SINGLE':
            print("this is a single press - need to increment the lap count")
            response = table.get_item(
                Key={
                    'deviceId': deviceId
                }
            )
            # check to see if the deviceId exists in the DynamoDB table; if not, create a new entry
            if 'Item' in response:
                print("Item to be updated: " + str(response['Item']))
                table.update_item(
                    Key={
                        'deviceId': deviceId
                    },
                    UpdateExpression='SET lapCount = :val1',
                    ExpressionAttributeValues={
                        ':val1': int(response['Item']['lapCount']) + 1
                    }
                )
            else:
                print("Not in table - adding new entry")
                table.put_item(
                   Item={
                        'deviceId': deviceId,
                        'lapCount': 1
                    }
                )

        # if not, reset the lap counter
        else:
            print("this is a double press (or maybe a long press), so reset the lap count")
            response = table.get_item(
                Key={
                    'deviceId': deviceId
                }
            )
            # check to see if the deviceId exists in the DynamoDB table; if not, do nothing
            if 'Item' in response:
                print("Item to be updated: " + str(response['Item']))
                table.update_item(
                    Key={
                        'deviceId': deviceId
                    },
                    UpdateExpression='SET lapCount = :val1',
                    ExpressionAttributeValues={
                        ':val1': 0
                    }
                )
    else:
        # event coming from somewhere else, so just log it and ignore
        print("Not an IoT Button event!")
    return 'Function complete'
