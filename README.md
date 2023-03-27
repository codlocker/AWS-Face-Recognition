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