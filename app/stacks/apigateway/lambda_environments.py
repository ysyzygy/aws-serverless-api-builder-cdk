import stacks.apigateway.api_gateway_props as api_gateway_props

SEPARATOR = " "


def delete_session_environment(api_gateway_props: api_gateway_props):
    environment = dynamoc_props(api_gateway_props)
    environment.update(cluster_environment(api_gateway_props))
    return environment

def create_session_environment(api_gateway_props: api_gateway_props):
    environment = dynamoc_props(api_gateway_props)
    environment.update(cluster_environment(api_gateway_props))
    environment.update(task_def_and_subnets_props(api_gateway_props))
    return environment

def cluster_environment(api_gateway_props):
    environment = {
        "CLUSTER_ARN": api_gateway_props.cluster_arn
    }
    return environment

def task_def_and_subnets_props(api_gateway_props):
    environment = {
        "TASK_DEFINITION_ARN": api_gateway_props.task_definition_arn,
        "SUBNET_IDS": SEPARATOR.join(api_gateway_props.subnets)
    }
    return environment

def dynamoc_props(api_gateway_props):
    environment = {
        "TABLE_NAME": api_gateway_props.table_name,
        "PARTITION_KEY": api_gateway_props.partition_key
    }
    return environment