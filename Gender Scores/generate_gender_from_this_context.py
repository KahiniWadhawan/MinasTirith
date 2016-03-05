''' Generates the gender of the question text using the word "This" '''

import cPickle as pickle
from csv import DictReader
import re, en
import string
from nltk.corpus import wordnet as wn

# Gets the set of words dependent on "This".
# "this_qtext_dump_v0.txt" is a dump that has the words dependent on "This" in the question text

qtcontext = "this_qtext_dump_v0.txt"

with open(qtcontext,'r') as fp:
    questionContext = pickle.load(fp)
fp.close()
   
this_contexts = set([])


for key in questionContext:
    this_contexts = set.union(this_contexts,questionContext[key])


# Uses WordNet hypernyms to see whether the words in 'this_contexts' have 'person_synset'/ 'male_synset'/ 'female_synset'
person_synset = wn.synset('person.n.01')
male_synset = wn.synset('male.n.01')
female_synset = wn.synset('female.n.01')

gender_dict = {}

for item in this_contexts:
    # Gets all hypernyms for 'this_contexts' words
    try:
        item_synset = wn.synsets(item)[0]
        hypernyms_item = set([i for i in item_synset.closure(lambda s:s.hypernyms())])
    except:
        pass

    # Checks for male/ female/ person synsets in hypernyms 
    if person_synset in hypernyms_item:
        if male_synset in hypernyms_item and female_synset not in hypernyms_item:
            gender = ['Male']
        elif female_synset in hypernyms_item and male_synset not in hypernyms_item:
            gender = ['Female']
        else:
            gender = ['Male', 'Female']
    else:
        gender = ['other']

    gender_dict.update({item : gender})



# Dumps gender into "gender_from_This_context.txt"      
with open("gender_from_This_context.txt", 'a') as tgd:
    pickle.dump(this_context_gender, tgd)
tgd.close()
