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
    all_posts = query_db('SELECT upvote, net_score FROM posts WHERE id = '+ post_id +';')

    if(len(all_posts) is 0):
        return page_not_found(404)
    else:
        update_upvote_query = "UPDATE posts SET upvote = {upvote_new}, net_score = {net_score_new} WHERE id = {post_id};"
        update_upvote_query=update_upvote_query.format(upvote_new = all_posts[0]['upvote']+1,
                                                        net_score_new = all_posts[0]['net_score'] + 1, post_id = post_id)
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
    all_posts = query_db('SELECT downvote, net_score FROM posts WHERE id = '+ post_id +';')
    if(len(all_posts) is 0):
        return page_not_found(404)
    else:
        update_downvote_query = "UPDATE posts SET downvote = {downvote_new}, net_score = {net_score_new} WHERE id = {post_id};"
        update_downvote_query=update_downvote_query.format(downvote_new = all_posts[0]['downvote']+1,
                                                            net_score_new = all_posts[0]['net_score'] - 1, post_id = post_id)
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

# reports the number of upvotes and downvotes for a post
@app.route('/votes/show_votes/<post_id>', methods=['GET'])
def show_votes(post_id):
    all_posts = query_db('SELECT upvote, downvote FROM posts WHERE id = '+ post_id +';')

    if(len(all_posts) is 0):
        return page_not_found(404)
    else:
        print(all_posts[0].keys())
        message = {
            'status' : 200,
            'total upvotes' : (int(all_posts[0]['upvote'])),
            'total downvotes': (int(all_posts[0]['downvote'])),
            'message' : 'Post: ' + post_id + ' votes reported'
        }
        resp = jsonify(message)
        resp.status_code = 200

        return resp

# list the n top-scoring posts to any community
@app.route('/votes/all/top/<n_posts>', methods=['GET'])
def top_posts(n_posts):
    try:
        query = "SELECT * FROM posts ORDER BY net_score DESC LIMIT {post_num};"

        query = query.format(post_num = n_posts)
        data = query_db(query)

        message = {
            'status' : 200,
            'data' : data,
            'message': 'These are the top scoring posts'
        }
        resp = jsonify(message)
        resp.status_code = 200

    except sqlite3.Error as e:
        message = {
            'status' : 400,
            'message' : "Bad Request, Posts not found",
        }
        resp = jsonify(message)
        resp.status_code = 400

    return resp

# given a list of post identifiers, return the list sorted by score
@app.route('/votes/list/top', methods=['POST'])
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

        query = query + " ORDER BY net_score;"
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


@app.errorhandler(404)
def page_not_found(e):
    message = {
        'status' : 404,
        'message' : '404 not found',
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
