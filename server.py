#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_cache import Cache
from markov import *
import tweepy
from jinja2 import StrictUndefined
import urlparse
from tweets_grabber import *
from config import *
from pagination import Pagination
import oauth2 as oauth

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "AIRSPEEDVELOCITYOFANUNLADENSWALLOW"

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route('/')
def index():
    """Render landing page if user is not signed in, home page if signed in."""
    if session.get('id'):
        return redirect('/home')
    args = "alice_in_wonderland"
    # display only the first 4 random tweets
    tweets = get_markov_tweets(args)[:5]
    return render_template("index.html", tweets=tweets)


@app.route('/about')
def about():
    """Render about page."""
    return render_template('about.html')


@app.route('/home')
def home():
    """Render main page for logged in users."""
    try:
        api = get_tweepy_api()
        # Get User object from Twitter API
        user_data = api.me()
        # Store main user info in session
        save_user_data_in_session(user_data)
        # Get random tweets from txt file to be displayed:
        args = "alice_in_wonderland"
        tweets = get_markov_tweets(args)[:5]
        return render_template('home.html', user_data=user_data,
                               statuses=tweets)
    except tweepy.TweepError as e:
        flash("Error: {} code: {}".format(e.reason))
        return redirect('/')


@app.route('/tweet/', methods=['GET'])
def tweet():
    """Tweet via API."""
    text = request.args.get('tweet')
    try:
        api = get_tweepy_api()
        api.update_status(text)
        flash("Success!")
        return redirect('/home')
    except tweepy.TweepError as e:
        flash("Error: {}".format(e.reason))
        return redirect('/home')


@app.route('/by-user')
def display_results():
    """Render page with results returned by the API search for users."""
    user = request.args.get('user')
    if not user:
        flash('Please type a twitter handle')
        return redirect('/home')

    results = get_list_of_users_by_name(user)

    return render_template('search-results.html',
                           users=results,
                           search_term=user)


@app.route('/markov-tweet/<screen_name>/<int:page>')
@cache.cached(timeout=60 * 5)
def markov_tweet(screen_name, page):
    """Render page with tweets generated by the Markov Chain algorithm."""
    try:
        api = get_tweepy_api()
        print "get tweepy api", api
        user_data = api.me()
        print "user_data", user_data._json
        tweets = get_all_tweets(screen_name)
    except tweepy.TweepError as e:
        flash("Error: {} ".format(e))
        return redirect('/')
    try:
        markov_tweets = get_markov_tweets(screen_name)
        pagination = Pagination(page, PER_PAGE)
        print pagination.page, pagination.per_page
        return render_template('markov-tweets.html',
                               user_data=user_data,
                               statuses=markov_tweets,
                               screen_name=screen_name,
                               pagination=pagination,)
    except IOError:
        # Flash errors returned by the function
        flash(tweets)
        return redirect('/home')


@app.route("/logout")
def process_logout():
    """Log user out."""
    for key in session.keys():
        session.pop(key)
    flash("Logged out.")
    return redirect("/")


@app.route('/register')
def get_oauth_token():
    """
    Send oauth request to twitter API and get request token or display errors.

    If successfull, will redirect user to Twitter's Approve/Deny page.

    """
    consumer = oauth.Consumer(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    client = oauth.Client(consumer)
    # Get oauth request token:
    resp, content = client.request(REQUEST_TOKEN_URL, "GET")
    # Any value other than 200 on status indicates a failure:
    if resp['status'] != '200':
            flash("Invalid response {}".format(resp['status']))
    # parse response params
    request_token = dict(urlparse.parse_qsl(content))
    # check if callback is confirmed, else flash errors.
    if request_token['oauth_callback_confirmed']:
        session['oauth_token'] = oauth_token = request_token['oauth_token']
        session['token_secret'] = request_token['oauth_token_secret']
        # now we will redirect the user to Twitter's authorization page
        return redirect(AUTHORIZE_URL +
                        "?oauth_token=" +
                        oauth_token)
    # if callback is not confirmed, flash errors and return to main page
    errors = request_token.get('errors')
    flash('error code: ', errors['code'], 'message :', errors['message'])
    return redirect('/')


@app.route("/oauth")
def oauth_process():
    """
    Redirect user to Twitter's Approve/Deny page.

    Upon a successful authentication we should have received a request
    containing the oauth_token and oauth_verifier parameters.
    the oauth token should be the same as received in /register.

    """
    oauth_verifier = request.args.get('oauth_verifier')
    # TODO: check for oauth token
    if oauth_verifier:
        access_token = get_access_token(oauth_verifier)
        if access_token:
            #store in session
            session['oauth_token'] = access_token['oauth_token']
            session['oauth_token_secret'] = access_token['oauth_token_secret']
            return redirect('/home')
    # If there is no access code, flash an error message
    else:
        flash('OAuth failed')

    return redirect('/')


######### Helper Functions #########

def get_access_token(oauth_verifier):
    """Use access code to request user's access token."""
    consumer = oauth.Consumer(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    token = oauth.Token(session['oauth_token'],
                        session['token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
    # Make a post request with the oauth verifier
    resp, content = client.request(ACCESS_TOKEN_URL, "POST")
    # Any value other than 200 on response indicates failure:
    if resp['status'] != '200':
            access_token = None
            flash("Invalid response {}".format(resp['status']))
    # if sucessfull, save oauth token in session
    access_token = dict(urlparse.parse_qsl(content))

    return access_token


def get_list_of_users_by_name(username):
    """
    Return list of dictionaries with each dictionary holding data returned from
    Tweepy API search for users in User object form.
    """
    api = get_tweepy_api()
    if not api:
        flash(session['auth_error'])
        return redirect('/home')

    users = []
    print "api.search_users", api.search_users(username, 20, 1)
    for user in api.search_users(username, 20, 1):
        user_data = {}
        user_data['id'] = user.id
        user_data['followers_count'] = user.followers_count
        user_data['description'] = user.description
        user_data['profile_image_url'] = user.profile_image_url
        user_data['profile_background_image_url'] = user.profile_background_image_url
        user_data['screen_name'] = user.screen_name
        user_data['name'] = user.name
        user_data['verified'] = user.verified
        user_data['follow_request_sent'] = user.follow_request_sent
        users.append(user_data)

    return users


def get_tweepy_api():
    """Return Twitter API wrapper."""
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(session['oauth_token'], session['oauth_token_secret'])
    return tweepy.API(auth)


def save_user_data_in_session(user_data):
    """Store current user info in a Flask session."""
    session['id'] = user_data.id
    session['description'] = user_data.description
    session['profile_image_url'] = user_data.profile_image_url
    session['screen_name'] = user_data.screen_name
    session['name'] = user_data.name
    session['verified'] = user_data.verified


def get_markov_tweets(screen_name):
    """
    Open txt file with scren_name's twitter timeline and create markov chain
    tweets from it.
    """
    args = os.getcwd() + '/data/' + screen_name + '.txt'
    generator = MarkovGenerator()
    generator.open_and_read_file(args)
    tweets = []
    for i in range(10):
        tweets.append(generator.make_text())
    return tweets

app.jinja_env.undefined = StrictUndefined
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0", port=5000)
