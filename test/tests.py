#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for Markov Chain app."""

import unittest
import doctest
import text_stoppers
import text_validators
import markov
import tweepy
import config
from unittest.mock import Mock, MagicMock, patch
import server


def load_tests(loader, tests, ignore):
    """Also run our doctests and file-based doctests."""
    tests.addTests(doctest.DocTestSuite(text_stoppers))
    tests.addTests(doctest.DocTestSuite(text_validators))
    tests.addTests(doctest.DocTestSuite(markov))
    return tests


class MarkovTweetTests(unittest.TestCase):
    """Tests for Markov Chains site."""

    def setUp(self):
        """Code to run before every test."""
        self.client = server.app.test_client()
        # look up flask documentation on test client
        server.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage? ."""
        result = self.client.get("/")
        self.assertIn("Ready to get started?", result.data)


    def test_log_out(self):
        """Do users who haven't RSVPed see the correct view?."""
        # FIXME: write a test for users who are not logged in can't go to home
        print "FIXME"


    def test_search_results(self):
        """Test search results page"""
        # result = self.client.post("/by-user",
        #                           data={'user': None},
        #                           follow_redirects=True)
        # self.assertIn("Please type a twitter handle", result.data)
        pass


    @patch('server.get_tweepy_api')
    def test_get_tweepy_api_with_error(self, mock_get_tweepy_api):
        # Configure the mock to not return a response with an error status code.
        reason_obj = [{u'message': u'Sorry, that page does not exist', u'code': 34}]
        mock_get_tweepy_api.return_value = MagicMock(spec=tweepy, **reason_obj)
        api = server.get_tweepy_api()
        self.assertEqual(api[0]['code'], 34)


    # auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    # auth.set_access_token(session['oauth_token'], session['oauth_token_secret'])
    # return tweepy.API(auth)

#check log in create fake token
# call twitter API
# render the page

# How to run tests:
# go to /markov_chains (parent directory)
# >>> python -m test.tests


if __name__ == "__main__":
    unittest.main()