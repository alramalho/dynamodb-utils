import boto3
import argparse

def delete_table_entries(table_name, aws_endpoint=None):
    if aws_endpoint:
        dynamodb = boto3.resource('dynamodb', endpoint_url=aws_endpoint)
        client = boto3.client('dynamodb', endpoint_url=aws_endpoint)
    else:
        dynamodb = boto3.resource('dynamodb')
        client = boto3.client('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Get the primary key name from the table description
    response = client.describe_table(TableName=table_name)
    key_name = response['Table']['KeySchema'][0]['AttributeName']

    # Scan the table and delete each item using the primary key
    scan = table.scan()
    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(Key={key_name: each[key_name]})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delete all entries from DynamoDB table.')
    parser.add_argument('table_name', type=str, help='Name of the table to delete entries from.')
    parser.add_argument('-e', '--aws_endpoint', type=str, help='AWS endpoint URL (optional).')
    args = parser.parse_args()
    delete_table_entries(args.table_name, args.aws_endpoint)
    print('Done.')
