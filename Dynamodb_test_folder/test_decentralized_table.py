import flask
from flask import render_template, g, jsonify, request
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import json
import uuid
from datetime import datetime
from operator import itemgetter


dynamodb = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

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
dynamodb.put_item(
    TableName = 'posts',
    Item={
        'post_id': {'S':'3'},
        'community': {'S':"Animal Crossing"},
        'time_posted': {'N':"1002"},
        'author': {'S':"Kailie"},
        'title': {'S':"I got takoyaki boi"},
        'url': {'S':"reddit.com"},
        'text': {'S':"I'm sorry Lionel"},

     }
)

x = dynamodb.query(
    TableName = 'posts',
    IndexName = 'Recent',
    Select = 'ALL_ATTRIBUTES',
<<<<<<< HEAD
    KeyConditionExpression = "community = :comm AND time_posted < :time",
    ExpressionAttributeValues={
        ":comm": {'S':"DNE"},
=======

    KeyConditionExpression = "community = :comm AND time_posted < :time",
    ExpressionAttributeValues={
        ":comm": {'S':"Animal Crossing"},
>>>>>>> 2be2f6e421ed4e26e3f709f56bc6e2f7e946af6d
        ":time": {'N':"2000"}
    }
)
for item in x['Items']:
    print(item)
