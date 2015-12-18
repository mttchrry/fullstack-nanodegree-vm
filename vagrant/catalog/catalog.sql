-- catalog definition of tables

DROP DATABASE IF EXISTS catalog;

CREATE DATABASE catalog;
\c catalog;
CREATE TABLE players(id SERIAL PRIMARY KEY, name varchar(50));
CREATE TABLE matches(winner integer REFERENCES players(id), loser integer REFERENCES players(id));

