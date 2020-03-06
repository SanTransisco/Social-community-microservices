-- $ sqlite3 posts.db < posts.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id INTEGER primary key,
    title VARCHAR,
    author VARCHAR,
    community VARCHAR,
    text VARCHAR,       
    UNIQUE(community, author, title)
);
INSERT INTO posts(title, author, community, text) VALUES('Sample post','Lambert Liu','CSUF-CPSC449','This is a sampe from defualt sql.');
INSERT INTO posts(title, author, community, text) VALUES('1','1','1','1');
COMMIT;
