import flask
from flask import render_template, g, jsonify, request
import sqlite3
app = flask.Flask(__name__)

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("posts.db")
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('posts.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/', methods=['GET'])
def home():
    message = {
        'status' : 200,
        'message' : 'Welcome to microservices',
        '1. POSTS' : '/api/posts',
        '2. VOTES' : '/api/votes'
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/posts/', methods=['GET'])
def post_path():
    message = {
        'status' : 200,
        'message' : '200 ok',
        '1. Create a new post' : '/api/posts/new_post',
        '2. Delete an existing post' : '/api/posts/delete_post',
        '3. Retrieve an existing post': '/api/posts/view',
        '4. List the n most recent posts to a particular community': '/api/posts/view_community',
        '5. List the n most recent posts to any community': '/api/posts/all'
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/posts/all')
def all_posts():
    try:
        data = query_db('SELECT author, community, title, time FROM posts ORDER BY id DESC;')
        message = {
            'status' : 200,
            'data' : data,
            'message': '200 ok'
        }
        resp = jsonify(message)
        resp.status_code = 200

    except sqlite3.Error as e:
        message = {
            'status' : 400,
            'message' : "Bad Request, fail to select sql"
            }
        resp = jsonify(message)
        resp.status_code = 400

    return resp

@app.route('/posts/view/<post_id>', methods=['GET'])
def view_post(post_id):
    try:
        query = "SELECT * FROM posts WHERE id = {post_id};"
        query = query.format(post_id = post_id)
        data = query_db(query)
        message = {
            'status' : 200,
            'data' : data,
            'message': '200 ok'
        }
        resp = jsonify(message)
        resp.status_code = 200

    except sqlite3.Error as e:
        message = {
            'status' : 400,
            'message' : "Bad Request, Post not found"
            }
        resp = jsonify(message)
        resp.status_code = 400

    return resp

@app.route('/posts/<_community>/recent/<_n_posts>', methods=['GET'])
def view_community(_community, _n_posts):
    try:
        query = "SELECT id, title, author, community, upvote, downvote, net_score, time FROM posts WHERE community ='{community}' ORDER BY time LIMIT {post_num};"

        query = query.format(community =_community, post_num = _n_posts)
        data = query_db(query)

        message = {
            'status' : 200,
            'data' : data,
            'message': '200 ok'
        }
        resp = jsonify(message)
        resp.status_code = 200

    except sqlite3.Error as e:
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
        query = "SELECT id, title, author, community, upvote, downvote, net_score, time FROM posts ORDER BY time LIMIT {post_num};"

        query = query.format(post_num = _n_posts)
        data = query_db(query)

        message = {
            'status' : 200,
            'data' : data,
            'message': '200 ok'
        }
        resp = jsonify(message)
        resp.status_code = 200

    except sqlite3.Error as e:
        message = {
            'status' : 400,
            'message' : "Bad Request, Posts not found"
            }
        resp = jsonify(message)
        resp.status_code = 400

    return resp

@app.route('/posts/delete', methods=['POST','DELETE'])
def delete_post():
    try:
        x = request.json
        query = "DELETE FROM posts WHERE title = '{title}' AND author = '{author}' AND community ='{community}';"
        query = query.format(title = x['title'], author = x['author'], community = x['community'])
        db = get_db()
        db.execute(query)
        db.commit()
        message = {
            'status' : 200,
            'message' : "Delete successfully"
        }
        resp = jsonify(message)
        resp.status_code = 200

    except sqlite3.Error as e:
        message = {
            'status' : 400,
            'message' : "Bad Request, fail to delete sql"
            }
        resp = jsonify(message)
        resp.status_code = 400

    return resp


@app.route('/posts/new', methods=['POST'])
def new_post():
    try:
        x = request.json

        if'url' in x:
            query = "INSERT INTO posts(title, author, community, url, text) VALUES ('{title}','{author}','{community}','{url}', '{text}')"
            query = query.format(title = x['title'], author = x['author'], community = x['community'], url = x['url'], text = x['text'])
        else:
            query = "INSERT INTO posts(title, author, community, text) VALUES ('{title}','{author}','{community}', '{text}')"
            query = query.format(title = x['title'], author = x['author'], community = x['community'], text = x['text'])

        with app.app_context():
            db = get_db()
            db.cursor().execute(query)
            db.commit()
        message = {
            'status' : 200,
            'message' : "Insert successfully"
            }
        resp = jsonify(message)
        resp.status_code = 200

    except sqlite3.Error as e:
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
