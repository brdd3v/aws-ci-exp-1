import boto3
import json
import sys


def get_client(service):
    client = boto3.client(service, 
                          endpoint_url="http://localhost:4566",
                          region_name="eu-central-1",
                          use_ssl=False,
                          verify=False)
    return client


def get_resource_config(filename):
    with open(f"{sys.path[0]}/{filename}", "r") as json_file:
        json_data = json.loads(json_file.read())["Config"]
        return json_data


def delete_logs():
    log_group_name = "/aws/lambda/lambda-func"
    client = get_client(service="logs")
    log_streams_resp = client.describe_log_streams(logGroupName=log_group_name)
    for log_stream in log_streams_resp["logStreams"]:
        client.delete_log_stream(logGroupName=log_group_name,
                                 logStreamName=log_stream["logStreamName"])


def delete_dynamodb_table_items():
    table_name = "DynamoDB-Table"
    client = get_client(service="dynamodb")
    resp = client.scan(TableName=table_name)
    for item in resp["Items"]:
        client.delete_item(TableName=table_name, 
                          Key={"MessageId": item["MessageId"]})


def publish_sample_msg():
    sns_topic = "sns-topic"
    client = get_client(service="sns")
    resp_topics = client.list_topics()
    topic_arn = [topic["TopicArn"] for topic in resp_topics["Topics"] 
                 if topic["TopicArn"].endswith(sns_topic)]

    for i in range(3):
        resp = client.publish(TopicArn=topic_arn[0],
                              Subject="Info",
                              Message=f"Some message-{i}")
        print(f"Message sent (MessageId {resp['MessageId']}")

