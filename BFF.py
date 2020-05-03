import flask
import requests
import json

app = flask.Flask(__name__)



@app.teardown_appcontext
def close_connection(exception):
    print("We are shutting down")

@app.cli.command('init')
def init_db():
    with app.app_context():
        pass

# gets the 25 most recent posts to a particular community
@app.route('/BFF/<_community>/recent', methods=['GET'])
def recent_posts(_community):
    url = 'http://localhost:2015/posts/{community}/recent/{num}'
    url = url.format(community = _community, num = 25)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    final_data = data['data']
    message = {
        'status': 200,
        'data': final_data,
        'message': '200 ok'
    }

    resp = jsonify(message)
    resp.status_code = 200

# gets the 25 most recent posts to any community
@app.route('/BFF/All/recent', methods=['GET'])
def all_recent_posts():
    url = 'http://localhost:2015/posts/all/recent/{num}'
    url = url.format(num = 25)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    final_data = data['data']
    message = {
        'status': 200,
        'data': final_data,
        'message': '200 ok'
    }

    resp = jsonify(message)
    resp.status_code = 200

# gets the top 25 posts to a particular community, sorted by score
@app.route('/BFF/<_community>/top', methods=['GET'])
def top_posts(_community):
    url = 'http://localhost:2015/votes/{community}/top/{num}'
    url = url.format(community = _community, num = 25)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    post_id = data['data']
    post_contents = []

    for i in post_id:
        url = 'http://localhost:2015/posts/{community}/post/{id}'
        url = url.format(community = _community, id = i)
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        data = r.json()
        post_info = data['data']
        post_contents.append(post_info)

    message = {
        'status': 200,
        'data': post_contents,
        'message': '200 ok'
    }

    resp = jsonify(message)
    resp.status_code = 200

# gets the top 25 posts to any community, sorted by score
@app.route('/BFF/All/top', methods=['GET'])
def all_top_posts():
    url = 'http://localhost:2015/votes/all/top/{num}'
    url = url.format(num = 25)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    post_id = data['data']
    post_contents = []

    for i in post_id:
        url = 'http://localhost:2015/posts/all/post/{id}'
        url = url.format(id = i)
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        data = r.json()
        post_info = data['data']
        post_contents.append(post_info)

    message = {
        'status': 200,
        'data': post_contents,
        'message': '200 ok'
    }

    resp = jsonify(message)
    resp.status_code = 200

# IN PROGRESS
# gets the top 25 posts to any community, ranking using "hot ranking" alg.
@app.route('/BFF/All/hot', methods=['GET'])
def all_hot_posts():
    url = 'http://localhost:2015/votes/all/hot/{num}'
    url = url.format(num = 25)
    data = r.json()
    final_data = data['data']
    message = {
        'status': 200,
        'data': final_data,
        'message': '200 ok'
    }

    resp = jsonify(message)
    resp.status_code = 200


@app.errorhandler(404)
def page_not_found(e):
    message = {
        'status' : 404,
        'message' : '404 not found',
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
