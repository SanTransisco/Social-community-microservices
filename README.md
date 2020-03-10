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

# Before ALL TYPE OF running scripts:
PLEASE MAKE SURE OPEN TERMINAL AND RUN:
    - $ flask init
    
# How To Run using flask:
1. Rename 'env.txt' to '.env'
2. Open 1st terminal: 
    - $ flask run
3. Open 2rd terminal:
    - $ python3 test.py
4. Test result will output on terminal, also, output json will be stored in output_json folder

# Running via gunicorn
1. Open terminal: (make sure cloded flask run terminal)
    - $ gunicorn3 -b localhost:5000 -w 3 api:app

# Managing processes & Load Balancing
1. Open 1st terminal: (make sure closed flask run terminal)
    - $ foreman start -c
2. Open 2rd terminal: 
    - $ ulimit -n 8192 && caddy

# Functionalities 
## Posting microservices
1. create a new post
2. delete an existing post
3. retrieve an existing post
4. list all posts from all communities
5. list all posts from a particular community

## Voting microsevice
1. Upvote a post
2. Downvote a post
3. Report the number of upvotes and downvotes for a post
4. LIst the n top-scoring posts to any community
5. Given a list of post identifiers, return the list sorted by score
