-- #Tester.sql

DROP DATABASE IF EXISTS tester1;

CREATE DATABASE tester1;
\c tester1;
CREATE TABLE blue(some_id integer PRIMARY KEY, some_text varchar(40) NOT NULL, hue float);
INSERT INTO blue VALUES (1, 'first', 1.2);
INSERT INTO blue VALUES (2, 'Second', 2.4);
\d blue;
SELECT * FROM blue;


DROP DATABASE IF EXISTS test2;
CREATE DATABASE test2;
\c test2;

