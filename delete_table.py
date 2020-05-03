
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
dynamodb.delete_table(TableName = 'posts')
