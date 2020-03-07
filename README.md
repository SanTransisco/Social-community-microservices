# cpsc449-proj1-microservices

# Authors:
1. Lambert Liu
2. Shijie Feng
3. San Tran
4. Kailie Chang

# How To Run using flask:
1. Rename 'env.txt' to '.env'
2. Open 1st terminal: 
    - $ flask init
    - $ flask run
3. Open 2rd terminal:
    - $ python3 test.py

# Managing processes & Load Balancing
1. Open 1st terminal: (make sure closed flask run terminal)
    - $ foreman start -c
2. Open 2rd terminal: 
    - $ ulimit -n 8192 && caddy

# Functionalities 
## votes
1. create a new post
2. delete an existing post
3. retrieve an existing post
4. list all posts from all communities
5. list all posts from a particular community

