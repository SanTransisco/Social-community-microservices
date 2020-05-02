import boto3
from boto3.dynamodb.conditions import Key, Attr


try:
	dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
	table = dynamodb.create_table(
		TableName='posts',
    		KeySchema=[
    		    {
    		        'AttributeName': 'post_id',
    		        'KeyType': 'HASH'  #Partition key
    		    },
    		    {
    		        'AttributeName': 'community',
    		        'KeyType': 'RANGE'  #Sort key
    		    }
    		],
    		AttributeDefinitions=[
    		    {
    		        'AttributeName': 'post_id',
    		        'AttributeType': 'S'
    		    },
    		    {
    		        'AttributeName': 'community',
    		        'AttributeType': 'S'
    		    },

    		],
    		ProvisionedThroughput={
    		    'ReadCapacityUnits': 100,
    		    'WriteCapacityUnits': 100
    		}
	)
except: # in case the table is already created
	pass