''' Creates Country Scores. Looks for Country and Nationality in question text,
    if the guess word's wiki content has the country or nationality mentioned,
    it's a match'''

import pickle, string, nltk
import cPickle as pickle
import logging
from gensim import corpora, models, similarities
import re, enchant
import string, nltk

from csv import DictReader, DictWriter
from stemming.porter2 import stem
import itertools, math, operator

from generate_guess_genders import freebase_gender
from generate_this_context import this_context


# Pre-processes guess words
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
correct = 0
cont = 0

# Loads countries dump 
with open("countries_dump.txt","rb") as fn: 
    country_dict = pickle.load(fn)

fn.close()

country_scores_dict = {}
dirname = "/Users/manjhunathkr/Documents/NLP/Final Project/All Trials/All Dumps/dumps_final_modified/"


# Gets the list of guesses matching country or nationality for each question text
for ii in train:   
    count += 1
    
    qid = ii['Question ID']
    spos = ii['Sentence Position']
    ques = ii['Question Text']
    


    # Gets all guess words in IR Wiki and QANTA Scores
    guess_words = []
    guesses = ii['IR_Wiki Scores'] + ", " + ii['QANTA Scores']
    words = re.split(',[^_]', guesses)


    # Creates a list of guesses
    # guess_original is the original list of guesses as present in the train.csv
    # guess_new is the pre-processed list of guesses
    # guess_map is a dictionary to map guess_new to its corresponding guess_original
    guess_original = []
    for word in words:
        guess = word.split(":")[0].rstrip().lstrip()
        guess_original.append(guess)

    guess_original = list(set(guess_original))

    guess_new = []
    country_match_guesses = []
    guess_map = {}

    for item in guess_original:
        modified_guess = remove_punct(item)
        guess_new.append(modified_guess)
        guess_map.update({modified_guess : item})


    # Gets list of countries/ nationalities present in question text
    qt_country_list = []
    for item in country_dict:
        for value in country_dict[item]:
            if value in ques:
                qt_country_list.append(item)
                break

    # Checks for presence of countries found above in the guess word's wiki page
    for guess in guess_new:
        fname = guess + ".txt"
        with open(dirname + fname, "rb") as f:
            data = pickle.load(f)
        f.close()

        country_match_count = 0
        country_matched = 0.0


        for item in qt_country_list:
            if country_matched == 1.0:
                break
            
            for value in country_dict[item]:
                country_match_count = data.count(value)
                if country_match_count > 0:
                    country_match_guesses.append(guess)
                    country_matched = 1.0
                    break
            

    country_score_list = []

    
    # Prepares scores in a list
    for guess in guess_new:
        if guess in country_match_guesses:
            country_score_list.append(guess_map[guess] + ":" + str(1.0))
        else:
            country_score_list.append(guess_map[guess] + ":" + str(0.0))

        

    country_scores_dict.update({(qid, spos):country_score_list})


# Dumps here
with open("final_train_country_scores_dict.txt", "wb") as fp:
    pickle.dump(country_scores_dict, fp)
    
fp.close()


test = DictReader(open("test.csv", 'rU'))

gender_scores_dict = {}
this_context_scores_dict = {}
this_context_related_scores_dict = {}
count = 0

# Same as above but for test.csv
# Gets the list of guesses matching country or nationality for each question text
for ii in test:
    count += 1
    
    qid = ii['Question ID']
    spos = ii['Sentence Position'] 
    ques = ii['Question Text']
 

    # Gets all guess words in IR Wiki and QANTA Scores
    guess_words = []
    guesses = ii['IR_Wiki Scores'] + ", " + ii['QANTA Scores']
    words = re.split(',[^_]', guesses)


    # Creates a list of guesses
    # guess_original is the original list of guesses as present in the train.csv
    # guess_new is the pre-processed list of guesses
    # guess_map is a dictionary to map guess_new to its corresponding guess_original
    guess_original = []
    for word in words:
        guess = word.split(":")[0].rstrip().lstrip()
        guess_original.append(guess)

    guess_original = list(set(guess_original))

    guess_new = []
    country_match_guesses = []
    guess_map = {}

    for item in guess_original:
        modified_guess = remove_punct(item)
        guess_new.append(modified_guess)
        guess_map.update({modified_guess : item})


    # Gets list of countries/ nationalities present in question text
    qt_country_list = []
    for item in country_dict:
        for value in country_dict[item]:
            if value in ques:
                qt_country_list.append(item)
                break

    # Checks for presence of countries found above in the guess word's wiki page
    for guess in guess_new:
        fname = guess + ".txt"
        with open(dirname + fname, "rb") as f:
            data = pickle.load(f)
        f.close()

        country_match_count = 0
        country_matched = 0.0
        for item in qt_country_list:
            if country_matched == 1.0:
                break
            
            for value in country_dict[item]:
                country_match_count = data.count(value)
                if country_match_count > 0:
                    country_match_guesses.append(guess)
                    country_matched = 1.0
                    break
            

    country_score_list = []

    
    # Prepares scores in a list
    for guess in guess_new:
        if guess in country_match_guesses:
            country_score_list.append(guess_map[guess] + ":" + str(1.0))
        else:
            country_score_list.append(guess_map[guess] + ":" + str(0.0))

        
        
    country_scores_dict.update({(qid, spos):country_score_list})

# Dumps here
with open("final_test_country_scores_dict.txt", "wb") as fp:
    pickle.dump(country_scores_dict, fp)
    
fp.close()

