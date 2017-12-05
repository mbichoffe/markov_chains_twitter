#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import re
from random import choice
from textblob import TextBlob #NLP 


class MarkovGenerator(object):
    """A Markov chain text generator"""

    def open_and_read_file(self, filenames):
        """Take file(s) as tuples; return text as string.

        Takes one or more strings that are a file path, opens the file,
        and turns the files' contents as one string of text.
        """
        body = []
        print filenames
        for filename in filenames:
            f = open(filename, 'rU')
            text = f.read()
            body.append(text)
            f.close()
        # create single string
        body = ' '.join(body)
        self.make_chains(body)


    def make_chains(self, text_string, n=2):
        """Take input text as string; return dictionary of Markov chains.

        A chain will be a key that consists of a tuple of (word1, word2)
        and the value would be a list of the word(s) that follow those two
        words in the input text.
        n is an integer indicating the number of items used to generate the n-grams.
        It is usually 2 or 3. If no number is specified, a bigram will be generated.

        For example:

            >>> chains = make_chains("hi there mary hi there juanita")

        Each bigram (except the last) will be a key in chains:

            >>> sorted(chains.keys())
            [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

        Each item in chains is a list of all possible following words:

            >>> chains[('hi', 'there')]
            ['mary', 'juanita']

            >>> chains[('there','juanita')]
            [None]
        """
        self.chains = {}
        words = text_string.split()
        for i in range(len(words)-n):
            ngram = (words[i], words[i+1])
            next_word = words[i+n]
            self.chains.setdefault(ngram, [])
            self.chains[ngram].append(next_word)


    def stop_text(self, words, new_word):
        """Should we stop making text?

        In this base generator, we should continue until we reach the
        end of our chain; in subclasses, we might stop on other conditions.
        """

        # This is just one way to think about this; there are many others.
        #punctuation for now
        ends_in_punct = new_word[-1] in ([".", "?", "!"])

        passed_char_limit = len(" ".join(words)) + len(new_word) > 140

        return passed_char_limit or ends_in_punct


    def make_text(self):
        """Take dictionary of markov chains; returns random text."""

        #character limit
        #punctuation
        #bad words
        #container for generated text
        words = []

        link = choice(self.chains.keys())#NPL
        words += link[0], link[1]

        while link in self.chains:
            # Keep looping until we have a key that isn't in the chains
            # (which would mean it was the end of our original text)
            #
            # Note that for long texts (like a full book), this might mean
            # it would run for a very long time.
            next_word = choice(self.chains[link])
            # Should we stop here?
            if self.stop_text(words, next_word):
                break

            words.append(next_word)
            link = (link[1], next_word)#create new ngram
            next_word = choice(self.chains[link])

        return " ".join(words)

    def make_and_post_tweets(random_text, markov_chains):
        """Create a tweet and send it to the Internet."""

        # Use Python os.environ to get at environmental variables
        # Note: run `source secrets.sh` before running this file
        # to make sure these environmental variables are set.
        api = twitter.Api(
            consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
            access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
            access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

        while True:
            status = api.PostUpdate(make_text(markov_chains))
            print status.text
            print  # blank line
            response = raw_input("Enter to tweet again [q to quit] > ")
            if response.lower() == 'q':
                break


def main():

    args = sys.argv[1:]
    if not args:
        print "usage: textfile.txt [textfile2.txt...]"
        sys.exit(1)

    print "\n\n\nRegular Generator"

    generator = MarkovGenerator()
    generator.open_and_read_file(args)

    for i in range(5):
        print generator.make_text()
        print

    #post tweets using Twitter API
    #make_and_post_tweets(random_text, markov_chains)

    #print random_text

if __name__ == "__main__":
    main()
