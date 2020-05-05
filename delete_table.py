import boto3
from redis import Redis
def delete_tables():
    try:
        r = Redis(db=1)
        top = Redis(db=2)
        r.flushdb()
        top.flushdb()
        db = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        print(db.delete_table(TableName="posts"))
    except:
        pass

if __name__ == "__main__":
    delete_tables()
