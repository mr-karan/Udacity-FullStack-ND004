import os
from flask import Flask, flash, g, jsonify, redirect, render_template,\
    request, session, url_for
from flask.ext.github import GitHub
from database_setup import Base, User, Artist, Song
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


app = Flask(__name__)
app.secret_key = "thisisasecretkey"


if os.environ['GITHUB_CLIENT_ID'] and os.environ['GITHUB_CLIENT_SECRET']:
    app.config['GITHUB_CLIENT_ID'] = os.environ['GITHUB_CLIENT_ID']
    app.config['GITHUB_CLIENT_SECRET'] = os.environ['GITHUB_CLIENT_SECRET']

else:
    app.config['GITHUB_CLIENT_ID'] = None
    app.config['GITHUB_CLIENT_SECRET'] = None

github = GitHub(app)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))
db_session = DBSession()

repo_uri = 'https://github.com/mr-karan/Udacity-FullStack-ND004'
base_uri = '/catalog/'
api_uri = base_uri + 'api/'


# oauth
@app.route('/login')
def login():
    """ login route/routine """
    if app.config['GITHUB_CLIENT_ID'] and app.config['GITHUB_CLIENT_SECRET']:
        return github.authorize(
            redirect_uri=url_for(
                'authorized',
                _external=True))
    else:
        flash('missing Github API Client ID.', 'warning')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('access_token', None)
    flash('Logged Out.', 'success')
    return redirect(url_for('index'))


@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next')
    if oauth_token is None:
        flash('Authorization failed.', 'danger')
        return redirect(next_url)

    user = db_session.query(User).filter_by(access_token=oauth_token).first()
    if user is None:
        user = User(oauth_token)
        db_session.add(user)

    user.access_token = oauth_token
    db_session.commit()

    session['user_id'] = user.id
    session['user_token'] = user.access_token

    flash('You\'re logged in! ', 'success')
    return redirect(url_for('index'))


# helper functions
def base_query():
    """ returns the full list of artists and songs """
    artists = db_session.query(Artist).all()
    songs = db_session.query(Song).all()
    return artists, songs


def parse_song_form(form):
    """ returns a new Song object from submitted form data POST requests """
    form = dict(form)
    if 'song-featured' not in form:
        form['song-featured'] = [False]
    else:
        form['song-featured'] = [True]
    song = Song(name=form['song-name'][0],
                song_url=form['song-url'][0],
                description=form['song-description'][0],
                featured=form['song-featured'][0],
                artist_id=form['song-artist'][0])
    return song


def authenticated():
    """ returns whether or not the session user is authenticated """
    if 'user_id' in session and 'user_token' in session:
        user = db_session.query(User).filter_by(id=session['user_id']).first()
        if user:
            return user.access_token == session['user_token']
    return False


def can_edit(song):
    """ returns whether the song is owned by the session user """
    if authenticated():
        if song.adder_id is None:
            return False
        else:
            return 'user_id' in session and song.adder_id == session['user_id']
    else:
        return False


# routes
@app.route('/source')
def source():
    """ redirects to github repository """
    return redirect(repo_uri)


@app.route(base_uri + 'seed')
def seed_database(fixture_filename='fixtures.json'):
    artists, _ = base_query()
    if len(artists) != 0:
        pass
    else:
        import json
        with open(fixture_filename) as data_file:
            fixtures = json.load(data_file)
            print(fixtures)
        seed_artists = fixtures['artists']
        for p in seed_artists:
            artist = Artist(name=p['name'])
            db_session.add(artist)
        seed_songs = fixtures['songs']
        for c in seed_songs:
            song = Song(name=c['name'],
                        song_url=c['song_url'],
                        description=c['description'],
                        featured=c['featured'],
                        artist_id=c['artist_id'])
            db_session.add(song)
        try:
            db_session.commit()
            flash('added.', 'warning')
        except Exception as e:
            flash('error. {}'.format(e), 'danger')
    return redirect(url_for('index'))


@app.route('/catalog')
@app.route('/')
def index():
    seed_database()
    artists, _ = base_query()
    featured_songs = db_session.query(Song).filter_by(featured=True)
    return render_template('index_songs.html',
                           artists=artists, songs=featured_songs,
                           title='Featured Songs', title_link=None,
                           logged_in=authenticated, editable=can_edit)


@app.route(api_uri + 'artists', methods=['GET'])
def index_artists_api():
    """ returns JSON response of artists """
    artists, _ = base_query()
    return jsonify(artists=[p.serialize for p in artists])


@app.route(api_uri + 'artists/<int:artist_id>', methods=['GET'])
def index_songs_api(artist_id):
    """ returns JSON response of songs """
    artist_songs = db_session.query(Song).filter_by(artist_id=artist_id)
    return jsonify(songs=[pc.serialize for pc in artist_songs])


@app.route(base_uri + 'artists/<int:artist_id>', methods=['GET'])
def index_songs(artist_id):
    """ artist show screen / songs index screen """
    artists, _ = base_query()
    try:
        artist = db_session.query(Artist).filter_by(id=artist_id).one()
    except:
        flash('Could not find what you were looking for :(', 'danger')
        return redirect(url_for('index'))
    artist_songs = db_session.query(Song).filter_by(artist_id=artist_id)
    return render_template('index_songs.html',
                           artists=artists, songs=artist_songs,
                           title=artist.name,
                           logged_in=authenticated, editable=can_edit)


@app.route(base_uri + 'songs/<int:song_id>', methods=['GET'])
def view_song(song_id):
    """ song view screen """
    artists, _ = base_query()
    try:
        song = db_session.query(Song).filter_by(id=song_id).one()
    except:
        flash('Could not find what you were looking for :(', 'danger')
        return redirect(url_for('index'))
    return render_template('view_song.html',
                           artists=artists, song=song,
                           title=song.name,
                           logged_in=authenticated,
                           editable=can_edit)


@app.route(base_uri + 'songs/new', methods=['GET', 'POST'])
def new_song():
    """ handles new song creation """
    if not authenticated():
        return redirect(url_for('login'))
    artists, _ = base_query()
    if request.method == 'POST':
        song = parse_song_form(request.form)
        song.adder_id = session['user_id']
        db_session.add(song)
        try:
            db_session.commit()
            flash('New song created!', 'success')
            return redirect(url_for('view_song', song_id=song.id))
        except Exception as e:
            flash('Something imploded. {}'.format(e), 'danger')
            return redirect(url_for('index'))
    else:
        song = {"id": None, "name": "", "song_url": "",
                "description": "", "start_date": "",
                "featured": False, "artist_id": None}
        return render_template('edit_song.html',
                               artists=artists, song=song,
                               title='New Song',
                               form_action=url_for('new_song'),
                               logged_in=authenticated)


@app.route(base_uri + 'songs/<int:song_id>/delete', methods=['GET', 'POST'])
def delete_song(song_id):
    """ handles song deletion """
    artists, _ = base_query()
    song = db_session.query(Song).filter_by(id=song_id).one()
    if not authenticated():
        return redirect(url_for('login'))
    elif not can_edit(song):
        flash('What are you doing here?', 'warning')
        return redirect(url_for('view_song', song_id=song_id))
    if request.method == 'POST':
        artist = db_session.query(Artist).filter_by(id=song.artist_id).one()
        db_session.delete(song)
        try:
            db_session.commit()
            flash('Song was deleted!', 'success')
            return redirect(url_for('index_songs', artist_id=artist.id))
        except Exception as e:
            flash('error. {}'.format(e), 'danger')
            return redirect(url_for('view_song', song_id=song.id))
    return render_template('delete_song.html',
                           artists=artists, song=song,
                           title='Are you sure that you want to DELETE:',
                           form_action=url_for('delete_song', song_id=song_id),
                           logged_in=authenticated)


@app.route(base_uri + 'songs/<int:song_id>/edit', methods=['GET', 'POST'])
def edit_song(song_id):
    """ handles song editing """
    artists, _ = base_query()
    song = db_session.query(Song).filter_by(id=song_id).one()
    if not authenticated():
        return redirect(url_for('login'))
    elif not can_edit(song):
        flash(
            'You don\'t own this! (Can\'t edit)',
            'warning')
        return redirect(url_for('view_song', song_id=song_id))
    if request.method == 'POST':
        song_params = parse_song_form(request.form)
        song.name = song_params.name
        song.song_url = song_params.song_url
        song.description = song_params.description
        song.featured = song_params.featured
        song.artist_id = song_params.artist_id
        db_session.add(song)
        try:
            db_session.commit()
            flash('Changes saved!', 'success')
        except Exception as e:
            flash('Something imploded. {}'.format(e), 'danger')
        return redirect(url_for('view_song', song_id=song_id))
    else:
        return render_template(
            'edit_song.html',
            artists=artists,
            song=song,
            title='Editing: ' + song.name,
            form_action=url_for(
                'edit_song',
                song_id=song_id),
            logged_in=authenticated)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
