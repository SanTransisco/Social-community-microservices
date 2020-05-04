import flask
from flask import render_template, g, jsonify, request
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import time
app = flask.Flask(__name__)

def normalize_dictionary(list):
    result = []
    for element in list:
        dict = {}
        dict['post_id'] = element['post_id']['S']
        dict['author'] = element['author']['S']
        dict['time_posted'] = element['time_posted']['N']
        dict['text'] = element['text']['S']
        dict['community'] = element['community']['S']
        dict['title'] = element['url']['S']
        result.append(dict)
    return result


@app.teardown_appcontext
def close_connection(exception):
    pass

@app.cli.command('init')
def init_db():
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
				'AttributeType': 'N'
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

@app.route('/posts/<_community>/post/<_post_id>', methods=['GET', 'DELETE'])
def view_post(_community,_post_id):
    if request.method== 'GET':
        try:
            dynamodb = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
            x = dynamodb.query(
                TableName = 'posts',
                Select = 'ALL_ATTRIBUTES',
                KeyConditionExpression = "community = :comm AND post_id = :id",
                ExpressionAttributeValues={
                    ":comm": {'S':_community},
                    ":id": {'S':_post_id}
                }
            )
            if(len(x["Items"]) == 0 ):
                message = {
                    'status' : 404,
                    'message' : "Bad Request, Post not found "
                    }
                resp = jsonify(message)
                resp.status_code = 400
            else:
                final_data = normalize_dictionary(x["Items"])
                message = {
                    'status' : 200,
                    'data' : final_data,
                    'message': '200 ok'
                }
                resp = jsonify(message)
                resp.status_code = 200

        except sqlite3.Error as e:
            message = {
                'status' : 400,
                'message' : "Bad Request, Post not found " + str(e) + " " + _community
                }
            resp = jsonify(message)
            resp.status_code = 400

        return resp
    elif request.method == 'DELETE':
        try:
            dynamodb = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
            x = dynamodb.delete_item(
                TableName = 'posts',
                Key = {
                    "community": {'S': _community},
                    ":id": {'S': _post_id}
                }
            )
            message = {
                'status' : 200,
                'message' : "Delete successfully"
            }
            resp = jsonify(message)
            resp.status_code = 200
        except:
            message = {
                'status' : 400,
                'message' : "Bad Request, fail to delete sql"
                }
            resp = jsonify(message)
            resp.status_code = 400

        return resp

@app.route('/posts/<_community>/recent/<_n_posts>', methods=['GET'])
def view_community(_community, _n_posts):
    try:
        boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        epoch = time.gmtime(0)
        x = dynamodb.query(
            TableName = 'posts',
            IndexName = 'Recent',
            Limit = int(_n_posts),
            Select = 'ALL_ATTRIBUTES',
            KeyConditionExpression = "community = :comm AND time_posted < :time",
            ExpressionAttributeValues={
                ":comm": {'S':_community},
                ":time": {'N': str(epoch)}
            }
        )
        if(len(x["Items"]) == 0 ):
            message = {
                'status' : 404,
                'message' : "Bad Request, Post not found "
                }
            resp = jsonify(message)
            resp.status_code = 400
        else:
            final_data = normalize_dictionary(x["Items"])
            message = {
                'status' : 200,
                'data' : final_data,
                'message': '200 ok'
            }
            resp = jsonify(message)
            resp.status_code = 200

    except:
        message = {
            'status' : 400,
            'message' : "Bad Request, Community not found"
            }
        resp = jsonify(message)
        resp.status_code = 400

    return resp

@app.route('/posts/all/recent/<_n_posts>', methods=['GET'])
def view_all(_n_posts):
    try:
        boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        epoch = time.gmtime(0)
        x = dynamodb.query(
            TableName = 'posts',
            IndexName = 'Recent',
            Limit = int(_n_posts),
            Select = 'ALL_ATTRIBUTES',
            KeyConditionExpression = "community = :comm AND time_posted < :time",
            ExpressionAttributeValues={
                ":comm": {'S':"All"},
                ":time": {'N': str(epoch)}
            }
        )
        if(len(x["Items"]) == 0 ):
            message = {
                'status' : 404,
                'message' : "Bad Request, Post not found "
                }
            resp = jsonify(message)
            resp.status_code = 400
        else:
            final_data = normalize_dictionary(x["Items"])
            message = {
                'status' : 200,
                'data' : final_data,
                'message': '200 ok'
            }
            resp = jsonify(message)
            resp.status_code = 200

    except:
        message = {
            'status' : 400,
            'message' : "Bad Request, Posts not found"
            }
        resp = jsonify(message)
        resp.status_code = 400

    return resp

@app.route('/posts/<_community>/new', methods=['POST'])
def new_post(_community):
    try:
        x = request.json
        dynamodb = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

        if 'url' in x:
            dynamodb.put_item(
                TableName = 'posts',
                Item={
                    'post_id': {'S':'2'},
                    'community': {'S':"Mechanical_Keyboards"},
                    'time_posted': {'N':"1001"},
                    'author': {'S':"San"},
                    'title': {'S':"Mods before Alphas"},
                    'url': {'S':"reddit.com"},
                    'text': {'S':"Why did Drop send my stuff in two packages"},
                 }
            )
        else:
            dynamodb.put_item(
                TableName = 'posts',
                Item={
                    'post_id': {'S':'2'},
                    'community': {'S':"Mechanical_Keyboards"},
                    'time_posted': {'N':"1001"},
                    'author': {'S':"San"},
                    'title': {'S':"Mods before Alphas"},
                    'text': {'S':"Why did Drop send my stuff in two packages"},

                 }
            )
        message = {
            'status' : 201,
            'url' : url,
            'message' : "Insert successfully"
            }
        resp = jsonify(message)
        resp.status_code = 201

    except sqlite3.Error as e:
        message = {
            'status' : 400,
            'message' : "Bad Request, fail to insert sql " + str(e)
            }
        resp = jsonify(message)
        resp.status_code = 400

    return resp



@app.errorhandler(404)
def page_not_found(e):
    message = {
        'status' : 404,
        'message' : '404 not found',
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
