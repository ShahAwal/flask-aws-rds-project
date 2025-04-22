from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct
import json

class FlaskRdsInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- Networking (VPC) ---
        # Use the default VPC for simplicity, or create a new one
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        # If not using default VPC: vpc = ec2.Vpc(self, "FlaskVpc", max_azs=2)

        # --- Security Group for RDS ---
        # Allows PostgreSQL traffic only from within the same VPC (adjust as needed)
        rds_security_group = ec2.SecurityGroup(
            self, "RdsSecurityGroup",
            vpc=vpc,
            description="Allow PostgreSQL access from within VPC",
            allow_all_outbound=True
        )
        rds_security_group.add_ingress_rule(
            # Allow traffic from any IP within the VPC CIDR block
            # For tighter security, restrict to specific Security Group of your app server/container host
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(5432),
            description="Allow PostgreSQL from VPC"
        )

        # --- Database Credentials Secret ---
        db_credentials = secretsmanager.Secret(
            self, "DBCredentialsSecret",
            secret_name="flask-app/db-credentials", # Define a clear name
            description="Credentials for Flask App RDS database",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({"username": "flaskadmin"}),
                generate_string_key="password",
                exclude_punctuation=True,
                include_space=False,
                password_length=16
            )
        )

        # --- RDS PostgreSQL Instance ---
        db_instance = rds.DatabaseInstance(
            self, "PostgresInstance",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15 # Use a relevant recent version
            ),
            instance_type=ec2.InstanceType.of( # Choose an appropriate instance type
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO # Suitable for lab/dev
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC), # Or PRIVATE for better security
            security_groups=[rds_security_group],
            credentials=rds.Credentials.from_secret(db_credentials), # Use secret for master credentials
            database_name="flaskappdb",
            removal_policy=RemovalPolicy.DESTROY, # Automatically delete on stack destroy (for lab)
            # Set to RETAIN or SNAPSHOT for production
            backup_retention=None if RemovalPolicy.DESTROY else cdk.Duration.days(7), # Disable backups if destroying
            delete_automated_backups=True if RemovalPolicy.DESTROY else False,
            multi_az=False # Keep costs down for lab
        )

        # --- Outputs ---
        CfnOutput(self, "DBEndpoint", value=db_instance.db_instance_endpoint_address)
        CfnOutput(self, "DBPort", value=db_instance.db_instance_endpoint_port)
        CfnOutput(self, "DBName", value="flaskappdb")
        CfnOutput(self, "SecretARN", value=db_credentials.secret_arn)
        CfnOutput(self, "RDSSecurityGroupId", value=rds_security_group.security_group_id)
