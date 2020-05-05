import boto3
from boto3.dynamodb.conditions import Key, Attr

def create_table():
	try:
		dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
		table = dynamodb.create_table(
			TableName='posts',
	    		KeySchema=[
	    		    {
	    		        'AttributeName': 'community',
	    		        'KeyType': 'HASH'  #Sort key
	    		    },
	    		    {
	    		        'AttributeName': 'post_id',
	    		        'KeyType': 'RANGE'  #Partition key
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
					{
						'AttributeName': 'date',
						'AttributeType': 'N'
					}

	    		],
				LocalSecondaryIndexes=[
					{
						'IndexName' : 'recent',
						'KeySchema':[
							{
								'AttributeName': 'community',
								'KeyType': 'HASH'  #PAR key
							},
							{
								'AttributeName': 'date',
								'KeyType': 'RANGE'  #Sort key
							},

						],
						'Projection':{
							'ProjectionType' : 'ALL'
						}
					},
				],
	    		ProvisionedThroughput={
	    		    'ReadCapacityUnits': 100,
	    		    'WriteCapacityUnits': 100
	    		}
		)
	except: # in case the table is already created
		pass

if __name__ == "__main__":
	create_table()
