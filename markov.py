#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
from text_stoppers import *
from text_validators import *
from random import choice


class MarkovGenerator(object):
    """A Markov chain text generator"""

    def open_and_read_file(self, filename):
        """Take file(s) as tuples; return text as string.

        Takes a string that is a file path, opens the file,
        and turns the files' contents as one string of text.
        """
        f = codecs.open(filename, encoding='utf-8')
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

            chains = make_chains("hi there mary hi there juanita")

        Each bigram (except the last) will be a key in chains:

            sorted(chains.keys())
            [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

        Each item in chains is a list of all possible following words:

            chains[('hi', 'there')]
            ['mary', 'juanita']

            chains[('there','juanita')]
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

        words = [] # container for our random text
        are_valid_words = False
        char_limit = 280

        while not are_valid_words:
            link = choice(self.chains.keys()) #tuple from chain
            word1 = link[0]
            word2 = link[1]
            print 'Checking words: ', word1, word2
            # Is the first word an acceptable POS? Are the words valid?
            are_valid_words = all([is_valid_p_o_s(word1), is_valid_word(word2),
                                  is_valid_word(word1)])

        words += word1.capitalize(), word2

        while link in self.chains:
            # Keep looping until we have a key that isn't in the chains
            # Or until we reach one of the text stopper conditions
            # Or we reach the 280 chars limit
            # If picked word is invalid, choose a new one

            next_word = choice(self.chains[link])
            if is_valid_word(next_word):
                words.append(next_word)
                # Should we stop here?
                if stop_text(next_word, words):
                    break
            link = (link[1], next_word)#create new ngram

        return " ".join(words)


def main(): # debugging
    args = sys.argv[1:]
    if not args:
        print "usage: textfile.txt [textfile2.txt...]"
        sys.exit(1)

    print "\n\n\nMarkov Generator"

    generator = MarkovGenerator()
    generator.open_and_read_file(args[0])

    for i in range(5):
        print generator.make_text()
        print


if __name__ == "__main__":
    main()
