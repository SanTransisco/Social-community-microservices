import requests, json

def view_index():
     url = 'http://127.0.0.1:5000/'
     r = requests.get(url)
     return r.text

def view_all():
    url = 'http://127.0.0.1:5000/posts/all'
    r = requests.get(url)
    return r.text

def view_post():
    url = 'http://127.0.0.1:5000/posts/view'
    with open("json/view_post.json", "r") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    return r.text

def view_by_community():
    url = 'http://127.0.0.1:5000/posts/view_community'
    with open("json/view_by_community.json", "r") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    return r.text

def new_post():
    url = 'http://127.0.0.1:5000/posts/new'
    with open("json/new_post.json", "r") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    return r.text

def new_post_w_url():
    url = 'http://127.0.0.1:5000/posts/new'
    with open("json/new_post _w_url.json", "r") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    return r.text

def delete_post():
    url = 'http://127.0.0.1:5000/posts/delete'
    with open("json/delete_post.json", "r") as f:
        data = json.load(f)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    return r.text

def main():
    print("---------------------------------------------------------\n")
    print("POSTS\n")
    print("---------------------------------------------------------\n")
    print("1. Create a new post with no link\n")
    print(new_post() + '\n')
    print("---------------------------------------------------------\n")
    print("1-1. Create a new post with link\n")
    print(new_post_w_url() + '\n')
    print("---------------------------------------------------------\n")
    print("1-2. Check if created\n")
    print(view_all() + '\n')
    print("---------------------------------------------------------\n")
    print("2. Retrieve an existing post\n")
    print(view_post() + '\n')
    print("---------------------------------------------------------\n")
    print("3. List the n most recent posts to any community\n")
    print(view_all() + '\n')
    print("---------------------------------------------------------\n")
    print("4. List the n most recent posts to a particular community\n")
    print(view_by_community() + '\n')
    print("---------------------------------------------------------\n")
    print("5. Delete an existing post\n")
    print(delete_post() + '\n')
    print("---------------------------------------------------------\n")
    print("5-1. Check if deleted\n")
    print(view_all() + '\n')
    print("---------------------------------------------------------\n")



if __name__=="__main__":
    main()
