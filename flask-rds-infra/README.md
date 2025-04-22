# Flask RDS Infrastructure (AWS CDK)

This directory contains the AWS Cloud Development Kit (CDK) code for provisioning the necessary AWS infrastructure to support the Flask application located in the sibling `../flask-rds-app` directory.

This infrastructure stack defines and deploys the backend resources required for the application to store and retrieve data securely.

## Resources Created

This CDK stack provisions the following AWS resources:

* **AWS RDS PostgreSQL Instance:** A managed PostgreSQL database instance (`db.t3.micro` by default, using PostgreSQL 15).
* **AWS Secrets Manager Secret:** Securely stores the master username (`flaskadmin`) and a randomly generated password for the RDS instance. The application retrieves these credentials at runtime.
* **EC2 Security Group:** Acts as a virtual firewall for the RDS instance, initially configured to allow PostgreSQL traffic (port 5432) only from within the default VPC where the instance resides. *Note: For local development/migration access, this security group might need temporary modification.*
* **(Reference)** **Default VPC Lookup:** The stack utilizes the default VPC in the specified AWS account and region.

## Technology

* AWS Cloud Development Kit (CDK) v2
* Python (as the CDK language)
* AWS CloudFormation (Synthesized from CDK code)

## Prerequisites

To deploy this infrastructure, you need:

1.  An AWS Account with appropriate IAM permissions (CloudFormation, RDS, EC2, Secrets Manager, IAM roles for CDK).
2.  AWS CLI installed and configured (`aws configure`) with credentials for your account.
3.  Node.js and npm installed (Required by the AWS CDK Toolkit). (Current CDK versions recommend Node.js LTS versions like 20.x or 22.x).
4.  Python 3.8+ installed.
5.  The Python dependencies for this CDK project installed (see Usage).

## Usage

Commands should be run from within this `flask-rds-infra` directory.

1.  **Set up Python Environment (if not already done):**
    ```bash
    # Ensure you are in the flask-rds-infra directory
    python3 -m venv .venv
    source .venv/bin/activate # Linux/macOS
    # .venv\Scripts\activate # Windows
    pip install -r requirements.txt
    ```

2.  **Bootstrap CDK (One-time per AWS Account/Region):**
    If this is the first time using CDK in this account/region combination, you need to bootstrap it.
    ```bash
    cdk bootstrap
    ```

3.  **Deploy the Stack:**
    This command synthesizes the CloudFormation template and deploys the resources defined in `flask_rds_infra/flask_rds_infra_stack.py`.
    ```bash
    cdk deploy
    ```
    * The CDK will show changes and ask for confirmation before deploying.
    * Note the **Outputs** printed at the end, especially `SecretARN`, `DBEndpoint`, `DBPort`, and `DBName`, as these are needed by the Flask application (`../flask-rds-app/.env` file).

4.  **Destroy the Stack:**
    To remove all the resources created by this stack (useful after finishing the lab to avoid costs):
    ```bash
    cdk destroy
    ```
    * Requires confirmation before deleting resources.
    * *Note:* The `RemovalPolicy` for the RDS instance and Secret is set to `DESTROY` in the stack code for easy cleanup in this lab context. **Do not use `DESTROY` for production data!**

## Configuration

* **AWS Account/Region:** The target deployment environment (account and region) is determined by the `env` parameter passed during stack instantiation in `app.py`. This typically uses the `CDK_DEFAULT_ACCOUNT` and `CDK_DEFAULT_REGION` environment variables set by the CDK CLI based on your configured AWS profile.
* **Resource Configuration:** Database instance type, version, secret name, etc., are defined within the `flask_rds_infra/flask_rds_infra_stack.py` file.

## Security Notes

* Credentials are not hardcoded but stored securely in AWS Secrets Manager.
* The RDS Security Group restricts network access. Remember to manage its rules carefully, especially if adding temporary access rules for local development.
* The CDK deployment role requires sufficient permissions to create the specified resources.
