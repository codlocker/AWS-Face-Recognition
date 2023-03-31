### Group Name :
- Dynamo

### Group Members :

- Ipsit Sahoo, Sandipan De, Varad Vijay Deshmukh

Installation steps:

- Ensure the test_case folder is downloaded from https://github.com/nehavadnere/cse546-project-lambda/tree/master/test_cases and set it up in the same directory as the project folder

- Ensure workload.py is in the same folder as well

- Run requirements.txt to ensure boto3 is installed for running the workload.py | pip install -r requirements.txt

- Install Docker setup (https://docs.docker.com/desktop/install/windows-install/)

 - In your docker environment, set-up the docker configuration file (Dockerfile) to run on this folder and push the changes to ECR.

- Once the docker has been setup, you can run workload.py to execute the test-cases.

RESOURCE NAMES:

1. input S3 nucket name : inputbucket-cse546
2. output S3 bucket name : outputbucket-cse546
3. Dynamo DB : After configuring AWS CLI, push data to dynamo_db using upload_data_to_dynamo.py
4. Here's how the end to end pipe looks like

![E2E flow](assets/Screenshot%202022-06-20%20213611.jpg)

- Once the docker has been setup, you can run workload.py to execute the test-cases.

Skeleton Forked from : https://github.com/nehavadnere/cse546-project-lambda

#### LOCAL ENVIRONMENT SETUP

 - Create a new python environment
 - Run: `pip install -r requirements.txt`
 - Uncomment line 177 in handler.py to test in your non-docker IDE environment.
- Execute `python handler.py`

=======
