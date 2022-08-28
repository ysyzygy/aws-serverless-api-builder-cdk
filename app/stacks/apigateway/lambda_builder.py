from aws_cdk import (
    core,
    aws_lambda as _lambda
)

def create_lambda(self, template, props, execution_role, environment = None ):

    lambda_name = template.substitute(name=props['name'])
    lambda_function = _lambda.Function(
        self,
        id=lambda_name,
        function_name=lambda_name,
        description=props['description'],
        runtime=_lambda.Runtime.PYTHON_3_8,
        code=_lambda.Code.from_asset(props['code_from_asset']),
        handler=props['handler'],
        memory_size=props['cpu'],
        timeout=core.Duration.minutes(props['timeout']),
        role=execution_role,
        environment=environment
    )
    __add_layer(lambda_function, props, self, template)
    return lambda_function


def __add_layer(lambda_function, props, self, template):
    if "layer" in props:
        layer_name = template.substitute(name=props["layer"]["name"])
        layer = _lambda.LayerVersion(self,
                                     layer_name,
                                     layer_version_name=layer_name,
                                     compatible_runtimes=[_lambda.Runtime.PYTHON_3_8],
                                     code=_lambda.Code.from_asset(props["layer"]["code"]),
                                     description=props["layer"]["description"])
        lambda_function.add_layers(layer)

