# cpsc449-proj1-microservices

# Authors:
1. Lambert Liu
2. Shijie Feng
3. San Tran
4. Kailie Chang

# Contributions:
- Lambert and Shijie own development and testing of the posting microservice, BFF recent functionalities, xml generation
- San and Kailie own development and testing of the voting microservice, BFF top and hot functionalities
- All group member own the procfile, WSGI server, load balancer, and Tuffix deployment

# Deploying multiple instances of the posts and voting microservice using load-balancing
1. Rename `env.txt` to `.env` to setup the deployment environment
2. Start DynamoDB on your computer open a command prompt window,
navigate to the directory where you extracted DynamoDBLocal.jar, and enter the following command.
```
$ java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
```
3.Then open another terminal instance in the project folder and run foreman
```
$ foreman start -c
```
4. Open yet another terminal instance and type the command:
```
$ ulimit -n 8192 && caddy
```
5. IN YET ANOTHER terminal instance type the command:
```
$ flask run
```
We are under the belief that we can run the BFF as another set of microservices using foreman.
However, for the sake of not having this potentially blow up we will run it using flask.
6. And open the last instance of the terminal, and type the command:
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

## BFF
1. The 25 most recent posts to a particular community
2. The 25 most recent posts to any community
3. The top 25 posts to a particular community, sorted by score
4. The top 25 posts to any community, sorted by score
5. The hot 25 posts to any community, ranked using Reddit’s “hot ranking” algorithm.
