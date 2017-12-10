#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for Balloonicorn's Flask app."""

import unittest
import doctest
import text_stoppers
import text_validators
import markov
import mock
import server

def load_tests(loader, tests, ignore):
    """Also run our doctests and file-based doctests.

    This function name, ``load_tests``, is required.
    """

    tests.addTests(doctest.DocTestSuite(text_stoppers))
    tests.addTests(doctest.DocTestSuite(text_validators))
    tests.addTests(doctest.DocTestSuite(markov))
    return tests

class MarkovTweetTests(unittest.TestCase):
    """Tests for Markov Chains site."""

    def setUp(self):
        """Code to run before every test."""
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""
        result = self.client.get("/")
        self.assertIn("Ready to get started?", result.data)

    def test_log_out(self):
        """Do users who haven't RSVPed see the correct view?"""
        #FIXME: write a test for users who are not logged in can't go to home
        print "FIXME"


    def test_search_results(self):
        """Test search results page"""
        # result = self.client.post("/by-user",
        #                           data={'user': None},
        #                           follow_redirects=True)
        # self.assertIn("Please type a twitter handle", result.data)
        pass




if __name__ == "__main__":
    unittest.main()