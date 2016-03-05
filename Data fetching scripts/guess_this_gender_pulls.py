# -*- coding: utf8 -*-

'''Used to get gender and topic types(to be matched with "this" context words/ related words in question text) of guesses.
    Data used: Freebase and Wikipedia'''

import simplejson, urllib, re, os
import cPickle as pickle
import string
from string import maketrans


this_guess_dict = {}
gender_dict = {}

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

with open("guessdump_trainandtestwith-.txt", 'r') as fp:
    guesses = pickle.load(fp)
fp.close()



transtab = maketrans("_", " ")
delete_chars = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

count = 0


for guess in guesses:
    
    # Replaces punctuations
    if '&amp;' in guess:
        guess = guess.replace('&amp;', '&')

    if '&quot;' in guess:
        guess = guess.replace('&quot;', '"')

    if '_' in guess:
        guess = guess.replace('_', ' ')
  
    
    guess_dumpversion = re.sub('[%s]' % re.escape(string.punctuation), '', guess)
    guess_freebaseversion = re.sub('[%s]' % re.escape('!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'), '', guess)

    # Takes content from Wikipedia 1st line for the guess
    f = open("/Users/manjhunathkr/Documents/NLP/Final Project/All Trials/All Dumps/dumps_final/"+guess_dumpversion+".txt", 'r')
    wiki_content = pickle.load(f)
    f.close()

    wiki_tokens = sentence_finder.split(wiki_content)[0].translate(transtab,delete_chars).split(" ")

    
    count += 1
    guess = guess.translate(transtab, delete_chars)

    # Pulls topic type and gender from Freebase for the guess
    try:
        query = guess_freebaseversion

        api_key = "AIzaSyCkS_lj0hVnsJ9c72Cj26mNB92wgI8qsLo"
        service_url = 'https://www.googleapis.com/freebase/v1/search'

        # parameters for topic type
        params = {
                'query': query,
                'key': api_key
        }
        url = service_url + '?' + urllib.urlencode(params)
        response = simplejson.loads(urllib.urlopen(url).read())

        # parameters for gender
        params2 = {
          'key': api_key,
          'filter': '/people/person/gender'
        }

        topic_service_url = 'https://www.googleapis.com/freebase/v1/topic'

        
        for result in response['result']:
            topic_id = result['mid']
            
            # updates dictionary with topic type from Freebase           
            try:
                this_guess_dict.update({guess_dumpversion : set(("/".join(result['notable']['name'].encode("utf8").lower().translate(transtab,delete_chars).split()).split("/")) + ("/".join(result['notable']['id'].encode("utf8").lower().translate(transtab,delete_chars).split()).split("/"))+ wiki_tokens)})

                
            except KeyError:
                this_guess_dict.update({guess_dumpversion : set([] + wiki_tokens)})
                pass
                


            topic_url = topic_service_url + topic_id + '?' + urllib.urlencode(params2)
            topic = simplejson.loads(urllib.urlopen(topic_url).read())


            # updates dictionary with gender from Freebase 
            try:
                for property in topic['property']:
                    for value in topic['property'][property]['values']:
                        gender_dict.update({guess_dumpversion :  value['text']})
                        break
                break
            except:
                gender_dict.update({guess_dumpversion : 'other'})
                break

        if count > 100:
            break

    except NameError:
        pass

    
    except KeyError:
        pass

    
# Dumps here
with open("this_guess_dumpv1.txt", 'a') as tgd:
    pickle.dump(this_guess_dict, tgd)
tgd.close()

with open("freebase_guess_gender_dumpv1.txt", 'a') as gd:
    pickle.dump(gender_dict, gd)
gd.close()
