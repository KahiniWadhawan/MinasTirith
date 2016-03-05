# -*- coding: utf8 -*-
'''Creates a list of words that are synonyms of words dependent on "This"''' 
import cPickle as pickle
import wordnik, re
from wordnik import *


apiUrl = 'http://api.wordnik.com/v4'
apiKey = '1082e4ca71806c679100c089c6d0c4a1cf0f28f50539da54d'

client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)

this_relatedwords_dict = {}

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

with open("this_qtext_dump_v0.txt", 'r') as fp:
    this_dump_dict = pickle.load(fp)
fp.close()

this_contexts = set([])


for key in this_dump_dict:
    this_contexts = set.union(this_contexts,this_dump_dict[key])





count = 0
for context in this_contexts:
    try: 
        count += 1
        # Replaces punctuations
        if '&amp;' in context:
            context = context.replace('&amp;', '&')

        if '&quot;' in context:
            context = context.replace('&quot;', '"')

        if '_' in context:
            context = context.replace('_', ' ')

        # Gets synonyms from wordnik
        list_relatedwords = []
        relatedwords_context = wordApi.getRelatedWords(context)

        for item in relatedwords_context:
            list_relatedwords += [x.lower() for x in item.words]

        set_relatedwords = set(list_relatedwords)

        this_relatedwords_dict.update({context: set_relatedwords})
        
    except TypeError:
        pass
 
    
# Dumps here
with open("this_relatedwords_dumpv0.txt", 'a') as tgd:
    pickle.dump(this_relatedwords_dict, tgd)
tgd.close()

