import flask
from flask import  g, jsonify, request
import sqlite3

app = flask.Flask(__name__)

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('posts.db')
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

@app.route('/votes/upvote/<post_id>', methods=['POST'])
def upvote_post(post_id):
    all_posts = query_db('SELECT upvote FROM posts WHERE id = '+ post_id +';')

    if(len(all_posts) is 0):
        return page_not_found(404)
    else:
        update_upvote_query = "UPDATE posts SET upvote = {upvote_new} WHERE id = {post_id};"
        update_upvote_query=update_upvote_query.format(upvote_new = all_posts[0]['upvote']+1, post_id = post_id)
        with app.app_context():
            db = get_db()
            db.cursor().execute(update_upvote_query)
            db.commit()

        message = {
            'status' : 200,
            'upvotes' : (int(all_posts[0]['upvote'])+1),
            'message' : 'Post :' +post_id + ' has been upvoted',
        }
        resp = jsonify(message)
        resp.status_code = 200

        return resp


@app.route('/votes/downvote/<post_id>', methods=['POST'])
def downvote_post(post_id):
    all_posts = query_db('SELECT downvote FROM posts WHERE id = '+ post_id +';')
    if(len(all_posts) is 0):
        return page_not_found(404)
    else:
        update_downvote_query = "UPDATE posts SET downvote = {downvote_new} WHERE id = {post_id};"
        update_upvote_query.format(upvote_new = all_posts[0]['downvote']+1, post_id = post_id)
        with app.app_context():
            db = get_db()
            db.cursor().execute(update_downvote_query)
            db.commit()

        message = {
            'status' : 200,
            'downvotes' : (int(all_posts[0]['downvote'])+1),
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
