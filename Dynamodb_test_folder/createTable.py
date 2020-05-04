import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
try:
	dynamodb = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
	table = dynamodb.create_table(
		AttributeDefinitions=[
			{
				'AttributeName': 'post_id',
				'AttributeType': 'S'
			},
			{
				'AttributeName': 'community',
				'AttributeType': 'S'  #Partition key
			},
			{
				'AttributeName': 'time_posted',
<<<<<<< HEAD
				'AttributeType': 'N'
=======
				'AttributeType': 'N' 
>>>>>>> 2be2f6e421ed4e26e3f709f56bc6e2f7e946af6d
			}
		],
		TableName='posts',
		KeySchema=[
		    {
		        'AttributeName': 'community',
		        'KeyType': 'HASH'  #Partition key
		    },
			{
				'AttributeName': 'post_id',
				'KeyType': 'RANGE'  #SORT key
			}
		],
		LocalSecondaryIndexes=[
			{
				'IndexName': 'Recent',
				'KeySchema':[
				 	{
		 		        'AttributeName': 'community',
		 		        'KeyType': 'HASH'  #Partition key
		 		    },
    		    	{
    		        	'AttributeName': 'time_posted',
    		        	'KeyType': 'RANGE'  #SORT key
    		    	}
				],
				'Projection': {
	                'ProjectionType': 'ALL'
            	},
			}
		],
		ProvisionedThroughput={
		    'ReadCapacityUnits': 100,
		    'WriteCapacityUnits': 100
		}
	)
except botocore.exceptions.ClientError as e : # in case the table is already created
	print(e)
	print("Yo stop, its already made")
	pass
