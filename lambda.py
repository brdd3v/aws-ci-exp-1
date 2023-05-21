import boto3
import os


if 'LOCALSTACK_HOSTNAME' in os.environ:
    dynamodb = boto3.resource('dynamodb',
                              endpoint_url=f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566",
                              region_name="eu-central-1")
else:
    dynamodb = boto3.resource('dynamodb',
                              region_name="eu-central-1")


def handler(event, context):
    table = dynamodb.Table('DynamoDB-Table')
    for msg in event['Records']:
        try:
            table.put_item(
                Item = {
                    'MessageId': msg['messageId'],
                    'QueueName': msg['eventSourceARN'].split(':')[-1],
                    'Message': msg['body']
                }
            )
        except Exception as e:
            print(e)

