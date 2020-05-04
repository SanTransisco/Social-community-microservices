import requests, json
import argparse
from feedgen.feed import FeedGenerator

def view_all(_num):
    url = 'http://localhost:2015/posts/all/recent/{num}'
    url = url.format(num = _num)
    r = requests.get(url)
    return r

def view_post(_community, _id):
    url = 'http://localhost:2015/posts/{community}/post/{id}'
    url = url.format(community = _community, id = _id)
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

def create_25_posts_to_any_community():
    resp = view_all(5)
    assert resp.status_code == 200, 'FAIL - Expected status code 200. Got status code' + str(resp.status_code)
    data = json.loads(resp.json()['data'])
    fg = FeedGenerator()
    fg.id('http://localhost:2015/posts/all/recent/25')
    fg.title('Microservice - view all')
    fg.link( href='http://localhost:2015/posts/all/recent/25', rel='alternate' )
    fg.description('The 25 most recent posts to any community')
    fg.language('en')

    for i in data:
        print(type(i))
        fe = fg.add_entry()
        fe.id('http://localhost:2015')
        fe.author(name = i['author'])
        fe.title(i['title'])
        fe.description(i['community'])
        fe.summary(i['date'])
        #fe.content(content=i['text'])



    rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
    fg.rss_file('AllPosts.xml') # Write the RSS feed to a file
    fg.rss_file('AllPosts.rss') # Write the RSS feed to a file

def main():
    parser = argparse.ArgumentParser(description='CPSC 449 project 2')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "Only turn this on if you want to see a lot of json")
    args = parser.parse_args()
    print("---------------------------------------------------------\n")
    print("POSTS\n")
    print("---------------------------------------------------------\n")
    """
        Create posts
    """
    print("\n1. Create a new post with no link\n")
    print("a. Create the post")
    resp = new_post("CSUF-CPSC449", "json/new_post1.json")
    assert resp.status_code == 201, 'FAIL - Expected status code 201. Got status code' + str(resp.status_code)
    print(resp)
    resp = new_post("CSUF-CPSC449", "json/new_post2.json")
    assert resp.status_code == 201, 'FAIL - Expected status code 201. Got status code' + str(resp.status_code)
    print(resp)
    resp = new_post("CSUF-CPSC449", "json/new_post3.json")
    assert resp.status_code == 201, 'FAIL - Expected status code 201. Got status code' + str(resp.status_code)
    print(resp)
    resp = new_post("CSUF-CPSC449", "json/new_post4.json")
    assert resp.status_code == 201, 'FAIL - Expected status code 201. Got status code' + str(resp.status_code)
    print(resp)
    resp = new_post("CSUF-CPSC449", "json/new_post5.json")
    assert resp.status_code == 201, 'FAIL - Expected status code 201. Got status code' + str(resp.status_code)
    print(resp)
    resp = new_post("CSUF-CPSC449", "json/new_post6.json")
    assert resp.status_code == 201, 'FAIL - Expected status code 201. Got status code' + str(resp.status_code)
    print(resp)
    resp = new_post("CSUF-CPSC449", "json/new_post7.json")
    assert resp.status_code == 201, 'FAIL - Expected status code 201. Got status code' + str(resp.status_code)
    print(resp)

    print("\n2. Create a new post with a link\n")
    resp = new_post("CSUF-CPSC449", "json/new_post_w_url1.json")
    assert resp.status_code == 201, 'FAIL - Expected status code 201. Got status code' + str(resp.status_code)
    print(resp)
    resp = new_post("Mechanical_Keyboards", "json/new_post_w_url2.json")
    assert resp.status_code == 201, 'FAIL - Expected status code 201. Got status code' + str(resp.status_code)
    print(resp)
    resp = new_post("BTSs", "json/new_post_w_url3.json")
    assert resp.status_code == 201, 'FAIL - Expected status code 201. Got status code' + str(resp.status_code)
    print(resp)

    """
        LIST N MOST RECENT POST FOR ALL COMMUNITIES
    """
    print( "\n3 - List the n most recent posts to any community\n")
    create_25_posts_to_any_community()
    """
    print( " n = 5 ")
    resp = view_all(5)
    assert resp.status_code == 200, 'FAIL - Expected status code 200. Got status code' + str(resp.status_code)
    #assert len(resp.json()['data']) == 5 , "FAIL - Expected the length of the json to be 5. Instead received" + str(len(resp.json()["data"]))
    print("PASS - view all last 5 posts returned 5 posts")
    if(args.verbose):
        print(resp.json()['data'])


        LIST N MOST RECENT POST FOR A PARTICULAR COMMUNITY

    print( "\n4 - List the n most recent posts to a particular community\n")
    print( " In this case the particular community is CSUF-CPSC449")
    print( " n = 5 ")
    resp = view_by_community("CSUF-CPSC449","5")
    assert resp.status_code == 200, 'FAIL - Expected status code 200. Got status code' + str(resp.status_code)
    #assert len(resp.json()['data']) == 5 , "FAIL - Expected the length of the json to be 5. Instead received" + str(len(resp.json()["data"]))
    print("PASS - view all last 5 posts returned 5 posts")
    if(args.verbose):
        print(resp.json()['data'])

    """


if __name__=="__main__":
    main()
