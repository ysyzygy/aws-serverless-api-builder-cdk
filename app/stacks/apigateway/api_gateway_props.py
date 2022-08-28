from dataclasses import dataclass
from aws_cdk import (aws_logs as logs)
from string import Template
from typing import List

@dataclass
class ApiGatewayProps:
    """Class for properties of ApiGateway."""
    props: dict
    template: Template
    dynamo_table_arn: str = None
    table_name: str = None
    partition_key: str = None


