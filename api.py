import flask
from flask import render_template, g, jsonify, request
import sqlite3
app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
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
        'message' : 'Welcome',
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/api/posts/all', methods=['GET'])
def all_posts():
    data = query_db('SELECT author, community, title FROM posts ORDER BY id DESC;')
    return jsonify(data)

@app.route('/api/posts/view', methods=['GET'])
def view_post():
    query_parameters = request.args
    title = query_parameters.get('title')
    author = query_parameters.get('author')
    community = query_parameters.get('community')
    query = "SELECT * FROM posts WHERE title = "+ title +" AND author = "+ author + " AND community ="+ community+";"
    data = query_db(query)
    return jsonify(data)

@app.route('/api/posts/view_community', methods=['GET'])
def view_community():
    query_parameters = request.args
    community = query_parameters.get('community')
    query = "SELECT * FROM posts WHERE community=" +community + ";"
    if not community:
        return page_not_found(404)

    data = query_db(query)
    return jsonify(data)


@app.route('/api/posts/delete', methods=['GET','DELETE'])
def delete_post():
    query_parameters = request.args
    title = query_parameters.get('title')
    author = query_parameters.get('author')
    community = query_parameters.get('community')
    sql = "DELETE FROM posts WHERE title = "+ title +" AND author = "+ author + " AND community ="+ community+";"
    db = get_db()
    db.execute(sql)
    db.commit()

    message = "Delete successfully from DB"
    resp = jsonify(message)
    resp.status_code = 200
    return resp


@app.route('/api/posts/new', methods=['GET'])
def new_post():
    query_parameters = request.args
    title = query_parameters.get('title')
    author = query_parameters.get('author')
    community = query_parameters.get('community')
    text = query_parameters.get('text')
    sql = "INSERT INTO posts(title, author, community, text) VALUES (%s,%s,%s,%s)" % (title,author,community,text)
    print(sql)
    with app.app_context():
        db = get_db()
        db.cursor().execute(sql)
        db.commit()
    message = "Insert successfully"
    resp = jsonify(message)
    resp.status_code = 200
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
