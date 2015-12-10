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
CREATE TABLE players(id SERIAL PRIMARY KEY, name varchar(50), wins integer DEFAULT 0, matches integer DEFAULT 0);
CREATE TABLE matches(winner integer REFERENCES players(id), loser integer REFERENCES players(id));
DROP DATABASE IF EXISTS test2;
CREATE DATABASE test2;
\c test2;

