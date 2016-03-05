#Creating dumps for LSI Scores

import cPickle as pickle
import logging
from gensim import corpora, models, similarities
import re
import string
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import nltk
from csv import DictReader, DictWriter


stopwords = set(nltk.corpus.stopwords.words())

def guess_dic_corpus_dump():

	#just provide Wiki Guess articles dir as dirname & destpath for dumps 
	dirname = "dumps_corrected/"      #Source dir for picking Guess Articles 
	destname = "sim_dumps_corrected/"   #dest dir for dumping corpus and dict 
	
	train = DictReader(open("train.csv", 'rU'))
	count = 0 
	#dumps for each question row 
        for ii in train:   #reading each question row 
		count += 1 
		documents = []
		guess_words = []
        	guesses = ii['IR_Wiki Scores'] + ", " + ii['QANTA Scores']
        	words = re.split(',[^_]', guesses)
		
        	for word in words:
                	guess = word.split(":")[0].rstrip().lstrip()
                	if '_' in guess:
                    		guess = guess.replace('_', ' ')
			if '&amp;' in guess:
                		guess = guess.replace('&amp;', '&')
			if '&quot;' in guess:
                		guess = guess.replace('&quot;', '"')
			
			guess = re.sub('[%s]' % re.escape(string.punctuation), '', guess)
                	guess_words.append(guess)
		
		#creating a list of uniques guess words from QANTA & Wiki guesses
		uniq_guess_words = list(set(guess_words))
		
		#storing guess_list 
		guessfname = destname + ii['Question ID'] + "_" + ii['Sentence Position'] + ".txt"
		fp = open(guessfname,"w")
		
		#fetching guess article for each guess  		
		for guess in uniq_guess_words:
			#writing guess to guess txt
			#guess index in txt file is same as index in lsi - used later while creating lsi scores  
			fp.write(guess + "\n")

			fname = guess + ".txt"
	 		#docs are maintained as list of strings
			print "path ::", dirname + fname
			with open(dirname+fname, "rb") as f:
    				data = pickle.load(f)
	    			data = data.translate(None, string.punctuation).lower()
				tokens = data.split()
				data_tokens = []
				for word in tokens:
					if word in stopwords:
						pass
					else:
						data_tokens.append(word)
							
 				documents.append(data_tokens)
				f.close()
		fp.close()

		#print "documents len :: ", len(documents)
	
		#for each qs and its list of guesses - store a dict of articles of guesses
		dictname = destname + ii['Question ID'] + "_" + ii['Sentence Position'] + ".dict"
		print "dictname ::", dictname
		dictionary = corpora.Dictionary(documents)
		dictionary.save(dictname) # store the dictionary, for future reference
		#print(dictionary)
		#print(dictionary.token2id)

		#creating corpus - from the dict
		corpusname =  destname + ii['Question ID'] + "_" + ii['Sentence Position'] + ".mm"
		corpus = [dictionary.doc2bow(doc) for doc in documents]
		corpora.MmCorpus.serialize(corpusname, corpus) # store to disk, for later use
		#print(corpus)


guess_dic_corpus_dump()


