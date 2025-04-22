import os
import json
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv() # Load .env file if present (for local dev)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a-default-fallback-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Option 1: Get DB URL directly from environment (less secure, good for quick local tests)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Option 2: Fetch credentials from AWS Secrets Manager (Recommended)
    db_uri = None
    secret_name = os.environ.get('SECRET_NAME')
    region_name = os.environ.get('AWS_REGION')

    if secret_name and region_name:
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            if 'SecretString' in get_secret_value_response:
                secret = json.loads(get_secret_value_response['SecretString'])
                username = secret.get('username')
                password = secret.get('password')
                host = secret.get('host') # Host stored in secret is preferred
                port = secret.get('port', 5432) # Default to 5432 if not in secret
                dbname = secret.get('dbname')
                # Construct the database URI
                db_uri = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
            else:
                # Handle binary secret if necessary (less common for DB creds)
                print("Binary secret found, cannot parse.")
        except ClientError as e:
            print(f"Error retrieving secret: {e}")
            # Handle error appropriately (e.g., raise exception, log, fallback)
            raise e # Fail fast if credentials cannot be loaded

    SQLALCHEMY_DATABASE_URI = db_uri

    if not SQLALCHEMY_DATABASE_URI:
         # Try falling back to DATABASE_URL env var if secret fetch failed or wasn't configured
         SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
         if not SQLALCHEMY_DATABASE_URI:
             raise ValueError("Database configuration not found. Set SECRET_NAME/AWS_REGION or DATABASE_URL environment variables.")
