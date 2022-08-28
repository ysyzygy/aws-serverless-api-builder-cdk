from aws_cdk import (
    aws_apigateway as api_gateway
)
import stacks.apigateway.method_builder_props as props


class MethodBuilder:
    lambdaIntegration: api_gateway.LambdaIntegration

    def __init__(self, props: props.MethodBuilderProps):
        self.api = props.api
        self.methodName = props.methodName

        self.lambdaIntegration = api_gateway.LambdaIntegration(props.lambdaFunction)
        responseModel = {props.repContentType: api_gateway.Model(props.parentStack,
                                                                 props.prefixId + 'ResponseModel',
                                                                 rest_api=self.api,
                                                                 schema=props.responseSchema,
                                                                 content_type=props.repContentType,
                                                                 description=props.methodName + ' response model',
                                                                 model_name=props.methodName + 'ResponseModel')}
        requestModel = None
        requestValidator = None

        if props.requestSchema:
            requestModel = {'application/json': api_gateway.Model(props.parentStack,
                                                                  props.prefixId + "RequestModel",
                                                                  rest_api=self.api,
                                                                  schema=props.requestSchema,
                                                                  content_type=props.reqContentType,
                                                                  description=props.methodName + ' request model',
                                                                  model_name=props.methodName + 'RequestModel')}
            requestValidator = api_gateway.RequestValidator(props.parentStack,
                                                            props.prefixId + "RequestValidator",
                                                            rest_api=self.api,
                                                            request_validator_name=props.methodName + "RequestValidator",
                                                            validate_request_body=False)

        baseResource = self.api.root.resource_for_path(props.baseResource)
        if props.optionalResources:
            for resource in props.optionalResources:
                baseResource = baseResource.add_resource(resource)
        self.addMethod(baseResource, props, responseModel, requestModel, requestValidator)

    def addMethod(self, baseResource, props, responseModel, requestModel, requestValidator):
        baseResource.add_method(
            http_method=props.httpMethod,
            integration=self.lambdaIntegration,
            request_parameters=props.queryParameters,
            method_responses=[
                api_gateway.MethodResponse(status_code=str(props.responseStatusCode),
                                           response_models=responseModel)],
            request_validator=requestValidator,
            request_models=requestModel,
            operation_name=self.methodName)
