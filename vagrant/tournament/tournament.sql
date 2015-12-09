-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;
CREATE TABLE players(id integer PRIMARY KEY, name varchar(50));
CREATE TABLE matches(id1 integer REFERENCES players(id), id1_win bool, id2 integer REFERENCES players(id), id2_win integer, round integer);

DROP DATABASE IF EXISTS test2;
CREATE DATABASE test2;
\c test2;

