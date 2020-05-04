import flask
from flask import render_template, g, jsonify, request
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import json
import uuid
import time
from datetime import datetime
import pytz
from operator import itemgetter

app = flask.Flask(__name__)

def format_list(list):
    result = []
    for x in list:
        element = {}
        element['post_id']= x['post_id']['S']
        element['community']= x['community']['S']
        element['author']= x['author']['S']
        element['title']=x['title']['S']
        element['text']=x['text']['S']
        element['date']=int(x['date']['N'])
        if 'url' in x:
            element['url'] = x['url']['S']
        result.append(element)
    return result

@app.cli.command('init')
def init_db():
    #create_table()
    pass

@app.route('/posts/<_community>/post/<_post_id>', methods=['GET', 'DELETE'])
def view_post(_community,_post_id):
    if request.method== 'GET':
        try:
            db = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
            y = int(time.time())
            data = db.query(
                TableName='posts',
                KeyConditionExpression="community = :comm AND post_id =:id",
                ExpressionAttributeValues={
                    ':comm' :{ 'S': _community },
                    ':id': {'S': str(post_id)}
                }
            )
            data = data['Items']
            new_Data = json.dumps(format_list(data)[0])
            if(len(data) <= 2 ):
                message = {
                    'status' : 400,
                    'message' : "Bad Request, Post not found "
                    }
                resp = jsonify(message)
                resp.status_code = 400
            else:
                message = {
                    'status' : 200,
                    'data' : new_Data,
                    'message': '200 ok'
                }
                resp = jsonify(message)
                resp.status_code = 200

        except:
            message = {
                'status' : 400,
                'message' : "Bad Request, Post not found " + str(e) + " " + _community
                }
            resp = jsonify(message)
            resp.status_code = 400

        return resp
    elif request.method == 'DELETE':
        try:
            response = table.delete_item(
                Key={
                    'post_id': _post_id,
                    'community': _community
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
                'message' : "Bad Request, fail to delete"
                }
            resp = jsonify(message)
            resp.status_code = 400

        return resp

@app.route('/posts/<_community>/recent/<_n_posts>', methods=['GET'])
def view_community(_community, _n_posts):
    try:
        db = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        y = int(time.time())
        data = db.query(
            TableName='posts',
            IndexName = 'recent',
            Limit = int(_n_posts),
            KeyConditionExpression="community = :comm AND #d <= :date",
            ExpressionAttributeNames={
                '#d' : 'date'
            },
            ExpressionAttributeValues={
                ':comm' :{ 'S': _community},
                ':date': { 'N': str(y) }
            }
        )
        data = data['Items']
        new_Data = json.dumps(format_list(data))
        message = {
            'status' : 200,
            'data' : new_Data,
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
        db = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        y = int(time.time())
        print("Current Time")
        print(y)
        data = db.query(
            TableName='posts',
            IndexName='recent',
            Limit = int(_n_posts),
            Select = 'ALL_ATTRIBUTES',
            KeyConditionExpression="community = :comm AND #d <= :date",
            ExpressionAttributeNames={
                '#d' : 'date'
            },
            ExpressionAttributeValues={
                ':comm' :{ 'S': "All"},
                ':date': { 'N': str(y) }
            }
        )
        data = data['Items']
        new_Data = json.dumps(format_list(data))
        message = {
            'status' : 200,
            'data' : new_Data,
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
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        table = dynamodb.Table('posts')
        x = request.json
        post_id = uuid.uuid4()
        date = time.time()
        #date = datetime.utcnow()
        #date = date.replace(tzinfo=pytz.utc)
        if 'url' in x:
            table.put_item(
                Item={
                     'post_id': str(post_id),
                     'community': x['community'],
		             'author': x['author'],
		             'title': x['title'],
                     'url': x['url'],
                     'text': x['text'],
		             'date': int(date)
                 }
            )
            table.put_item(
                Item={
                     'post_id': str(post_id),
                     'community': "All",
		             'author': x['author'],
		             'title': x['title'],
                     'url': x['url'],
                     'text': x['text'],
		             'date': int(date)
                 }
            )
        else:
            table.put_item(
                Item={
                     'post_id': str(post_id),
                     'community': x['community'],
                     'author': x['author'],
	                 'title': x['title'],
 		             'text': x['text'],
                     'date': int(date)
                 }
            )
            table.put_item(
                Item={
                     'post_id': str(post_id),
                     'community': 'All',
                     'author': x['author'],
	                 'title': x['title'],
 		             'text': x['text'],
                     'date': int(date)
                 }
            )

        with app.app_context():
            db = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
            data = db.query(
                TableName='posts',
                KeyConditionExpression="community = :comm AND post_id =:id",
                ExpressionAttributeValues={
                    ':comm' :{ 'S': x['community'] },
                    ':id': {'S':str(post_id)}
                }
            )
            data = data['Items'][0]
            url = "/posts/" +data['community']['S'] +"/post/"+ str(data['post_id']['S'])
        message = {
            'status' : 201,
            'url' : str(url),
            'message' : "Insert successfully"
            }
        resp = jsonify(message)
        resp.status_code = 201

    except:
        message = {
            'status' : 400,
            'message' : "Bad Request, fail to insert sql"
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
