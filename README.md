# cpsc449-proj1-microservices

# Authors:
1. Lambert Liu
2. Shijie Feng
3. San Tran
4. Kailie Chang

# Contributions:
- Lambert and Shijie own development and testing of the posting microservice
- San and Kailie own development and testing of the voting microservice
- All group member own the procfile, WSGI server, load balancer, and Tuffix deployment

# Deploying multiple instances of the posts and voting microservice using load-balancing
1. Rename `env.txt` to `.env` to setup the deployment environment
2. If posts.db does not exists.
In the terminal
```
$ flask init
```
3.Then run foreman
```
$ foreman start -c
```
4. Open 2rd terminal:
```
$ ulimit -n 8192 && caddy
```
5. Run the test script in a 3rd Terminal

**Before running the test script make sure the posts.db has not been modified yet**

If posts.db has been modified, delete it and start from step 1 if you want to run the
test script.
```
$ python3 test.py
```
Also to keep the screen clutter down I opted to not display some json data.
If you wish to see the json data type
```
$ python3 test.py -v
```

# Functionalities
## post
1. create a new post
2. delete an existing post
3. retrieve an existing post
4. list all posts from all communities
5. list all posts from a particular community

## votes
1. Upvote a post
2. Downvote a post
3. Report the number of upvotes and downvotes for a post
4. List the n top-scoring posts to any community
5. Given a list of post identifiers, return the list sorted by score.
