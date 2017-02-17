# Project 4 FSND

### Setup Project

```bash
  $ git clone https://github.com/mr-karan/Udacity-FullStack-ND004
  $ cd Udacity-FullStack-ND004/Project4/
  $ virtualenv venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt
```

### Create Database
```bash
   $ cd tournament/
   $ psql 
   $ CREATE DATABASE tournament;
   $ \q
   $ psql -dtournament < tournament.sql
```

### Running Tests
```bash
    $ python tournament_test.py
```
