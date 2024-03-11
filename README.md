# Cross Region AWS Transfer Family User Lambda
This serverless application automates the transfer of users from one AWS Transfer Family server (source) to another (destination). It is designed to run as an AWS Lambda function on a scheduled basis.

## Overview
The Lambda function fetches all users from the source server, checks their existence on the destination server, and creates them on the destination server if they don't already exist. It also updates the SSH public keys for each user on the destination server.

## Setup
### Prerequisites
AWS CLI installed and configured with necessary permissions.
AWS Transfer Family servers set up with the required users on both source and destination.
Python 3.10 installed on your local machine.

### Deployment
Clone this repository to your local machine.

```
git clone https://github.com/your-username/transfer-user-lambda.git
```
Navigate to the project directory.

```
cd transfer-user-lambda
```
Install the required dependencies.

```
pip install -r requirements.txt -t functions
```
Update the serverless.yaml file with your specific configuration.

Replace test-deployment-bucket-danial in the deploymentBucket property with your desired AWS S3 bucket for deployment.
Adjust the environment variables under transferUserFunction to match your server IDs, regions, and any other necessary configurations.
Deploy the serverless application.
```
sls deploy
```
### Configuration
- HOST_SERVER_ID: The ID of the source Transfer Family server.
- DEST_SERVER_ID: The ID of the destination Transfer Family server.
- SOURCE_REGION: The AWS region where the source server is located.
- DEST_REGION: The AWS region where the destination server is located.
Other environment variables can be configured as needed.
### Usage
The Lambda function is scheduled to run every 3 hours by default, as specified in the serverless.yaml file. Adjust the cron expression in the events section if needed.

### Permissions
The Lambda function requires the following AWS Identity and Access Management (IAM) permissions:

transfer:DescribeUser
transfer:CreateUser
transfer:ImportSshPublicKey
transfer:ListUsers
iam:PassRole
logs:*
### Cleanup
To remove the deployed resources, run:
```
sls remove
```
## Notes
Make sure to handle sensitive information securely, especially environment variables containing access keys and server IDs.
This Lambda function is designed to be executed in a secure AWS environment and may need adjustments for specific use cases or additional security measures.
