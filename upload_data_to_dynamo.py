import boto3
import json
import os
import time
from botocore.exceptions import ClientError

dynamo_client = boto3.resource(service_name='dynamodb', region_name='us-east-1')
table_name='Student_data'

# delete table if it exists
try:
    student_data_table = dynamo_client.Table(table_name)
    student_data_table.delete()

    print(f"Deleting {student_data_table.name}...")
    student_data_table.wait_until_not_exists()
except ClientError as ce:
    print(ce.response['Error'])

# Create the table
try:
    dynamo_client.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
        ],
        TableClass='STANDARD',
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            },
        ],
        BillingMode='PROVISIONED',
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
    )

    print(f'Table {table_name} successfully created')
except ClientError as ce:
    print(ce.response['Error'])
    exit(-1)


student_data_table = dynamo_client.Table(table_name)

student_data_table.wait_until_exists()

if os.path.exists('./student_data.json'):
    data = json.load(open('./student_data.json'))
else:
    print('File student.json does not exist')
    exit(-1)

# Upload data to table
for d in data:
    print(f'Adding {d}')
    student_data_table.put_item(Item=d)
