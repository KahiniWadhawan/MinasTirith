'''Generates words that are dependent on the word "This" for all question text in train and test'''

from __future__ import division
import operator
import nltk
import string
from csv import DictReader, DictWriter
import wikipedia
import re
import time
import cPickle as pickle
from pattern.en import tag
from collections import Counter, defaultdict

import corenlp
from corenlp import StanfordCoreNLP


# Used to avoid spliting on period that are part of sentence
sentence_finder = re.compile(r"""
        # Split sentences on whitespace between them.
        (?:               # Group for two positive lookbehinds.
          (?<=[.!?])      # Either an end of sentence punct,
        | (?<=[.!?]['"])  # or end of sentence punct and quote.
        )                 # End group of two positive lookbehinds.
        (?<!  Mr\.   )    # Don't end sentence on "Mr."
        (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
        (?<!  Jr\.   )    # Don't end sentence on "Jr."
        (?<!  Dr\.   )    # Don't end sentence on "Dr."
        (?<!  Prof\. )    # Don't end sentence on "Prof."
        (?<!  Sr\.   )    # Don't end sentence on "Sr."
        (?<!  U\.S\.   )    # Don't end sentence on "U.S."
        (?<!  U\.K\.   )    # Don't end sentence on "U.K."
        (?<!  U\.S\.A\.   )    # Don't end sentence on "U.S.A."
        \s+               # Split on whitespace between sentences.
        """, 
        re.IGNORECASE | re.VERBOSE)
        
        
sp = StanfordCoreNLP()
this_dictionary = defaultdict(list)
this_dump = "this_qtext_dump_v0.txt" 
train = DictReader(open("train.csv",'r'))
count = 0



for ii in train:
    count += 1
    print "train", count
    questionId = ii['Question ID']
    sentencePos = ii['Sentence Position']
    questionText = ii['Question Text']

    # Parses and finds the words dependent on "This"    
    for line in sentence_finder.split(questionText):
        sparse = corenlp.corenlp.StanfordCoreNLP.raw_parse(sp, line)
        this_dependencies = [y for x, y, z in sparse['sentences'][0]['dependencies'] if (z == u'This' or z == u'this' )]
        this_dictionary[(questionId, sentencePos)] += this_dependencies
        
    this_dictionary[(questionId, sentencePos)] = set(this_dictionary[(questionId, sentencePos)])



count = 0
test = DictReader(open("test.csv",'r'))

# Same as above, for test file
for ii in test:
    count +=1
    print "test", count
    questionId = ii['Question ID']
    sentencePos = ii['Sentence Position']
    questionText = ii['Question Text']

    # Parses and finds the words dependent on "This" 
    for line in sentence_finder.split(questionText):
        sparse = corenlp.corenlp.StanfordCoreNLP.raw_parse(sp, line)
        this_dependencies = [y for x, y, z in sparse['sentences'][0]['dependencies'] if (z == u'This' or z == u'this' )]
        this_dictionary[(questionId, sentencePos)] += this_dependencies

    this_dictionary[(questionId, sentencePos)] = set(this_dictionary[(questionId, sentencePos)])

# Dumps here        
with open(this_dump, 'w') as fp:
    pickle.dump(this_dictionary, fp)
fp.close()
