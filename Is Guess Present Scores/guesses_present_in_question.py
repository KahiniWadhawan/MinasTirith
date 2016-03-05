'''Generates scores for guesses based on whether they are present in question text or not'''

import pickle, string, nltk
import cPickle as pickle
import logging
from gensim import corpora, models, similarities
import re, enchant
import string
import nltk

from csv import DictReader, DictWriter
from stemming.porter2 import stem
import itertools, math, operator

from generate_guess_genders import freebase_gender
from generate_this_context import this_context


# Pre-processes guesses
def remove_punct(guess):
    if '_' in guess:
            guess = guess.replace('_', ' ')
    if '&amp;' in guess:
            guess = guess.replace('&amp;', '&')
    if '&quot;' in guess:
            guess = guess.replace('&quot;', '"')
                            
    guess = re.sub('[%s]' % re.escape(string.punctuation), '', guess)
    
    return guess



train = DictReader(open("train.csv", 'rU'))
count = 0 

guess_in_ques_dict = {}
proper_name_list =[]


# Prepares the set of common first names
# 'CSV_Database_of_First_Names.csv' contains the list of common American/ English first names obtained from the web
proper_names = DictReader(open("CSV_Database_of_First_Names.csv", 'rU'))
for name in proper_names:
    proper_name_list.append(name.values()[0].lower())

proper_name_set = set(proper_name_list)


# Gets the list of guesses present in the question text
for ii in train:   
    count += 1

    qid = ii['Question ID']
    spos = ii['Sentence Position'] 
    ques = ii['Question Text']
    ques = re.sub('[%s]' % re.escape(string.punctuation), ' ', ques)


    
    # Gets all guess words in IR Wiki and QANTA Scores
    guess_words = []
    guesses = ii['IR_Wiki Scores'] + ", " + ii['QANTA Scores']
    words = re.split(',[^_]', guesses)
    words = list(set(words))


    # Creates a list of guesses
    # guess_original is the original list of guesses as present in the train.csv
    guess_original = []
    for word in words:
        guess = word.split(":")[0].rstrip().lstrip()
        guess_original.append(guess)

    guess_original = list(set(guess_original))


    
    guess_in_ques_list = []
    # Checks for guesses present in question text in train.csv
    for item in guess_original:
        modified_guess = remove_punct(item)
        split_modified_guess = modified_guess.split()

        tags_set = set([y for x,y in nltk.pos_tag(split_modified_guess)])
        non_nouns = set([x for x in tags_set if x not in ['NN', 'NNS', 'NNP', 'NNPS']])

        guess_in_ques_score = 0.0
        
        # Checks if the guess word(unsplit) is present in the question text
        if modified_guess in ques:
            guess_in_ques_score = 1.0

        else:
            # Checks if last names of proper name guesses
            if non_nouns == set([]):
                
                # Checks if guess has common first names in it;
                # If yes, checks if the last word of guess is present in question text
                # Length condition to remove undesirable answers when the last word contains only few characters
                if len(set.intersection(set(split_modified_guess), proper_name_set)) > 0:
                    if (split_modified_guess[-1]+ " ") in ques and len(set(split_modified_guess[-1].split())) > 2:
                        guess_in_ques_score = 1.0


                # Else checks if the first word of guess is present in question text
                # Length condition to remove undesirable answers when the first word contains only few characters
                else:
                    if (split_modified_guess[0]+ " ") in ques and len(set(split_modified_guess[0].split())) > 2:
                        guess_in_ques_score = 1.0

                        
                        
            else:
               guess_in_ques_score = 0.0 
                        
                
                     
        guess_in_ques_list.append(item + ":" + str(guess_in_ques_score))
                
    
    guess_in_ques_dict.update({(qid, spos):guess_in_ques_list})


# Dumps here    
with open("final_train_is_guess_present_in_ques_dict.txt", "wb") as fp:
    pickle.dump(guess_in_ques_dict, fp)
    
fp.close()



test = DictReader(open("test.csv", 'rU'))

guess_in_ques_dict = {}

count = 0

# Same as above, but for test.csv
# Gets the list of guesses present in the question text
for ii in test: 
    count += 1

    qid = ii['Question ID']
    spos = ii['Sentence Position'] 
    ques = ii['Question Text']
    ques = re.sub('[%s]' % re.escape(string.punctuation), ' ', ques)


    # Gets all guess words in IR Wiki and QANTA Scores
    guess_words = []
    guesses = ii['IR_Wiki Scores'] + ", " + ii['QANTA Scores']
    words = re.split(',[^_]', guesses)
    words = list(set(words))


    # Creates a list of guesses
    # guess_original is the original list of guesses as present in the test.csv
    guess_original = []
    for word in words:
        guess = word.split(":")[0].rstrip().lstrip()
        guess_original.append(guess)

    guess_original = list(set(guess_original))

    guess_in_ques_list = []

    # Checks for guesses present in question text in test.csv
    for item in guess_original:
        modified_guess = remove_punct(item)
        split_modified_guess = modified_guess.split()

        tags_set = set([y for x,y in nltk.pos_tag(split_modified_guess)])
        non_nouns = set([x for x in tags_set if x not in ['NN', 'NNS', 'NNP', 'NNPS']])

        guess_in_ques_score = 0.0
        # Checks if the guess word(unsplit) is present in the question text
        if modified_guess in ques:
            guess_in_ques_score = 1.0
            
        else:
            # Checks if last names of proper name guesses
            if non_nouns == set([]):

                # Checks if guess has common first names in it;
                # If yes, checks if the last word of guess is present in question text
                # Length condition to remove undesirable answers when the last word contains only few characters
                if len(set.intersection(set(split_modified_guess), proper_name_set)) > 0:
                    if (split_modified_guess[-1]+ " ") in ques and len(set(split_modified_guess[-1].split())) > 2:
                        guess_in_ques_score = 1.0
                        
                # Else checks if the first word of guess is present in question text
                # Length condition to remove undesirable answers when the first word contains only few characters                       
                else:
                    if (split_modified_guess[0]+ " ") in ques and len(set(split_modified_guess[0].split())) > 2:
                        guess_in_ques_score = 1.0
                        
                        
                        
            else:
               guess_in_ques_score = 0.0 
                        
                
                
        guess_in_ques_list.append(item + ":" + str(guess_in_ques_score))
        
        
    guess_in_ques_dict.update({(qid, spos):guess_in_ques_list})


# Dumps here
with open("final_test_is_guess_present_in_ques_dict.txt", "wb") as fp:
    pickle.dump(guess_in_ques_dict, fp)
    
fp.close()
