import flask
from flask import render_template, g, jsonify, request
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import json
import uuid
from datetime import datetime
import pytz
from operator import itemgetter

app = flask.Flask(__name__)

def delete_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('posts')
    table.delete()

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@app.cli.command('init')
def init_db():
    #create_table()
    pass

@app.route('/posts/<_community>/post/<_post_id>', methods=['GET', 'DELETE'])
def view_post(_community,_post_id):
    if request.method== 'GET':
        try:
            dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
            table = dynamodb.Table('posts')
            response = table.query(
                KeyConditionExpression=Key('post_id').eq(_post_id) & Key('community').eq(_community)
            )

            data = json.dumps(response['Items'])
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
                    'data' : data,
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
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        table = dynamodb.Table('posts')
        response = table.scan()
        response = sorted(response['Items'], key=itemgetter('date'), reverse=True)
        data = list()
        limit_count = 0
        for i in response:
            if i['community'] == _community:
                if limit_count < int(_n_posts):
                    data.append(i)
                    limit_count += 1
        data = json.dumps(data)
        message = {
            'status' : 200,
            'data' : data,
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
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
        table = dynamodb.Table('posts')
        response = table.scan()
        response = sorted(response['Items'], key=itemgetter('date'), reverse=True)
        data = list()
        limit_count = 0
        for i in response:
            if limit_count < int(_n_posts):
                data.append(i)
                limit_count += 1
        data = json.dumps(data)
        message = {
            'status' : 200,
            'data' : data,
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
        date = datetime.utcnow()
        date = date.replace(tzinfo=pytz.utc)
        if'url' in x:
            table.put_item(
                Item={
                     'post_id': str(post_id),
                     'community': x['community'],
		             'author': x['author'],
		             'title': x['title'],
                     'url': x['url'],
                     'text': x['text'],
		             'date': str(date)


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
                     'date': str(date)
                 }
            )

        with app.app_context():
            dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
            table = dynamodb.Table('posts')
            response = table.scan()
            data = dict();
            for i in response['Items']:
                if i['community'] == x['community'] and i['title'] == x['title'] and i['author'] == x['author']:
                    data = i
            url = "/posts/" +data['community'] +"/post/"+ str(data['post_id'])
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
