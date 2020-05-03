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

@app.route('/BFF/<_community>/recent', methods=['GET'])
def new_post(_community,_post_id):
    pass


@app.route('/BFF/All/recent', methods=['GET'])
def new_post(_community,_post_id):
    pass

@app.route('/BFF/<_community>/top', methods=['GET'])
def new_post(_community,_post_id):
    pass


@app.route('/BFF/All/top', methods=['GET'])
def new_post(_community,_post_id):
    pass

@app.route('/BFF/All/hot', methods=['GET'])
def new_post(_community,_post_id):
    pass

@app.errorhandler(404)
def page_not_found(e):
    message = {
        'status' : 404,
        'message' : '404 not found',
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
