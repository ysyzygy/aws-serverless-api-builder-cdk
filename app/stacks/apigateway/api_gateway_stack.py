from aws_cdk import (
    core,
    aws_iam as iam,
    aws_apigateway as api_gateway,
    aws_s3 as s3,
    aws_dynamodb as dynamodb

)
from string import Template

import stacks.apigateway.lambda_builder as lambda_builder
import stacks.apigateway.method_builder as api_method
import stacks.apigateway.method_builder_props as method_props
import stacks.apigateway.schemas as schemas
import stacks.apigateway.api_gateway_props as api_gateway_props
import stacks.apigateway.lambda_environments  as lambda_environments
import stacks.apigateway.lambda_roles  as lambda_roles

class ApiGatewayStack(core.Stack):
    """
    Class: ApiGatewayStack

    It creates an API restful to manage data conversions flows
    """

    def __init__(self, scope: core.Construct, api_gateway_props: api_gateway_props, **kwargs) -> None:
        """

        @param scope:core.App() main app
        @param id: Stack id
        @type id: core.Construct
        @param props: properties for resources naming
        @type props: dict
        @param template: template for naming compliance
        @type template: Template
        @param kwargs: environment where to create the stack
        """
        props = api_gateway_props.props
        template = api_gateway_props.template
        id = template.substitute(name=props["api_gateway"]["stack_name"])
        super().__init__(scope, id, stack_name=id, description=props["api_gateway"]["description"], **kwargs)
        log_group = api_gateway_props.log_group
        self.__create_api_gateway_role(props, template)
        log_group_destination = api_gateway.LogGroupLogDestination(log_group=log_group)
        api = api_gateway.RestApi(self, template.substitute(name=props["api_gateway"]["api_rest_name"]),
                                  description=template.substitute(name=props["api_gateway"]["api_rest_description"]),
                                  deploy_options=api_gateway.StageOptions(
                                      stage_name=template.substitute(name=props["api_gateway"]["stage_name"]),
                                      data_trace_enabled=True,
                                      logging_level=api_gateway.MethodLoggingLevel.INFO,
                                      access_log_destination=log_group_destination)
                                  )

        sessions_table_name = self.__create_session_table(props, template,api_gateway_props)
        api_gateway_props.dynamo_table_resource_policy = "arn:aws:dynamodb:" + props["project"]["region"] + ":" + props["project"][
            "account_id"] + ":table/" + sessions_table_name

        self.__get_build_integrations(
            props,
            api,
            template,
            api_gateway_props
        )

    def __create_session_table(self, props: dict, template: Template, api_gateway_props: api_gateway_props):
        """

             @param props: properties for resources naming
             @type props: dict
             @param template: template for naming compliance
             @type template: Template

             """
        sessions_table_name = template.substitute(name=props["dynamodb"]["session_table"])
        api_gateway_props.table_name = sessions_table_name
        api_gateway_props.partition_key = "session_id"
        dynamodb.Table(self, sessions_table_name,
                                        table_name=api_gateway_props.table_name,
                                        partition_key=dynamodb.Attribute(name=api_gateway_props.partition_key,
                                                                         type=dynamodb.AttributeType.STRING),
                                        time_to_live_attribute="ttl")
        return sessions_table_name



    def __create_api_gateway_role(self, props: dict, template: Template) -> iam.IRole:
        """
        create api gateway role: Create a role to execute a  HTTP Method to invoke an api
        @param props: properties for resources naming
        @type props: dict
        @param template: template for naming compliance
        @type template: Template
        @return: created role
        @rtype: iam.IRole
        """

        role_name = template.substitute(name=props["api_gateway"]["role_name"])
        role = iam.Role(self, role_name, role_name=role_name,
                        assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com")
                        )
        return role

    def __get_build_integrations(self, props: dict,
                                 api: api_gateway.RestApi, template: Template,
                                 api_gateway_props: api_gateway_props):
        for integration in props["api_gateway"]["integrations"]:
            name = integration["name"]
            environment, id_prefix, request_schema, response_schema, role = self.build_api_method(api_gateway_props,
                                                                                                  integration, name,
                                                                                                  template)
            lambda_integration = lambda_builder.create_lambda(self,
                                                              template,
                                                              integration["lambda"],
                                                              role,
                                                              environment)

            self.__get_api_method_resources(integration)

            method_builder_props = method_props.MethodBuilderProps(response_schema, lambda_integration,
                                                                   name, api,
                                                                   self, integration["base_resource"],
                                                                   integration["method"],
                                                                   id_prefix,
                                                                   integration["optional_resources"],
                                                                   request_schema,
                                                                   integration["status_code"],
                                                                   integration["req_contentType"],
                                                                   integration["rep_contentType"],
                                                                   integration["query_parameters"])
            api_method.MethodBuilder(method_builder_props)

    def __get_api_method_resources(self, integration):
        if "optional_resources" not in integration:
            integration["optional_resources"] = None
        if "status_code" not in integration:
            integration["status_code"] = 200
        if "body_validation" not in integration:
            integration["body_validation"] = False
        if "req_contentType" not in integration:
            integration["req_contentType"] = "application/json"
        if "query_parameters" not in integration:
            integration["query_parameters"] = None
        if "rep_contentType" not in integration:
            integration["rep_contentType"] = "application/json"

    def build_api_method(self, api_gateway_props, integration, name, template):
        request_schema = None
        # Id models methods etc not avoid "-" characters
        id_prefix = template.substitute(name=name).replace("-", "")
        environment = {}
        role = None
        name_func = integration["name_func"]
        try:
            response_schema_func = getattr(schemas, f"{name_func}_rp_schema")
            response_schema = response_schema_func()
        except AttributeError:
            # this method doesn't have response_schema: continue
            pass
        try:
            request_schema_func = getattr(schemas, f"{name_func}_req_schema")
            request_schema = request_schema_func()
        except AttributeError:
            # this method doesn't have response_schema: continue
            pass
        try:
            environment_func = getattr(lambda_environments, f"{name_func}_environment")
            environment = environment_func(api_gateway_props)
        except AttributeError:
            print("No environment")
            # this method doesn't have response_schema: continue
            pass
        try:
            role_func = getattr(lambda_roles, f"{name_func}_role")
            role = role_func(self, integration["lambda"], template, api_gateway_props)
        except AttributeError:
            print("No role")
            # this method doesn't have response_schema: continue
            pass
        return environment, id_prefix, request_schema, response_schema, role