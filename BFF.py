import flask
import requests
import json
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

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

    fg = FeedGenerator()
    fg.id(url)
    fg.title('Microservice - view community')
    fg.link(href=url, rel='alternate')
    fg.description('The 25 most recent posts to a particular community')
    fg.language('en')

    for i in final_data:
        fe = fg.add_entry()
        fe.id(i['post_id'])
        fe.author({'name': i['author'], 'email':""})
        fe.title(i['title'])
        fe.description(i['community'])
        date = datetime.fromtimestamp(i['date'])
        date = date.replace(tzinfo=pytz.utc)
        fe.published(date)
        fe.content(content=i['text'])
        if 'url' in i:
            fe.source(url=i['url'], title=i['title'])

    rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
    resp = flask.Response(rssfeed, mimetype='text/xml', status = 200, content_type = 'application/rss+xml; charset=UTF-8')
    return resp

# gets the 25 most recent posts to any community
@app.route('/BFF/All/recent', methods=['GET'])
def all_recent_posts():
    url = 'http://localhost:2015/posts/all/recent/{num}'
    url = url.format(num = 25)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    final_data = data['data']

    fg = FeedGenerator()
    fg.id(url)
    fg.title('Microservice - view all')
    fg.link( href=url, rel='alternate' )
    fg.description('The 25 most recent posts to any community')
    fg.language('en')

    #This is genating the RSS feeds
    for i in final_data:
        fe = fg.add_entry()
        fe.id(i['post_id'])
        fe.author({'name': i['author'], 'email':""})
        fe.title(i['title'])
        fe.description(i['community'])
        date = datetime.fromtimestamp(i['date'])
        date = date.replace(tzinfo=pytz.utc)
        print(date)
        fe.published(date)
        fe.content(content=i['text'])
        if 'url' in i:
            fe.source(url=i['url'], title=i['title'])

    rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
    resp = flask.Response(rssfeed, mimetype='text/xml', status = 200, content_type = 'application/rss+xml; charset=UTF-8')
    return resp

# gets the top 25 posts to a particular community, sorted by score
@app.route('/BFF/<_community>/top', methods=['GET'])
def top_posts(_community):
    url = 'http://localhost:2015/votes/{community}/top/{num}'
    url = url.format(community = _community, num = 25)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    post_id = data['data']

    fg = FeedGenerator()
    fg.id(url)
    fg.title('Microservice - view top community posts')
    fg.link( href=url, rel='alternate' )
    fg.description('The 25 top posts to a particular community')
    fg.language('en')

    for i in post_id:
        url = 'http://localhost:2015/posts/{community}/post/{id}'
        url = url.format(community = _community, id = i)
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        data = r.json()
        post_info = data['data']

        fe = fg.add_entry()
        fe.id(post_info['post_id'])
        fe.author({'name': post_info['author'], 'email':""})
        fe.title(post_info['title'])
        fe.description(post_info['community'])
        date = datetime.fromtimestamp(post_info['date'])
        date = date.replace(tzinfo=pytz.utc)
        print(date)
        fe.published(date)
        fe.content(content=post_info['text'])
        if 'url' in post_info:
            fe.source(url=post_info['url'], title=post_info['title'])

    rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
    resp = flask.Response(rssfeed, mimetype='text/xml', status = 200, content_type = 'application/rss+xml; charset=UTF-8')
    return resp

# gets the top 25 posts to any community, sorted by score
@app.route('/BFF/All/top', methods=['GET'])
def all_top_posts():
    url = 'http://localhost:2015/votes/all/top/{num}'
    url = url.format(num = 25)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    post_id = data['data']

    fg = FeedGenerator()
    fg.id(url)
    fg.title('Microservice - view all top posts')
    fg.link( href=url, rel='alternate' )
    fg.description('The 25 top posts to any community')
    fg.language('en')

    for i in post_id:
        url = 'http://localhost:2015/posts/all/post/{id}'
        url = url.format(id = i)
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        data = r.json()
        post_info = data['data']

        fe = fg.add_entry()
        fe.id(post_info['post_id'])
        fe.author({'name': post_info['author'], 'email':""})
        fe.title(post_info['title'])
        fe.description(post_info['community'])
        date = datetime.fromtimestamp(post_info['date'])
        date = date.replace(tzinfo=pytz.utc)
        print(date)
        fe.published(date)
        fe.content(content=post_info['text'])
        if 'url' in post_info:
            fe.source(url=post_info['url'], title=post_info['title'])

    rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
    resp = flask.Response(rssfeed, mimetype='text/xml', status = 200, content_type = 'application/rss+xml; charset=UTF-8')
    return resp

# IN PROGRESS
# gets the top 25 posts to any community, ranking using "hot ranking" alg.
@app.route('/BFF/All/hot', methods=['GET'])
def all_hot_posts():
    url = 'http://localhost:2015/votes/all/hot/{num}'
    url = url.format(num = 25)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()
    post_id = data['data']

    fg = FeedGenerator()
    fg.id(url)
    fg.title('Microservice - view all hot posts')
    fg.link( href=url, rel='alternate' )
    fg.description('The 25 hot posts to any community')
    fg.language('en')

    for i in post_id:
        url = 'http://localhost:2015/posts/all/post/{id}'
        url = url.format(id = i)
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        data = r.json()
        post_info = data['data']

        fe = fg.add_entry()
        fe.id(post_info['post_id'])
        fe.author({'name': post_info['author'], 'email':""})
        fe.title(post_info['title'])
        fe.description(post_info['community'])
        date = datetime.fromtimestamp(post_info['date'])
        date = date.replace(tzinfo=pytz.utc)
        print(date)
        fe.published(date)
        fe.content(content=post_info['text'])
        if 'url' in post_info:
            fe.source(url=post_info['url'], title=post_info['title'])

    rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
    resp = flask.Response(rssfeed, mimetype='text/xml', status = 200, content_type = 'application/rss+xml; charset=UTF-8')
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
