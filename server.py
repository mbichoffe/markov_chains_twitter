#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, session, \
    jsonify
from flask_debugtoolbar import DebugToolbarExtension
from markov import *
import twitter
import requests
from jinja2 import StrictUndefined
import json
import urlparse
import oauth2 as oauth
# import calendar
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "AIRSPEEDVELOCITYOFANUNLADENSWALLOW"
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN_KEY = os.environ.get('TWITTER_ACCESS_TOKEN_KEY')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

###ENDPOINTS###
REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
RETURN_URL = 'http://localhost:5000/oauth'

@app.route('/')
def index():
    # if session['user_id']:
    #     return redirect('/home')

    args = ["gettysburg.txt"]
    generator = MarkovGenerator()
    generator.open_and_read_file(args)
    tweets = []
    for i in range(5):
        tweets.append(generator.make_text())
    print tweets
    return render_template("index.html", tweets=tweets)
    """Main page."""

@app.route('/home')
def home():
    """Render main page"""
    api = twitter.Api(
                      consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                      consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                      access_token_key=session['oauth_token'],
                      access_token_secret=session['oauth_token_secret'])

    user_data = api.VerifyCredentials()
    statuses = api.GetUserTimeline()
    return render_template('home.html', user_data=user_data,
                            statuses=statuses)


@app.route('/register')
def get_oauth_token():
    """
    Send oauth request to twitter API and get token or display errors.
    If successfull, will redirect user to Twitter's Approve/Deny page.
    """
    consumer = oauth.Consumer(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    client = oauth.Client(consumer)
    # Get oauth request token:
    resp, content = client.request(REQUEST_TOKEN_URL, "GET")
    #Any value other than 200 on status indicates a failure:
    if resp['status'] != '200':
            flash("Invalid response {}".format(resp['status']))
    # parse response params
    request_token = dict(urlparse.parse_qsl(content))
    # check if callback is confirmed, else flash errors.
    if request_token['oauth_callback_confirmed']:
        oauth_token = request_token['oauth_token']
        session['oauth_token'] = oauth_token #save in session
        oauth_token_secret = request_token['oauth_token_secret']
        session['oauth_token_secret'] = oauth_token_secret
        # now we will redirect the user to Twitter's authorization page
        return redirect(AUTHORIZE_URL
                        + "?oauth_token=" 
                        + oauth_token)
    # if callback is not confirmed, flash errors and return to main page
    errors = request_token.get('errors')
    flash('error code: ', errors['code'], 'message :', errors['message'])
    return redirect('/')


@app.route("/oauth")
def oauth_process():
    """Redirect user to Twitter's Approve/Deny page."""

    # Upon a successful authentication we should have received a request
    # containing the oauth_token and oauth_verifier parameters.
    # the oauth token should be the same as received in /register.

    oauth_verifier = request.args.get('oauth_verifier')
    # TODO: check for oauth token
    if oauth_verifier:
        access_token = get_access_token(oauth_verifier)

        if access_token:
            session['oauth_token'] = access_token['oauth_token']
            session['oauth_token_secret'] = access_token['oauth_token_secret']
            return redirect('/home')
    # If there is no access code, flash an error message
    else:
        flash('OAuth failed')

    return redirect('/')

######### Helper Functions #########

def get_access_token(oauth_verifier):
    """Use access code to request user's access token"""

    consumer = oauth.Consumer(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    token = oauth.Token(session['oauth_token'],
                        session['oauth_token_secret'])
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


app.jinja_env.undefined = StrictUndefined
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = False

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0", port=5000)