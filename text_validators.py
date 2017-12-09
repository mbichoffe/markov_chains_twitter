#!/usr/bin/env python
# -*- coding: utf-8 -*-
from textblob import TextBlob
import wordfilter
import re

# CC = coordinating conjunction
# TO = to
# MD = Modal
# IN = Preposition or subordinating conjunction
p_o_s_tags = ['CC', 'TO', 'MD', 'IN']


def is_valid_p_o_s(first_word):
    """

    Check if the first word is a coherent sentence starter, using 
    part of speech analysis, returns True if word is not one of the
    listed parts of speech, False otherwise.

    >>> is_valid_p_o_s("For")
    For's part of speech:IN
    False
    >>> is_valid_p_o_s("Hello")
    Hello's part of speech:NN
    True
    >>> is_valid_p_o_s("And")
    And's part of speech:CC
    False


    """
    try:
        print (first_word +'\'s part of speech:' + TextBlob(first_word).tags[0][1])
        p_o_s = TextBlob(first_word).tags[0][1]
        if p_o_s not in p_o_s_tags:
            return True
        return False
    except (IndexError, UnicodeDecodeError) as e:
        print('Invalid character. Regenerating message!')
        return False


def is_valid_word(word):
    """

    Check if word is:
    - a 'bad word' (only words of oppresion,
    some profanity is ok) or if it is an http links
    - a link (https://)
    - a RT
    - an &amp; (still finding out how to fix that)
    Return True if any of the above is true.

    >>> is_valid_p_o_s("Hello")
    Hello's part of speech:NN
    True
    >>> is_valid_p_o_s("And")
    And's part of speech:CC
    False
    >>> is_valid_word("bitch")
    False
    >>> is_valid_word("lovely")
    True
    >>> is_valid_word("http://mysite.com")
    False
    >>> is_valid_word("RT:")
    False

    """

    if wordfilter.blacklisted(word):
        return False

    if 'http' in word[:5]:
        return False

    if re.search(r"\bRT(\.|:|,|$)", word, re.IGNORECASE):
        return False

    if word == '&amp;':
        return False

    return True
