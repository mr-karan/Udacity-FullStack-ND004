#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("enginename=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    engine = connect()
    cur = engine.cursor()
    cur.execute("DELETE FROM matches;")
    engine.commit()
    engine.close()


def deletePlayers():
    """Remove all the player records from the database."""
    engine = connect()
    cur = engine.cursor()
    cur.execute("DELETE FROM players;")
    engine.commit()
    engine.close()


def countPlayers():
    """Returns the number of players currently registered."""
    engine = connect()
    cur = engine.cursor()
    cur.execute("SELECT count(*) AS count FROM players;")
    player_count = cur.fetchone()
    engine.close()
    return player_count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    engine = connect()
    cur = engine.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    engine.commit()
    engine.close()


def playerresults():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    engine = connect()
    cur = engine.cursor()
    cur.execute("SELECT * FROM results")
    player_results = cur.fetchall()
    engine.close()

    return player_results


def reportMatch(win, lost):
    """Records the outcome of a single match between two players.
    Args:
      win:  the id number of the player who won
      lost:  the id number of the player who lost
    """
    engine = connect()
    cur = engine.cursor()
    cur.execute("INSERT INTO matches (win, lost) VALUES ( \
        {0}, {1});".format(win, lost))
    engine.commit()
    engine.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the results.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    engine = connect()
    cur = engine.cursor()
    cur.execute("SELECT player.id, player.name, opponent.id, opponent.name \
        FROM results player, results opponent \
        WHERE player.wins = opponent.wins AND player.id < opponent.id;")
    pairs = cur.fetchall()
    engine.close()
    print pairs
    return pairs
