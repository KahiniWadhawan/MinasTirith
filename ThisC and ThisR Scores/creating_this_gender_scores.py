'''Creates Gender, This Context, This Related Scores for guesses'''

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
correct = 0
cont = 0


gender_scores_dict = {}
this_context_scores_dict = {}
this_context_related_scores_dict = {}

# Gets the list of guesses matching Gender, This Context, This Related Context for each question text
for ii in train:   
    count += 1
    
    qid = ii['Question ID']
    spos = ii['Sentence Position']
    ques = ii['Question Text']

    # Gets all guess words in IR Wiki and QANTA Scores
    guess_words = []
    guesses = ii['IR_Wiki Scores'] + ", " + ii['QANTA Scores']
    words = re.split(',[^_]', guesses)
    words = list(set(words))


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
    guess_map = {}
    
    for item in guess_original:
        modified_guess = remove_punct(item)
        guess_new.append(modified_guess)
        guess_map.update({modified_guess : item})
        


    # Gets list of guesses matching This_Context words, This_Related words, Gender in the question text
    (ques_this_context, this_context_guess_matches, ques_this_context_related, this_context_related_guess_matches, gender_from_this_context) = this_context(qid, spos, guess_new)
    (ques_gender_cat, gender_match_guesses) = freebase_gender(qid, spos, guess_new, gender_from_this_context)


    
    gender_score_list = []
    this_context_score_list = []
    this_context_related_score_list = []

    
    # Creates a list of (Gender, This Context, This Related) scores for the guesses with 1.0 indicating a match
    for guess in guess_new:
        if guess in gender_match_guesses:
            gender_score_list.append(guess_map[guess] + ":" + str(1.0))
        else:
            gender_score_list.append(guess_map[guess] + ":" + str(0.0))

        if guess in this_context_guess_matches:
            this_context_score_list.append(guess_map[guess] + ":" + str(1.0))
        else:
            this_context_score_list.append(guess_map[guess] + ":" + str(0.0))

        if guess in this_context_related_guess_matches:
            this_context_related_score_list.append(guess_map[guess] + ":" + str(1.0))
        else:
            this_context_related_score_list.append(guess_map[guess] + ":" + str(0.0))

        
        
    gender_scores_dict.update({(qid, spos):gender_score_list})
    this_context_scores_dict.update({(qid, spos):this_context_score_list})
    this_context_related_scores_dict.update({(qid, spos):this_context_related_score_list})


# Dumps the scores
with open("final_train_gender_scores_dict.txt", "wb") as fp:
    pickle.dump(gender_scores_dict, fp)
    
fp.close()

with open("final_train_this_context_scores_dict.txt", "wb") as fp:
    pickle.dump(this_context_scores_dict, fp)
    
fp.close()

with open("final_train_this_context_related_scores_dict.txt", "wb") as fp:
    pickle.dump(this_context_related_scores_dict, fp)
    
fp.close()


# Same process as the above. This time for the test file



test = DictReader(open("test.csv", 'rU'))

gender_scores_dict = {}
this_context_scores_dict = {}
this_context_related_scores_dict = {}
count = 0


# Gets the list of guesses matching Gender, This Context, This Related Context for each question text
for ii in test:   
    count += 1
    
    qid = ii['Question ID']
    spos = ii['Sentence Position'] 
    ques = ii['Question Text']
    
    
    # Gets all guess words in IR Wiki and QANTA Scores
    guess_words = []
    guesses = ii['IR_Wiki Scores'] + ", " + ii['QANTA Scores']
    words = re.split(',[^_]', guesses)
    words = list(set(words))

    
    # Creates a list of guesses
    # guess_original is the original list of guesses as present in the test.csv
    # guess_new is the pre-processed list of guesses
    # guess_map is a dictionary to map guess_new to its corresponding guess_original
    guess_original = []
    for word in words:
        guess = word.split(":")[0].rstrip().lstrip()
        guess_original.append(guess)

    guess_original = list(set(guess_original))

    guess_new = []
    guess_map = {}
    for item in guess_original:
        modified_guess = remove_punct(item)
        guess_new.append(modified_guess)
        guess_map.update({modified_guess : item})
        


    # Gets list of guesses matching This_Context words, This_Related words, Gender in the question text
    (ques_this_context, this_context_guess_matches, ques_this_context_related, this_context_related_guess_matches, gender_from_this_context) = this_context(qid, spos, guess_new)
    (ques_gender_cat, gender_match_guesses) = freebase_gender(qid, spos, guess_new, gender_from_this_context)

    
    gender_score_list = []
    this_context_score_list = []
    this_context_related_score_list = []
    

    # Creates a list of (Gender, This Context, This Related) scores for the guesses with 1.0 indicating a match
    for guess in guess_new:
        if guess in gender_match_guesses:
            gender_score_list.append(guess_map[guess] + ":" + str(1.0))
        else:
            gender_score_list.append(guess_map[guess] + ":" + str(0.0))

        if guess in this_context_guess_matches:
            this_context_score_list.append(guess_map[guess] + ":" + str(1.0))
        else:
            this_context_score_list.append(guess_map[guess] + ":" + str(0.0))

        if guess in this_context_related_guess_matches:
            this_context_related_score_list.append(guess_map[guess] + ":" + str(1.0))
        else:
            this_context_related_score_list.append(guess_map[guess] + ":" + str(0.0))

        
        
    gender_scores_dict.update({(qid, spos):gender_score_list})
    this_context_scores_dict.update({(qid, spos):this_context_score_list})
    this_context_related_scores_dict.update({(qid, spos):this_context_related_score_list})



# Dumps the scores
with open("final_test_gender_scores_dict.txt", "wb") as fp:
    pickle.dump(gender_scores_dict, fp)
    
fp.close()

with open("final_test_this_context_scores_dict.txt", "wb") as fp:
    pickle.dump(this_context_scores_dict, fp)
    
fp.close()

with open("final_test_this_context_related_scores_dict.txt", "wb") as fp:
    pickle.dump(this_context_related_scores_dict, fp)
    
fp.close()
