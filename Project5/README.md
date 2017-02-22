# Item Catalog


### How to run

This simple web application uses GitHub for authorization and authentication.  To simulate security best practices, the API keys are not in the main application file or hard-coded.  
However, to facilitate grading, a shell script, `export_keys.sh`, is available to export API keys 
to server environment variables.

```
  $ git clone https://github.com/mr-karan/Udacity-FullStack-ND004
  $ cd Udacity-FullStack-ND004/Project5/
  $ virtualenv venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt
```


# Project 5 FSND

### Setup Project

```bash
  $ git clone https://github.com/mr-karan/Udacity-FullStack-ND004
  $ cd Udacity-FullStack-ND004/Project5/
  $ virtualenv venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt
```

### Create Database
```bash
   $ psql 
   $ CREATE DATABASE udacity_song;
   $ \q
```

### Running
- (Optional) Obtain your own GitHub API keys by [registering a new application](https://github.com/settings/applications).  Ensure you add `localhost:5000/github-callback` as the authorization callback URL.
- `source export_keys.sh`.
- `python application.py`.
- `localhost:5000`.  The first-time run of the server will initialize the database with sample music data.




### JSON Endpoint is available at

[http://localhost:5000/catalog/api/artists](http://localhost:5000/catalog/api/artists)

