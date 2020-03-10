# cpsc449-proj1-microservices

# Authors:
1. Lambert Liu
2. Shijie Feng
3. San Tran
4. Kailie Chang

# Managing processes & Load Balancing
1. If posts.db does not exists.
In the terminal
```
$ flask init
```
2.Then run foreman
```
$ foreman start -c
```
3. Open 2rd terminal:
```
$ ulimit -n 8192 && caddy
```
4. Run the test script

**Before running the test script make sure the post.db has not been modified yet**
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
