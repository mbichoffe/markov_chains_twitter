#!/usr/bin/env python
"""Generate Markov text from text files."""
import sys
from random import choice
from textblob import TextBlob #NLP 

def open_and_read_file(filename):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    f = open(filename, 'rU')
    text = f.read()
    f.close()

    return text


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

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
    markov_chains = {}
    words = text_string.split()
    for i in range(len(words)-2):
        bigram = (words[i], words[i+1])
        next_word = words[i+2]
        markov_chains.setdefault(bigram, [])
        markov_chains[bigram].append(next_word)

    return markov_chains


def make_text(chains):
    """Return text from chains."""

    #container for generated text
    words = []

    link = choice(chains.keys())
    words += link[0], link[1]
    next_word = choice(chains[link])

    while next_word is not None:
        link = (link[1], next_word)
        words.append(next_word)
        next_word = chains.get(choice(chains[link]))

    print words
    return " ".join(words)


def main():

    args = sys.argv[1:]
    if not args:
        print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
        sys.exit(1)

    # The args array is left just containing the dirs.
   
    if len(args) == 0:
        print "error: must specify one or more dirs"
        sys.exit(1)

  # Call functions

    # Open the file and turn it into one long string
    input_text = open_and_read_file(input_path)

    # Get a Markov chain
    markov_chains = make_chains(input_text)

    # Produce random text
    random_text = make_text(markov_chains)

    print random_text

if __name__ == "__main__":
    main()
