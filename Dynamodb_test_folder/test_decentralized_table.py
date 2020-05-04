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

x = dynamodb.query(
    TableName = 'posts',
    IndexName = 'Recent',
    Select = 'ALL_ATTRIBUTES',
    KeyConditionExpression = "community = :comm AND time_posted < :time",
    ExpressionAttributeValues={
        ":comm": {'S':"DNE"},
        ":time": {'N':"2000"}
    }
)
for item in x['Items']:
    print(item)
