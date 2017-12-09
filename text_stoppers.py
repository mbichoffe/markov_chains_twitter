#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

abbreviations_caps = ['R.S.V.P.', 'E.T.A.', 'P.S.', 'D.I.Y.', 'B.Y.O.B.', 
                      'D.C.', 'Gov.', 'U.S.', 'U.K.', 'U.N.', 'E.U.', 
                      'F.B.I.', 'C.I.A.']

abbreviations_list = ['mr', 'ms', 'mrs', 'msr', 'dr', 'gov', 'pres', 'sen', 
'sens', 'rep', 'reps', 'prof', 'gen', 'messrs', 'col', 'sr', 'jf', 'sgt', 
'mgr', 'fr', 'rev', 'jr', 'snr', 'atty', 'supt', 'ave', 'blvd', 'st', 'rd', 
'hwy', 'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'sept', 'oct', 
'nov', 'dec', 'etc', 'v', 'vs' ]


def is_abbreviation(word):
    """
    Return True if word is in abbreviations list; else return False.

    >>> is_abbreviation('R.S.V.P.')
    False
    >>> is_abbreviation("Dec.")
    True
    >>> is_abbreviation("Man.")
    False
    >>> is_abbreviation("")
    False

    """
    word = word[:-1]
    if word.lower() in abbreviations_list:
        return True
    return False

def stop_text(word, words):
    """Should we stop making text?
    Other than reaching the 280 chars limit, check for words that indicate
    the end of a sentence.
    Not that useful with Twitter, where it is not common to end sentences with
    a period.

    >>> long_text = ['This', 'planet', 'has', '-', 'or', 'rather', 'had', '-', 'a', 'problem,', 'which', 'was', 'this:', 'most', 'of', '', 'the', '', 'people', '', 'on', '', 'it', 'were', 'unhappy', 'for', 'pretty', 'much', 'of', 'the', 'time.', 'Many', 'solutions', 'were', 'suggested', 'for', 'this', 'problem,', 'but', 'most', 'of', 'these', 'were', '', 'largely', '', 'concerned', 'with', 'the', 'movements', 'of', 'small', 'green', 'pieces', 'of', 'paper,', 'which', 'is', 'odd', 'because', 'on', 'the', 'whole', 'it', "wasn't", '', 'the', '', 'small', 'green', 'pieces', 'of', 'paper', 'that', 'were', 'unhappy.']
    >>> word = 'apple'
    >>> stop_text(word, long_text)
    True

    >>> word = 'apple'
    >>> text = "Hello world"
    >>> stop_text(word, text)
    False

    >>> word = "Mr."
    >>> text = "Hello world"
    >>> stop_text(word, text)
    False
    >>> word = "ending."
    >>> text = "Hello there."
    >>> stop_text(word, text)
    True

    """
    if word in abbreviations_caps:
        return False
    if word[-1] in ['?', '!']:
        return True
    if word[-1] == '.' and not is_abbreviation(word):
        return True
    if len(" ".join(words)) >= 280:
        return True
    return False

 