import requests, json
'''url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere'
payload = open("request.json")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=payload, headers=headers)'''
def view_index():
     url = 'http://127.0.0.1:5000/'
     r = requests.get(url)
     return r.text

def view_all():
    url = 'http://127.0.0.1:5000/api/posts/all'
    r = requests.get(url)
    return r.text

def view_post():
    url = 'http://127.0.0.1:5000/api/posts/view'
    with open("json/view_post.json", "r") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    return r.text

def view_by_community():
    url = 'http://127.0.0.1:5000/api/posts/view_community'
    with open("json/view_by_community.json", "r") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    return r.text

def new_post():
    url = 'http://127.0.0.1:5000/api/posts/new'
    with open("json/new_post.json", "r") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    return r.text

def delete_post():
    url = 'http://127.0.0.1:5000/api/posts/delete'
    with open("json/delete_post.json", "r") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    return r.text

def main():
    print(view_by_community())


main()
