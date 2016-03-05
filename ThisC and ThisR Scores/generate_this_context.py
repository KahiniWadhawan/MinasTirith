'''Generates a set of guesses matching This Context and This Related words on question text.
    Gender of question text based on word "This" is also generated here and are used in other modules '''

import cPickle as pickle
from csv import DictReader
import re, nltk, inflect
import string

# "this_qtext_dump_v0.txt" is dump containing words that are dependent on the word "This" for every question text
# Dependent words were found by dependency parsing using Stanford Parser
qtcontext = "this_qtext_dump_v0.txt"

with open(qtcontext,'r') as fp:
    questionContext = pickle.load(fp)
fp.close()


# "this_relatedwords_dumpv0.txt" is dump containing synonyms of the words that are dependent on the word "This" for every question text
qtcontext_related = "this_relatedwords_dumpv0.txt"

with open(qtcontext_related,'r') as fp:
    questionContextRelated = pickle.load(fp)
fp.close()


# "gender_from_this_context.txt" is dump containing gender of the question text based on "This" for every question text
gender_from_this_context = "gender_from_This_context.txt"

with open(gender_from_this_context ,'r') as fp:
    thisGender = pickle.load(fp)
fp.close()


# "this_guess_dumpv1.txt" is dump containing words list of words that represent the guess.
# This list was taken using Freebase which has the required info under "notable for"/ "notable type" for each topic
guesscontext = "this_guess_dumpv1.txt"

with open(guesscontext,'r') as fp:
    guessContext = pickle.load(fp)
fp.close()


# Gives set of guesses matching This context, This Related words in question text and also Gender of question text based on "This"
def this_context(questionID, sposition, guesses):
    this_context_guess_matches = {}
    this_context_related_guess_matches = {}
    try:
        qt_context = questionContext[(questionID, sposition)]
    except:
        qt_context = set([])

        
    # Returns empty sets if the question text does not have "This"
    if qt_context == None or qt_context == set([]):
        return (set([]), this_context_guess_matches, set([]), this_context_related_guess_matches, None)

    # Looks for gender indicating words in the list of words dependent on "This"
    if ('man' in qt_context or 'mans' in qt_context or 'boy' in qt_context):
        gender = ['Male']
    elif ('woman' in qt_context or 'womans' in qt_context or 'lady' in qt_context or 'girl' in qt_context):
        gender = ['Female']
    elif ('person' in qt_context or 'persons' in qt_context):
        gender = ['Male','Female']
    else:
        gender = []
    qt_context_related = set([])


    # Removes 'this' context words which denote gender (or) are verbs
    for item in qt_context.copy():
        if item in ['man', 'mans', 'boy', 'woman', 'womans', 'lady', 'girl', 'person', 'persons']:
            qt_context.remove(item)
        else:
            if nltk.pos_tag(item.split())[0][1] in ['VB', 'VBD','VBG', 'VBN', 'VBP', 'VBZ']:
                qt_context.remove(item)
               
    if len(qt_context)> 0:
        for item in qt_context:
            if item in questionContextRelated.keys():
                qt_context_related = set.union(qt_context_related, questionContextRelated[item])

                

    # Removes 'this' related words which denote gender (or) are verbs
    for item in qt_context_related.copy():
        if item in ['man', 'mans', 'boy', 'woman', 'womans', 'lady', 'girl', 'person', 'persons']:
            qt_context_related.remove(item)
        else:

            if nltk.pos_tag(item.split())[0][1] in ['VB', 'VBD','VBG', 'VBN', 'VBP', 'VBZ']:
                qt_context_related.remove(item)

    for item in qt_context:
        if item in thisGender.keys():
            gender += thisGender[item]

    gender = set(gender)

    if (gender == set([]) or gender == set([''])):
        gender = None
        


    # Taking only the singular form of This context
    p = inflect.engine()
    qt_context_copy = []

    for item in qt_context:
        try:
            sing_noun = p.singular_noun(item)
            if sing_noun != False and type(sing_noun) == str:
                qt_context_copy.append(sing_noun)
            else:
                qt_context_copy.append(item)
        except:
            qt_context_copy.append(item)
            pass
            

    qt_context = set(qt_context_copy)
 

    # Pre-processes guesses and looks for guesses matching question text's 'This' context and related words
    for guess in guesses:

        if '_' in guess:
            guess = guess.replace('_', ' ')
        if '&amp;' in guess:
            guess = guess.replace('&amp;', '&')
        if '&quot;' in guess:
            guess = guess.replace;('&quot;', '"')
    
        guess = re.sub('[%s]' % re.escape(string.punctuation), '', guess)

        if guess in guessContext.keys():
            try:
                guess_context = guessContext[guess]

                
            except:
                guess_context = set([])
                pass
            
            if (guess_context == None or guess_context == ''):
                guess_context = set([])
        else:
            guess_context = set([])


        
        intersection_length_qt_context = len(set.intersection(qt_context, guess_context))
        intersection_length_qt_context_related = len(set.intersection(qt_context_related, guess_context))
            
        if (guess_context!=None and guess_context!= set([]))  and intersection_length_qt_context > 0:
            this_context_guess_matches.update({guess: intersection_length_qt_context})

        if (guess_context!=None and guess_context!= set([]))  and intersection_length_qt_context_related > 0:
            this_context_related_guess_matches.update({guess: intersection_length_qt_context_related})

    return (qt_context, this_context_guess_matches, qt_context_related, this_context_related_guess_matches, gender)



