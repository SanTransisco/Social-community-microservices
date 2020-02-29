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
    return render_template('index.html')

@app.route('/api/posts/all', methods=['GET'])
def all_posts():
    all_posts = query_db('SELECT author, community, title FROM posts;')
    return jsonify(all_posts)

@app.route('/api/posts/new_post')
def new_posts_form():
    return render_template('post_form.html')

@app.route('/api/posts/new_post', methods=['POST'])
def new_post():
    author = request.form['Author']
    community = request.form['Community']
    title = request.form['Title']
    text = request.form['Text']
    sql = "INSERT INTO posts(title, author, community, text) VALUES ('%s','%s','%s','%s')" % (title,author,community,text)
    with app.app_context():
        db = get_db()
        db.cursor().execute(sql)
        db.commit()
    return render_template('index.html')



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()
