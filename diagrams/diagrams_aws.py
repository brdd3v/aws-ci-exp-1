from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.database import Dynamodb
from diagrams.aws.management import Cloudwatch


with Diagram("", outformat=["png"], show=False):
    lambda_ = Lambda("Lambda Func")
    SNS("SNS Topic") >> SQS("SQS Queue") >> lambda_ >> Dynamodb("DynamoDB Table")
    lambda_ >> Cloudwatch("Cloudwatch Log Group")
