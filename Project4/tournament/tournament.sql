-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  win INT REFERENCES players(id),
  lost INT REFERENCES players(id)
);

INSERT INTO players (name) VALUES ('LeBron');
INSERT INTO players (name) VALUES ('Kevin');
INSERT INTO players (name) VALUES ('Stephen');

INSERT INTO matches (win, lost) VALUES (2, 1);
INSERT INTO matches (win, lost) VALUES (1, 3);
INSERT INTO matches (win, lost) VALUES (3, 2);

CREATE VIEW results AS
  SELECT players.id, players.name, winnings.n AS winnings, count.n AS matches_played
      FROM players, winnings, count
      WHERE players.id = winnings.id and players.id = count.id
      ORDER BY winnings DESC;

CREATE VIEW winnings AS
  SELECT players.id, count(matches.win) AS n FROM players
  LEFT JOIN matches ON players.id =  matches.win
  GROUP BY players.id;

CREATE VIEW count AS
  SELECT players.id, count(matches.win) AS n FROM players
  LEFT JOIN matches ON players.id = matches.win
  OR players.id = matches.lost
  GROUP BY players.id;
