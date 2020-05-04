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
def recent_posts(_community):
    url = 'http://localhost:2015/posts/{comm}/recent/{num}'
    url = url.format(comm = _community,num = 25)
    r = requests.get(url)
    data=r.json()
    final_data = data['data']
    message = {
        'status' : 200,
        'data' : final_data,
        'message': '200 ok'
    }
    resp = jsonify(message)
    resp.status_code = 200


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
