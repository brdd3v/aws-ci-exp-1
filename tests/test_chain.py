import time
import pytest

import common_funcs


@pytest.fixture()
def client(request):
    return common_funcs.get_client(request.param)


@pytest.fixture()
def load_sample_data():
    common_funcs.publish_sample_msg()  # sns -> sqs -> lambda -> dynamodb


def setup_function(function):
    common_funcs.delete_dynamodb_table_items()


@pytest.mark.parametrize("client", ["dynamodb"], indirect=True)
def test_dynamodb_no_data(client):
    resp = client.scan(TableName="DynamoDB-Table")
    assert len(resp["Items"]) == 0


@pytest.mark.parametrize("client", ["dynamodb"], indirect=True)
@pytest.mark.usefixtures("load_sample_data")
def test_dynamodb_data(client):
    time.sleep(5)  # waiting for data to load
    resp = client.scan(TableName="DynamoDB-Table")
    assert len(resp["Items"]) == 3


def teardown_function(function):
    common_funcs.delete_dynamodb_table_items()
    common_funcs.delete_logs()

