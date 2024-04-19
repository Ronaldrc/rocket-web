from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    RemovalPolicy
)

class LambdaDynamoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        table_name = "rocket-web"
        partition_key_name = "uid"
        read_capacity_units = 5
        write_capacity_units = 5

        table = dynamodb.Table(self, id=table_name,
                            table_name=table_name,
                            partition_key=dynamodb.Attribute(
                                name=partition_key_name,
                                type=dynamodb.AttributeType.NUMBER),
                            read_capacity=read_capacity_units,
                            write_capacity=write_capacity_units,
                            removal_policy=RemovalPolicy.DESTROY)
        
        # Lambda Function
        lambda_function = lambda_.Function(self, "rocket-web",
                                           runtime=lambda_.Runtime.PYTHON_3_8,
                                           handler="lambda_function.py",
                                           path=lambda_.Code.from_asset("lambda.zip"))

        # IAM Permissions
        table.grant_read_write_data(lambda_function)
        lambda_function.add_to_role_policy(iam.PolicyStatement(
            actions=["dynamodb:*"],
            resources=[table.table_arn],
        ))

        # Invoke Lambda function once


        # Populate dynamoDB

