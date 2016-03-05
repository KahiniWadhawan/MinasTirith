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
import operator

#Below is a simple dictionary that categorizes pronouns+exceptions as male/female
pronouns_dict = {'male/person': ['he' , 'him', 'his', 'himself', 'man', 'boy', 'men', 'person'],
                'female/person': ['she', 'her', 'herself', 'lady', 'woman', 'girl', 'person'],
}
    

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

list_counts = {}
pronoun_dump = "questiontextpronouns_3.txt" 
train = DictReader(open("train_final.csv",'r'))

for ii in train:
    questionId = ii['Question ID']
    sentencePos = ii['Sentence Position']
    questionText = ii['Question Text']
    #Pull up Question Text from Training data
    sentences = questionText.lower().split()
    max_value = {}
    
    for category, pro_list in pronouns_dict.iteritems():
        for element in pro_list:
            max_value.update({element: sentences.count(element)})
    #Get the pronoun that occurs max times and check for the category from the above dictionary. If found, set the category accordingly.
    max_pronoun, count = sorted(max_value.items(), key = operator.itemgetter(1), reverse = True)[0]
    found = False
    
    for category, pro_list in pronouns_dict.iteritems():
        if max_pronoun in pro_list:
            list_counts.update({(questionId, sentencePos):category})
            found = True
            break
            
    #If not found, set category as None
    if found==False:
        list_counts.update({(questionId, sentencePos):'None'})


test = DictReader(open("test.csv",'r'))
for ii in test:
    questionId = ii['Question ID']
    sentencePos = ii['Sentence Position']
    questionText = ii['Question Text']
    #Pull up Question Text from Test data
    sentences = questionText.lower().split()
    max_value = {}
    
    for category, pro_list in pronouns_dict.iteritems():
        for element in pro_list:
            max_value.update({element: sentences.count(element)})
            
    #Get the pronoun that occurs max times and check for the category from the above dictionary. If found, set the category accordingly.
    max_pronoun, count = sorted(max_value.items(), key = operator.itemgetter(1), reverse = True)[0]
    found = False
    
    for category, pro_list in pronouns_dict.iteritems():
        if max_pronoun in pro_list:
            list_counts.update({(questionId, sentencePos):category})
            found = True
            break
            
    #If not found, set category as None
    if found==False:
        list_counts.update({(questionId, sentencePos):'None'})

#Dumps the dictionary for future purpose
with open(pronoun_dump, 'wb') as fp:
    pickle.dump(list_counts, fp)
fp.close()
