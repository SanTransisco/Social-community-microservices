import flask
from redis import Redis
from flask import  g, jsonify, request
from dateutil import parser
import json
import time

app = flask.Flask(__name__)
#This is a regular SET that just stores all the upvote/downvote info
#Key: POST:ID
#VALUE: VOTE INFO
Posts_Store = Redis(db =1)

#THIS IS A SORTED SET
#You sort things using their scores
# MECHANICAL_KEYBOARDS: {post1 : 100, post3:76,post2:6}
# BTS: {post4 : 200, post6:150,post5:50}
# ALL: {post1:200, post3:150,post2:50}
#So you can sort
Top = Redis(db=2)

from datetime import datetime, timedelta
from math import log

epoch = datetime(1970, 1, 1)

def epoch_seconds(date):
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def score(ups, downs):
    return ups - downs

def hot(ups, downs, date):
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(sign * order + seconds / 45000, 7)

def decode_redis_results(arr):
    result = []
    for i in arr:
        result.append(i.decode("utf-8"))
    return result


@app.teardown_appcontext
def close_connection(exception):
    print("We are shutting down")
'''
@app.cli.command('init')
def init_db():
    with app.app_context():
'''


@app.route('/votes/<_community>/post/<_post_id>/new_post', methods=['POST'])
def new_post(_community,_post_id):
    try:
        #NEW STUFF
        response = Posts_Store.hgetall(_post_id)
        time_posted = datetime.now().isoformat()
        #NEW STUFF
        if len(response) != 0 :
            message = {
                'status' : 400,
                'message' : "Bad Request - Post already Exists"
                }
            resp = jsonify(message)
            resp.status_code = 400
        else:
            response[b"UpVotes"] = str(0).encode("utf-8")
            response[b"DownVotes"] = str(0).encode("utf-8")
            response[b"Total_Score"] = str(0).encode("utf-8")
            response[b"date_created"] = str(time_posted).encode("utf-8")
            message = {
                'status' : 200,
                'message' : 'Post :' +_post_id + ' has been created on the voting microservice',
            }
            Posts_Store.hmset(_post_id,response)

            #MECHANICAL_KEYBOARDS {011021 : 200}
            Top.zadd(_community,{_post_id : 0})
            Top.zadd("All",{_post_id : 0})
            Top.zadd("HOT",{_post_id : hot(0,0, parser.isoparse(time_posted))})
            
            resp = jsonify(message)
            resp.status_code = 200
    except redis.exceptions as e:
        message = {
            'status' : 400,
            'message' : "Bad Request- Community or Post does not exists"
            }
        resp = jsonify(message)
        resp.status_code = 400

    return resp


@app.route('/votes/<_community>/post/<_post_id>/upvote', methods=['PATCH'])
def upvote_post(_community,_post_id):
    try:
        #NEW STUFF
        response = Posts_Store.hgetall(_post_id)
        #NEW STUFF
        if len(response) == 0 :
            message = {
                'status' : 404,
                'message' : "Post Not Found"
                }
            resp = jsonify(message)
            resp.status_code = 404
        else:
            response[b"UpVotes"] = str(int(response[b"UpVotes"])+1).encode("utf-8")
            response[b"Total_Score"] = str(int(response[b"Total_Score"])+1).encode("utf-8")

            message = {
                'status' : 200,
                'upvote' : int(response[b"UpVotes"]),
                'message' : 'Post :' +_post_id + ' has been upvoted',
            }

            Posts_Store.hmset(_post_id,response)

            #MECHANICAL_KEYBOARDS {011021 : 200}
            Top.zadd(_community,{_post_id : int(response[b"Total_Score"])+1})
            Top.zadd("All",{_post_id : int(response[b"Total_Score"])+1})
            time_posted = response[b"date_created"].decode("utf-8")
            Top.zadd("HOT",{_post_id : hot(
                                        int(response[b"UpVotes"]),
                                        int(response[b"DownVotes"]),
                                        parser.isoparse(time_posted))})

            resp = jsonify(message)
            resp.status_code = 200
    except redis.exceptions as e:
        message = {
            'status' : 400,
            'message' : "Bad Request- Community or Post does not exists"
            }
        resp = jsonify(message)
        resp.status_code = 400

    return resp


@app.route('/votes/<_community>/post/<_post_id>/downvote', methods=['PATCH'])
def downvote_post(_community,_post_id):
    try:
        response = Posts_Store.hgetall(_post_id)
        #NEW STUFF
        if len(response) ==0:
            message = {
                'status' : 404,
                'message' : "Post Not Found"
                }
            resp = jsonify(message)
            resp.status_code = 404
        else:
            response[b"DownVotes"] = str(int(response[b"DownVotes"])+1).encode("utf-8")
            response[b"Total_Score"] = str(int(response[b"Total_Score"])-1).encode("utf-8")
            message = {
                'status' : 200,
                'downvote' : int(response[b"DownVotes"]),
                'message' : 'Post :' +_post_id + ' has been downvoted',
            }

            Posts_Store.hmset(_post_id,response)
            Top.zadd(_community,{_post_id : int(response[b"Total_Score"])})
            Top.zadd("All",{_post_id : int(response[b"Total_Score"])})
            time_posted = response[b"date_created"].decode("utf-8")
            Top.zadd("HOT",{_post_id : hot(int(response[b"UpVotes"]),int(response[b"DownVotes"]), parser.isoparse(time_posted))})

            resp = jsonify(message)
            resp.status_code = 200
    except redis.exceptions as e:
        message = {
            'status' : 400,
            'message' : "Bad Request- Community or Post does not exists"
            }
        resp = jsonify(message)
        resp.status_code = 400
    return resp

# reports the number of upvotes and downvotes for a post
@app.route('/votes/<_community>/post/<_post_id>/score', methods=['GET'])
def show_votes(_community, _post_id):
    try:
        response = Posts_Store.hgetall(_post_id)
        #NEW STUFF
        if len(response) ==0:
            message = {
                'status' : 404,
                'message' : "Post Not Found"
                }
            resp = jsonify(message)
            resp.status_code = 404
        else:
            message = {
                'status' : 200,
                'upvote' : int(response[b'UpVotes']),
                'downvote': int(response[b'DownVotes']),
                'message' : 'Post: ' + _post_id + ' votes reported'
            }
            time_posted = response[b"date_created"].decode("utf-8")
            Top.zadd("HOT",{_post_id : hot(int(response[b"UpVotes"]),int(response[b"DownVotes"]), parser.isoparse(time_posted))})
            resp = jsonify(message)
            resp.status_code = 200

    except redis.exceptions as e:
        message = {
            'status' : 400,
            'message' : "Bad Request- Community or Post does not exists"
            }
        resp = jsonify(message)
        resp.status_code = 400
    return resp

# list the n top-scoring posts to any community
@app.route('/votes/all/top/<n_posts>', methods=['GET'])
def top_posts(n_posts):
    try:
        result=Top.zrevrange("All",0,int(n_posts)-1)
        payload = decode_redis_results(result)
        message = {
            'status' : 200,
            'data' : result,
            'message': 'These are the top scoring posts'
        }
        resp = jsonify(message)
        resp.status_code = 200

    except redis.exceptions as e:
        message = {
            'status' : 400,
            'message' : "Bad Request, Posts not found",
        }
        resp = jsonify(message)
        resp.status_code = 400

    return resp

@app.route('/votes/all/hot/<n_posts>', methods=['GET'])
def hot_posts(n_posts):
    try:
        result=Top.zrevrange("HOT",0,int(n_posts)-1)
        payload = decode_redis_results(result)
        message = {
            'status' : 200,
            'data' : result,
            'message': 'These are the top scoring posts'
        }
        resp = jsonify(message)
        resp.status_code = 200

    except redis.exceptions as e:
        message = {
            'status' : 400,
            'message' : "Bad Request, Posts not found",
        }
        resp = jsonify(message)
        resp.status_code = 400

    return resp

@app.route('/votes/<_community>/top/<n_posts>', methods=['GET'])
def top_posts_community(_community, n_posts):
    try:
        result=Top.zrevrange(_community,0,int(n_posts)-1)
        payload = decode_redis_results(result)
        message = {
            'status' : 200,
            'data' : result,
            'message': 'These are the top scoring posts'
        }
        resp = jsonify(message)
        resp.status_code = 200

    except redis.exceptions as e:
        message = {
            'status' : 400,
            'message' : "Bad Request- Community or Post does not exists"
        }
        resp = jsonify(message)
        resp.status_code = 400

    return resp
'''
# given a list of post identifiers, return the list sorted by score
@app.route('/votes/list/top', methods=['GET'])
def list():
    try:
        x = request.json

        array = x['post']
        query = "SELECT id FROM posts WHERE "

        firstTime = 0
        for post in array:
            if firstTime == 0:
                query = query + "id = " + str(post)
                firstTime = 1
            else:
                query = query + " OR id = " + str(post)

        query = query + " ORDER BY net_score DESC;"
        print(query)
        data = query_db(query)

        message = {
            'status' : 200,
            'data' : data,
            'message': 'These are the top scoring posts from the list'
        }
        resp = jsonify(message)
        resp.status_code = 200

    except sqlite3.Error as e:
        message = {
            'status' : 400,
            'message' : "Bad Request, Posts not found" + str(e),
        }
        resp = jsonify(message)
        resp.status_code = 400

    return resp
'''

@app.errorhandler(404)
def page_not_found(e):
    message = {
        'status' : 404,
        'message' : '404 not found',
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
