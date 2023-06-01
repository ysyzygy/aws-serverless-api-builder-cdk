
# AWS Serverless API Builder with AWS CDK

## Intro

- App: Create all resources to execute a task with AWS CDK

### Standard naming conventions:

Every resource created by CDK has an id and usually a name.
id and name should be the same.
Every resource has the following naming format:
{projectname}-{featurename}

In order to achieve that in each main app.py is created a Template:

```from string import Template
project_name = properties['project']['name']
##name: functional name to identify a resource created by aws cdk
template = Template(project_name + '-$name')

This template is added as parameter in every new stack:

PipelineStack(app,
              template.substitute(name=properties['pipeline']['pipeline_stack_name']),
              props=properties,
              **template=template**,
              tags=tags)
```      
##### pdoc: Auto-generate API documentation for Python projects
 Place inside app or cicd folder to update pdoc type:
pdoc --html stacks --force
