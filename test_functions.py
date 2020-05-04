import requests, json
def view_all(_num):
    url = 'http://localhost:2015/posts/all/recent/{num}'
    url = url.format(num = _num)
    r = requests.get(url)
    return r

def view_post(_community, _id):
    url = 'http://localhost:2015/posts/{community}/post/{id}'
    url = url.format(community = _community, id = _id)
    print(url)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    return r

def view_by_community(_community, _num):
    url = 'http://localhost:2015/posts/{community}/recent/{num}'
    url = url.format(community = _community, num = _num)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    return r

def new_post(_community, post):
    url = 'http://localhost:2015/posts/{community}/new'
    url = url.format(community = _community)
    with open(post, "r") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    return r

def delete_post(_community, _id):
    url = 'http://localhost:2015/posts/{community}/post/{id}'
    url = url.format(community = _community, id = _id)
    headers = {'content-type': 'application/json'}
    r = requests.delete(url, headers=headers)
    return r

def upvote_post(_community, _id):
    url = 'http://localhost:2015/votes/{community}/post/{id}/upvote'
    url = url.format(community = _community, id = _id)
    headers = {'content-type': 'application/json'}
    r = requests.patch(url, headers=headers)
    return r

def downvote_post(_community, _id):
    url = 'http://localhost:2015/votes/{community}/post/{id}/downvote'
    url = url.format(community = _community, id = _id)
    headers = {'content-type': 'application/json'}
    r = requests.patch(url, headers=headers)
    return r

def get_score(_community, _id):
    url = 'http://localhost:2015/votes/{community}/post/{id}/score'
    url = url.format(community = _community, id = _id)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    return r

def top_posts(_num):
    url = 'http://localhost:2015/votes/all/top/{num}'
    url = url.format(num = _num)
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    return r

def order_posts(json_obj):
    url = 'http://localhost:2015/votes/list/top'
    headers = {'content-type': 'application/json'}
    r = requests.get(url, json = json_obj, headers=headers)
    return r
