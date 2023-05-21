import pytest
from deepdiff import DeepDiff

import common_funcs


tags = {'Env': 'Dev', 'Owner': 'TFProviders'}

table_properties_exclude_paths = [
    "root['CreationDateTime']",
    "root['TableSizeBytes']",
    "root['TableArn']",
    "root['TableId']",
    "root['ItemCount']",
    "root['Replicas']",
    "root['ProvisionedThroughput']['LastIncreaseDateTime']",
    "root['ProvisionedThroughput']['LastDecreaseDateTime']",
    "root['ProvisionedThroughput']['NumberOfDecreasesToday']"
]

lambda_properties_exclude_paths = [
    "root['FunctionArn']",
    "root['CodeSize']",
    "root['RevisionId']",
    "root['LastModified']",
    "root['CodeSha256']",
    "root['RuntimeVersionConfig']"
]


@pytest.fixture()
def resource_config(request):
    return common_funcs.get_resource_config(request.param)


@pytest.fixture()
def client(request):
    return common_funcs.get_client(request.param)


@pytest.mark.parametrize("resource_config, client",
                         [("dynamodb_table_config.json", "dynamodb")],
                         indirect=True)
def test_dynamodb_table(resource_config, client):
    resp = client.describe_table(TableName="DynamoDB-Table")
    diff = DeepDiff(resp["Table"],
                    resource_config,
                    exclude_paths=table_properties_exclude_paths,
                    ignore_order=True)
    assert not diff
    # Tags
    resp = client.list_tags_of_resource(ResourceArn=resp["Table"]["TableArn"])
    assert {tag["Key"]: tag["Value"] for tag in resp["Tags"]} == tags


@pytest.mark.parametrize("resource_config, client",
                         [("lambda_config.json", "lambda")],
                         indirect=True)
def test_lambda_func(resource_config, client):
    resp = client.get_function(FunctionName="lambda-func")
    diff = DeepDiff(resp["Configuration"],
                    resource_config,
                    exclude_paths=lambda_properties_exclude_paths,
                    ignore_order=True)
    assert not diff
    # Tags
    resp = client.list_tags(Resource=resp["Configuration"]["FunctionArn"])
    assert resp["Tags"] == tags


@pytest.mark.parametrize("client", ["sns"], indirect=True)
def test_sns_topic(client):
    topic = "sns-topic"
    resp = client.list_topics()
    topics = {topic["TopicArn"].split(":")[-1]:
              topic["TopicArn"] for topic in resp["Topics"]}
    assert topic in topics
    resp = client.list_subscriptions_by_topic(TopicArn=topics[topic])
    assert len(resp["Subscriptions"]) == 1
    # Tags
    resp = client.list_tags_for_resource(ResourceArn=topics[topic])
    assert {tag["Key"]: tag["Value"] for tag in resp["Tags"]} == tags


@pytest.mark.parametrize("client", ["sqs"], indirect=True)
def test_sqs_queue(client):
    queue = "sqs-queue"
    resp = client.list_queues()
    queues = {queue_url.split("/")[-1]:
              queue_url for queue_url in resp["QueueUrls"]}
    assert queue in queues
    # Tags
    resp = client.list_queue_tags(QueueUrl=queues[queue])
    assert resp["Tags"] == tags


@pytest.mark.parametrize("client", ["logs"], indirect=True)
def test_logs(client):
    log_group = "/aws/lambda/lambda-func"
    resp = client.describe_log_groups()
    log_groups = [group["logGroupName"] for group in resp["logGroups"]]
    assert log_group in log_groups
    # Tags
    resp = client.list_tags_log_group(logGroupName=log_group)
    assert resp["tags"] == tags

