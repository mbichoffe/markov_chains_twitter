#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import re
from text_stoppers import *
from random import choice
from textblob import TextBlob #NLP 


class MarkovGenerator(object):
    """A Markov chain text generator"""

    def open_and_read_file(self, filename):
        """Take file(s) as tuples; return text as string.

        Takes a string that is a file path, opens the file,
        and turns the files' contents as one string of text.
        """
        f = open(filename, 'rU')
        text = f.read()
        f.close()
        self.make_chains(text)


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


    def make_text(self):
        """Take dictionary of markov chains; returns random text."""

        words = []

        char_limit = 280

        link = choice(self.chains.keys())#NPL
        while not self.valid_p_o_s(link[0]):
            link = choice(self.chains.keys())
        words += link[0], link[1]

        while link in self.chains and len(words) < char_limit:
            # Keep looping until we have a key that isn't in the chains
            # (which would mean it was the end of our original text)
            next_word = choice(self.chains[link])
            words.append(next_word)
            # Should we stop here?
            if stop_text(next_word):
                break
            link = (link[1], next_word)#create new ngram

        return " ".join(words)


    def make_and_post_tweets(random_text, markov_chains):
        """Create a tweet and send it to the Internet."""

        # Use Python os.environ to get at environmental variables
        # Note: run `source secrets.sh` before running this file
        # to make sure these environmental variables are set.
    def valid_p_o_s(self, word):
        try:
            print (word +'\'s part of speech:' + TextBlob(word).tags[0][1])
            p_o_s = TextBlob(word).tags[0][1]
            if p_o_s != 'CC' and p_o_s != 'TO' and p_o_s != 'MD' and p_o_s != 'IN':
                return True
            return False
        except (IndexError, UnicodeDecodeError) as e:
            print('Invalid character. Regenerating message!')
            return False

def main():
    args = sys.argv[1:]
    if not args:
        print "usage: textfile.txt [textfile2.txt...]"
        sys.exit(1)

    print "\n\n\nRegular Generator"

    generator = MarkovGenerator()
    generator.open_and_read_file(args[0])

    for i in range(5):
        print generator.make_text()
        print 

    #post tweets using Twitter API
    #make_and_post_tweets(random_text, markov_chains)

    #print random_text

if __name__ == "__main__":
    main()
