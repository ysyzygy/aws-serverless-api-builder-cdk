from aws_cdk import (
    aws_apigateway as api_gateway,
)


def create_session_rp_schema():
    create_session_response_schema = api_gateway.JsonSchema(type=api_gateway.JsonSchemaType.OBJECT, properties={
        "containerIp": api_gateway.JsonSchema(type=api_gateway.JsonSchemaType.STRING,
                                              description='Service container address IP'),
        "status": api_gateway.JsonSchema(type=api_gateway.JsonSchemaType.STRING,
                                              description='Service container address IP')
    })
    return create_session_response_schema


def delete_session_rp_schema():
    return create_session_rp_schema()
