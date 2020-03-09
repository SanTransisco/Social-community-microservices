-- $ sqlite3 posts.db < posts.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id INTEGER primary key ,
    title VARCHAR,
    author VARCHAR,
    community VARCHAR,
    text VARCHAR,
    url VARCHAR DEFAULT NULL,
    upvote INTEGER DEFAULT 0,
    downvote INTEGER DEFAULT 0,
    time DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(community, author, title)
);
INSERT INTO posts(title, author, community, url, text) VALUES('Sample post','Lambert Liu','CSUF-Admission', 'https://sites.google.com/view/cpsc-449','This is a sampe from defualt sql.');
COMMIT;
