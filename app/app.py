#!/usr/bin/env python3

import json
import os
from string import Template

from aws_cdk import core

from stacks.apigateway.api_gateway_stack import ApiGatewayStack
from stacks.apigateway.api_gateway_props import ApiGatewayProps

if 'CDKENV' in os.environ.keys():
    cdk_env = os.environ['CDKENV']
else:
    cdk_env = 'dev'

properties = "resources/" + cdk_env + '.properties.json'

f = open(properties, 'r')
env_properties = json.load(f)
f.close()

ACCOUNT_NUMBER = properties['project']['account_id']

CDK_DEFAULT_REGION = os.environ.get('CDK_DEFAULT_REGION', properties['project']['region'])
tags = properties['project']['tags']

project_name = properties['project']['name']
# name: functional name to identify a resource created by aws cdk
env_template = Template(project_name + '-$name')
global_resources_template = Template(project_name + "-" + cdk_env + '-$name')

cdk_env = core.Environment(
    account=os.environ.get("CDK_DEPLOY_ACCOUNT", ACCOUNT_NUMBER),
    region=os.environ.get("CDK_DEPLOY_REGION", CDK_DEFAULT_REGION)
)
app = core.App()

api_gateway_props = ApiGatewayProps(
    props=properties,
    template=env_template
)

api_gateway_stack = ApiGatewayStack(
    app,
    api_gateway_props=api_gateway_props,
    env=cdk_env,
    tags=tags)


app.synth()
