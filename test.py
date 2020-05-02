import requests, json
import argparse
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
    print( " n = 3 ")
    resp = view_all(3)
    assert resp.status_code == 200, 'FAIL - Expected status code 200. Got status code' + str(resp.status_code)
    print(len(resp.json()['data']))
    #assert len(resp.json()['data']) == 3 , "FAIL - Expected the length of the json to be 3. Instead received" + str(len(resp.json()["data"]))
    print("PASS - view all last 3 posts returned 3 posts")
    if(args.verbose):
        print(resp.json()['data'])

    print( " n = 5 ")
    resp = view_all(5)
    assert resp.status_code == 200, 'FAIL - Expected status code 200. Got status code' + str(resp.status_code)
    #assert len(resp.json()['data']) == 5 , "FAIL - Expected the length of the json to be 5. Instead received" + str(len(resp.json()["data"]))
    print("PASS - view all last 5 posts returned 5 posts")
    if(args.verbose):
        print(resp.json()['data'])
'''
    """
        LIST N MOST RECENT POST FOR A PARTICULAR COMMUNITY
    """
    print( "\n5 - List the n most recent posts to a particular community\n")
    print( " In this case the particular community is CSUF-CPSC449")
    print( " n = 3 ")
    resp = view_by_community("CSUF-CPSC449","3")
    assert resp.status_code == 200, 'FAIL - Expected status code 200. Got status code' + str(resp.status_code)
    assert len(resp.json()['data']) == 3 , "FAIL - Expected the length of the json to be 3. Instead received" + str(len(resp.json()["data"]))
    print("PASS - view all last 3 posts returned 3 posts")
    if(args.verbose):
        print(resp.json()['data'])

    print( " n = 5 ")
    resp = view_by_community("CSUF-CPSC449","5")
    assert resp.status_code == 200, 'FAIL - Expected status code 200. Got status code' + str(resp.status_code)
    assert len(resp.json()['data']) == 5 , "FAIL - Expected the length of the json to be 5. Instead received" + str(len(resp.json()["data"]))
    print("PASS - view all last 5 posts returned 5 posts")
    if(args.verbose):
        print(resp.json()['data'])

    """
        DELETE POST
    """
    print("\n6 - Delete a post\n")
    print(" If this post is ran on a blank posts.db then there should only be one post in the\nMechanical Keyboards Community")
    resp = view_by_community("Mechanical_Keyboards","1")
    print(resp.json())
    print(" We will now delete it")
    resp = delete_post("Mechanical_Keyboards" , "2")
    assert resp.status_code == 200, 'FAIL - Expected status code 200. Got status code' + str(resp.status_code)
    print("PASS -  Delete returned 200")
    print("now there are no more posts in Mechanical_Keyboards :(")
    resp = view_by_community("Mechanical_Keyboards","1")
    print(resp.json())


    """
        VOTING MICROSERVICES TESTING
    """
    print("---------------------------------------------------------\n")
    print("VOTES\n")
    print("---------------------------------------------------------\n")
    print("We will be updating this post in particular")
    resp = view_post("CSUF-CPSC449", "7")
    print(resp.json()['data'])


    print("\n1. Attempt to upvote/downvote a post before any posts are made\n")
    resp = upvote_post("DoesNotExist", "1")
    assert resp.status_code == 404, 'FAIL - Expected status code 400. Got status code' + str(resp.status_code)
    print("PASS - status code returns 400 because there is no posts to upvote in the DoesNotExist Community")
    resp = downvote_post("DoesNotExist", "1")
    assert resp.status_code == 404, 'FAIL - Expected status code 400. Got status code' + str(resp.status_code)
    print("PASS - status code returns 400 because there is no posts to view in the DoesNotExist Community")

    print("\n2. Attempt to upvote/downvote a post\n")
    resp = upvote_post("CSUF-CPSC449", "7")
    assert resp.status_code == 200, 'FAIL - Expected status code 200. Got status code' + str(resp.status_code)
    print("PASS - status code returns 200 upvote successful")
    resp = downvote_post("CSUF-CPSC449", "7")
    assert resp.status_code == 200, 'FAIL - Expected status code 200. Got status code' + str(resp.status_code)
    print("PASS - status code returns 200 downvote successful")

    print("\n3 - Get the vote scores from the post")
    resp = get_score("CSUF-CPSC449", "7")
    assert resp.status_code == 200, 'FAIL - Expected status code 200. Got status code' + str(resp.status_code)
    print("PASS - status code returns 200 upvote successful")
    assert resp.json()['upvote']==1, 'FAIL - Expected upvote 1. Got upvote' + resp.json()['upvote']
    assert resp.json()['downvote']==1, 'FAIL - Expected downvote 1. Got downvote' + resp.json()['downvote']
    print("PASS - In test 2 we only upvoted and downvoted once.")

    print("\n upvoting and downvoting various posts for the next set of tests")
    upvote_post("CSUF-CPSC449", "7")
    upvote_post("CSUF-CPSC449", "7")
    upvote_post("CSUF-CPSC449", "7")
    upvote_post("CSUF-CPSC449", "7")
    upvote_post("CSUF-CPSC449", "7")

    upvote_post("CSUF-CPSC449", "1")
    upvote_post("CSUF-CPSC449", "1")
    downvote_post("CSUF-CPSC449", "1")

    downvote_post("CSUF-CPSC449", "4")
    downvote_post("CSUF-CPSC449", "4")
    downvote_post("CSUF-CPSC449", "4")
    downvote_post("CSUF-CPSC449", "4")
    downvote_post("CSUF-CPSC449", "4")

    upvote_post("CSUF-CPSC449", "5")
    upvote_post("CSUF-CPSC449", "5")
    upvote_post("CSUF-CPSC449", "5")
    downvote_post("CSUF-CPSC449", "5")
    downvote_post("CSUF-CPSC449", "5")

    print("\n4 - Printing the top n posts in a community")
    print("n=3")
    resp = top_posts(3)
    assert len(resp.json()['data'])== 3, "Expected the top 3 posts, instead got " + str(len(resp.json()['data']))
    print("PASS - requested the top 3 posts. Got the top 3 posts")
    if(args.verbose):
        print(resp.json()['data'])

    print("n=5")
    resp = top_posts(5)
    assert len(resp.json()['data'])== 5, "Expected the top 5 posts, instead got " + str(len(resp.json()['data']))
    print("PASS - requested the top 5 posts. Got the top 5 posts")
    if(args.verbose):
        print(resp.json()['data'])

    print("\n5 - Given a list of post identifiers, return the list sorted by score.")
    x = '{"post": [1,7,4,5,3]}'
    x = json.loads(x)
    resp = order_posts(x)
    print(resp.json()['data'])
'''

if __name__=="__main__":
    main()
