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
from collections import Counter

#Below is a simple dictionary that categorizes pronouns+exceptions as male/female
pronouns_dict = {'male/person': ['he' , 'him', 'his', 'himself', 'man', 'boy', 'men', 'person'],
                'female/person': ['she', 'her', 'herself', 'lady', 'woman', 'girl', 'person']}

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
        (?<!  U\.S\.   )    # Don't end sentence on "U.S"
        \s+               # Split on whitespace between sentences.
        """, 
        re.IGNORECASE | re.VERBOSE)

pronoun_dumps = "wikipronouns.txt"
list_counts = {}

#Loading all the unique guesses
with open("guessdump.txt", 'r') as fp:
    guesses = pickle.load(fp)
fp.close()

for guess in guesses:

    #Load the wiki content for that guess
    f = open("dumps_final/"+guess+".txt", 'r')
    wiki_content = pickle.load(f)
    f.close()

    #We take the 2nd, 3rd and 4th sentence present in the wiki article for pronouns
    pronoun_sentences = sentence_finder.split(wiki_content)[1:3]
    all_words = "".join(pronoun_sentences).lower().split()
    found = False
    max_value = {}
    #Below logic is to find the pronoun that occurs max number of times and then categorize it based on the aboove dictionary
    for category, pro_list in pronouns_dict.iteritems():
        for element in pro_list:
            max_value.update({element: all_words.count(element)})
    max_pronoun, count = sorted(max_value.items(), key = operator.itemgetter(1), reverse = True)[0]
    for category, pro_list in pronouns_dict.iteritems():
        if max_pronoun in pro_list:
            list_counts.update({guess:category})
            found = True
            break
    #If no match is found, we set the category as None
    if found==False:
        list_counts.update({guess:'None'})

with open("guessdump_test.txt", 'r') as fp:
    guesses = pickle.load(fp)
fp.close()

for guess in guesses:

    #Load the wiki content for that guess
    f = open("dumps_final/"+guess+".txt", 'r')
    wiki_content = pickle.load(f)
    f.close()

    #We take the 2nd, 3rd and 4th sentence present in the wiki article for pronouns
    pronoun_sentences = sentence_finder.split(wiki_content)[1:3]
    all_words = "".join(pronoun_sentences).lower().split()
    found = False
    max_value = {}

    #Below logic is to find the pronoun that occurs max number of times and then categorize it based on the aboove dictionary
    for category, pro_list in pronouns_dict.iteritems():
        for element in pro_list:
            max_value.update({element: all_words.count(element)})
    max_pronoun, count = sorted(max_value.items(), key = operator.itemgetter(1), reverse = True)[0]
    for category, pro_list in pronouns_dict.iteritems():
        if max_pronoun in pro_list:
            list_counts.update({guess:category})
            found = True
            break
    #If no match is found, we set the category as None
    if found==False:
        list_counts.update({guess:'None'})

#Dumping for future use
with open(pronoun_dumps, 'wb') as fp:
    pickle.dump(list_counts,fp)
fp.close()
