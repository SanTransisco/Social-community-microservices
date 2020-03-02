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
    #We need to commit the changes to the database if we want to commit something
    get_db().commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('posts.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#This is ripe for SQL injection attack
@app.route('/api/votes/upvote/<post_id>', methods=['POST'])
def upvote_post(post_id):
    all_posts = query_db('SELECT upvotes FROM posts WHERE id = '+ post_id +';')

    if(len(all_posts) is 0):
        return page_not_found(404)
    else:
        update_upvote_query = 'UPDATE posts SET upvotes = ' + str((int(all_posts[0]['upvotes'])+1)) + ' WHERE id ='+ post_id +';'
        with app.app_context():
            db = get_db()
            db.cursor().execute(update_upvote_query)
            db.commit()

        message = {
            'status' : 200,
            'upvotes' : (int(all_posts[0]['upvotes'])+1),
            'message' : 'Post :' +post_id + ' has been upvoted',
        }
        resp = jsonify(message)
        resp.status_code = 200

        return resp


@app.route('/api/votes/downvote/<post_id>', methods=['POST'])
def downvote_post(post_id):
    all_posts = query_db('SELECT downvotes FROM posts WHERE id = '+ post_id +';')
    if(len(all_posts) is 0):
        return page_not_found(404)
    else:
        update_downvote_query = 'UPDATE posts SET downvotes = ' + str((int(all_posts[0]['downvotes'])+1)) + ' WHERE id ='+ post_id +';'
        with app.app_context():
            db = get_db()
            db.cursor().execute(update_downvote_query)
            db.commit()

        message = {
            'status' : 200,
            'downvotes' : (int(all_posts[0]['downvotes'])+1),
            'message' : 'Post :' +post_id + ' has been downvoted',
        }
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
