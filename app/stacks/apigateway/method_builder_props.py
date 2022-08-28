from dataclasses import dataclass
from aws_cdk import (
    aws_apigateway as api_gateway,
    aws_lambda as _lambda,
    core
)


@dataclass
class MethodBuilderProps:
    """Class for properties of Method builder."""
    responseSchema: api_gateway.JsonSchema
    lambdaFunction: _lambda.Function
    methodName: str
    api: api_gateway.RestApi
    parentStack: core.Stack
    baseResource: str
    httpMethod: str
    prefixId: str
    optionalResources: list = None
    requestSchema: api_gateway.JsonSchema = None
    responseStatusCode: int = 200
    reqContentType: str = "application/json"
    repContentType: str = "application/json"
    queryParameters: {} = None
