#!/usr/bin/env python3
import os
import aws_cdk as cdk

# Import your stack class
from flask_rds_infra.flask_rds_infra_stack import FlaskRdsInfraStack

# Define the environment using environment variables set by CDK CLI
# Ensure your AWS CLI is configured correctly for these to be populated
cdk_env = cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION")
)

app = cdk.App()

# Instantiate the stack and pass the environment information
FlaskRdsInfraStack(
    app,
    "FlaskRdsInfraStack",
    env=cdk_env  # <-- Add this env parameter
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.
    #---------------------------------------------------------------------------
    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.
    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    #---------------------------------------------------------------------------
    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */
    #env=cdk.Environment(account='123456789012', region='us-east-1'),
    #---------------------------------------------------------------------------
    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
)

app.synth()
