'''Generates list of guesses whose gender match the genders identified in the question text'''

import cPickle as pickle
from csv import DictReader
import re
import string

# "questiontextpronouns_3.txt" is a dump that contains the gender referred by the question text
# Gender of the question text is identified by the first pronoun present in the question text
# This is used as a backup identifier when gender of question text cannot be idenitified by the word "This"
qtpronouns = "questiontextpronouns_3.txt"

with open(qtpronouns,'r') as fp:
    questionPronouns = pickle.load(fp)
fp.close()



# "freebase_guess_gender_dumpv1.txt" is a dump that identifies the gender of the guesses
# Gender of the guesses is identified using the Freebase gender property
guesspronouns = "freebase_guess_gender_dumpv1.txt"

with open(guesspronouns,'r') as fp:
    guessPronouns = pickle.load(fp)
fp.close()



# "wikipronouns.txt" is a dump that identifies the gender of the guesses
# Gender of the guesses is identified by the pronouns occuring in max. frequency in the 2nd and 3rd lines of wikipedia
# This is used as a backup gender identifier when gender of a guess cannot be identified by Freebase
wikiguesspronouns = "wikipronouns.txt"

with open(wikiguesspronouns,'r') as fp:
    wikiGuessPronouns = pickle.load(fp)
fp.close()



# Returns a tuple containing the gender of question text and a list of guesses having the gender of question text
def freebase_gender(questionID, sposition, guesses, gender_from_this_context):
    
    qt_cat = questionPronouns[(questionID, sposition)]
    
    # Checks if the gender of the question text can be identified by the word "This"
    # Else uses gender identified by pronouns
    if gender_from_this_context != None:
        qt_cat = list(gender_from_this_context)
    else:
        if qt_cat == 'female/person':
            qt_cat = ['Female']
        elif qt_cat == 'male/person':
            qt_cat = ['Male']
        else:
            qt_cat = ['other']


    
    category_guess = []
    for guess in guesses:
        # Pre-processing guess words
        if '_' in guess:
            guess = guess.replace('_', ' ')
        if '&amp;' in guess:
            guess = guess.replace('&amp;', '&')
        if '&quot;' in guess:
            guess = guess.replace;('&quot;', '"')
    
        guess = re.sub('[%s]' % re.escape(string.punctuation), '', guess)


        # Checks for gender of guesses that comes from Freebase;
        # If not present uses genders identified based on pronouns from Wiki
        if guess in guessPronouns.keys():
            try:
                guess_cat = guessPronouns[guess]
                
            except:
                guess_cat = None
                pass
            
            if guess_cat == '':
                guess_cat = None
        else:
            if guess in wikiGuessPronouns.keys():
                try:
                    guess_cat = wikiGuessPronouns[guess]

                    if guess_cat == 'female/person':
                        guess_cat = 'Female'
                    elif guess_cat == 'male/person':
                        guess_cat = 'Male'
                    else:
                        guess_cat = 'other'
                except:
                    guess_cat = None
                    pass

            if guess_cat == '':
                guess_cat = None
            else:
                guess_cat = None
                    


            
        if guess_cat == None or guess_cat in qt_cat:
            category_guess.append(guess)

    return (qt_cat, category_guess)
