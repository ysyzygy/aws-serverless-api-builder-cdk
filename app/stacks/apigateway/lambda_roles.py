from aws_cdk import aws_iam as iam
from aws_cdk.aws_iam import ManagedPolicy
from string import Template
import stacks.apigateway.api_gateway_props as api_gateway_props

def create_session_role(self, props: dict, template: Template, api_gateway_props: api_gateway_props):
    execution_role, policy_name = lambda_basic_role(props, self, template)
    statements = []

    execution_role.attach_inline_policy(iam.Policy(
        self,
        policy_name,
        policy_name=policy_name,
        statements=statements))

    return execution_role


def lambda_basic_role(props, self, template):
    execution_role_name = template.substitute(name=props['execution_role'])
    execution_role = iam.Role(self,
                              execution_role_name,
                              role_name=execution_role_name,
                              assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))
    execution_role.add_managed_policy(ManagedPolicy.
                                      from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'))
    policy_name = template.substitute(name=props["policy_name"])
    return execution_role, policy_name


def delete_session_role(self, props: dict, template: Template, api_gateway_props: api_gateway_props):
    execution_role, policy_name = lambda_basic_role(props, self, template)
    statements = []

    execution_role.attach_inline_policy(iam.Policy(
        self,
        policy_name,
        policy_name=policy_name,
        statements=statements))

    return execution_role