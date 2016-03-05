#For Creating LSI Scores and dumping into a Dictionary 

import cPickle as pickle
import logging
from gensim import corpora, models, similarities
import re
import string
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import nltk
from csv import DictReader, DictWriter


stopwords = set(nltk.corpus.stopwords.words())
#storing similarity scores in dict 
sim_scores = {}
cont = 0 



def remove_punct(guess):
	if '_' in guess:
      		guess = guess.replace('_', ' ')
	if '&amp;' in guess:
                guess = guess.replace('&amp;', '&')
	if '&quot;' in guess:
        	guess = guess.replace('&quot;', '"')
				
	guess = re.sub('[%s]' % re.escape(string.punctuation), '', guess)
	
	return guess

#Main function for LSI scores generation
#Using Gensim, TF-IDF and LSI Model  
def similarity():
	cont = 0
	train = DictReader(open("train.csv", 'rU'))
	count = 0 
	correct = 0
	#loading noun txt
	#Giving more weight to noun words  
	with open("nouns.txt","rb") as fn: 
		nouns = pickle.load(fn)

	#storing similarity scores in dict 
        for ii in train:   #reading each question row
		cont +=1
		qid = ii['Question ID']
		spos = ii['Sentence Position']
		#dir of dumped dictionary and corpus 
		dirname = "sim_dumps_corrected/" +  ii['Question ID'] + "_" + ii['Sentence Position']  
		dictname = dirname + ".dict"
		corpusname = dirname + ".mm"
		#text file contains guess words stored in position that matches to their index in lsi model doc.
		#this will be used in later part of this code. 
		txtname =  dirname +   ".txt"   	        	
		
		#loading dictionary and corpus
		dictionary = corpora.Dictionary.load(dictname)
		corpus = corpora.MmCorpus(corpusname) # comes from the first tutorial, "From strings to vectors"
		tfidf = models.TfidfModel(corpus)
		lsi = models.LsiModel(tfidf[corpus], id2word=dictionary, num_topics=300)
		#lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=300)	
		
		#forming guess list 
		ft = open(txtname,'r' )
		guess_words = []
		for line in ft:
			guess_words.append(line.replace("\n",""))
		#print "$$$$$$$$$$$$$ guess_words ::", guess_words
		ques = ii['Question Text']
		#print "ques ::",ques, " ", ii['Sentence Position']		

 		ques = ques.translate(None, string.punctuation).lower()
		#ques = re.sub('[%s]' % re.escape(string.punctuation), '', ques)

		tokens = ques.split()
		ques_tokens = []
		for word in tokens:
			if word in stopwords:
				pass
			#up-weighting nouns in tokens
			#nouns come from nouns list above  
			if word+"\r" in nouns:   
				ques_tokens.append(word)
				ques_tokens.append(word)
				ques_tokens.append(word)
				ques_tokens.append(word)

			else:
				ques_tokens.append(word)
		vec_bow = dictionary.doc2bow(ques_tokens)
		vec_lsi = lsi[vec_bow] # convert the query to LSI space
		#print(vec_lsi)

		index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
		sims = index[vec_lsi] # perform a similarity query against the corpus
		
		sims = sorted(enumerate(sims), key=lambda item: -item[1])
		print(sims) # print sorted (document number, similarity score) 2-tuples	
		#adding sim scores to dict for dump
		#get back original guess word 
		guess_orig = ii['IR_Wiki Scores'] + ", " +  ii['QANTA Scores']
		words = re.split(',[^_]', guess_orig)
		guess_o = []
		for word in words:
                	gues = word.split(":")[0].rstrip().lstrip()
			guess_o.append(gues)
		guess_o = list(set(guess_o))
		
		#mapping guess with orig 
		guess_map = {}
		for word in guess_words:
			for orig in guess_o:
				orig_stp = remove_punct(orig)
				if orig_stp == word:
					guess_map[word]= orig
		
		#replace doc id with guess word 
		sims_new = []
		for tup in sims:
			ind = tup[0]
			guess = guess_words[ind]
			sims_new.append(guess_map[guess] + ":"+ str(tup[1]))
		#print "sims_new ::", sims_new
		sim_scores[qid,spos] = sims_new
		
		#checking accuracy - just a local accuracy indicator, not required for lsi generating scores 
		sim_max_ind = sims[0][0]
		sim_max_ind2 = sims[1][0]
		sim_max_ind3 = sims[2][0]
		sim_max_ind4 = sims[3][0]
		sim_max_score = sims[0][1]
		
		#print "######## sim_max::", sim_max_ind, sim_max_score

		#checking with answer 
		sim_res = []
		sim_res.append(guess_words[sim_max_ind])
		sim_res.append(guess_words[sim_max_ind2])
		sim_res.append(guess_words[sim_max_ind3])
		#sim_res.append(guess_words[sim_max_ind4])
		"""
		sim_res.append(sims_new[0][0])
		sim_res.append(sims_new[1][0])
		sim_res.append(sims_new[2][0])
		sim_res.append(sims_new[3][0])
		"""
		#sim_res = guess_words[sim_max_ind]
		
		"""answer = ii['Answer']
		#purify answer 
		if '_' in answer:
                	answer = answer.replace('_', ' ')
		if '&amp;' in answer:
                	answer = answer.replace('&amp;', '&')
		if '&quot;' in answer:
                	answer = answer.replace('&quot;', '"')
			
		answer = re.sub('[%s]' % re.escape(string.punctuation), '', answer)

		
		print "answer and sim_res :: ", answer, sim_res
		count += 1
		if answer in sim_res:
			print "#################Correct"
			correct += 1
		else:
			print "#################Wrong"

	#accuracy % 
	accuracy = (correct/float(count)) * 100 
	print "accuracy :;", correct, count, accuracy	"""
		#dumping scores in a dict after every 500 rows
		if cont % 500 == 0:
			print "sim dict len ::", len(sim_scores)
			fname = "SimDict/sim_scores_train_dict_redone_" + str(cont) + ".txt"
 			with open(fname,"wb") as fp:
				pickle.dump(sim_scores,fp)
			fp.close()

		
#cont = 0 				
similarity()

#print "sim dict len ::", len(sim_scores)
#dumping scores in a dict after all the training data rows are processed
"""with open('sim_scores_train_dict_redone.txt',"wb") as fp:
	pickle.dump(sim_scores,fp)
	fp.close()"""

