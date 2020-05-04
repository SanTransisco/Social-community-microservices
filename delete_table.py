import boto3
db = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
print(db.delete_table(TableName="posts"))
