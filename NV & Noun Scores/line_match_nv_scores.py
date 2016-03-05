#Generate NV Scores/Noun Scores 
#Generate line to line similarity scores based on Noun, Verb and Date if NV Scores
#Else based on Just Nouns if Noun Scores 

import pickle, string, nltk
import cPickle as pickle
import logging
from gensim import corpora, models, similarities
import re, enchant
import string
import nltk
from csv import DictReader, DictWriter
import itertools, math, operator

# Added by manju
#from generate_guess_genders import freebase_gender
#from generate_this_context import this_context

stopwords = set(nltk.corpus.stopwords.words())
enchant_dict = enchant.Dict("en_US")
noun_scores = {} 

#separates an article into sentences 
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


#function for finding similarity based on Noun, verb or date match between lines of question and a guess article
def filter_guess(ques,guess_words, qid, spos):
        guess_ext = []
        #guess articles dump dir 
        dirname = "dumps_corrected/"

        documents = []  #list for keeping list of lines of all guess word articles. its a list of list. each sublist is a line 

        # Added by manju
        #(ques_this_context, this_context_guess_matches, ques_this_context_related, this_context_related_guess_matches, gender_from_this_context) = this_context(qid, spos, guess_words)

        #print "ques_this_context", ques_this_context
        #print "this_context_matches", this_context_guess_matches
        #print "gender_from_this_context", gender_from_this_context
        
        #print "\n"
        
        #ques_gender_cat, gender_match_guesses = freebase_gender(qid, spos, guess_words, gender_from_this_context)

        #print ques_gender_cat, gender_match_guesses

        #print "\n"
         
        for item in guess_words:
                fname = item + ".txt"
                with open(dirname + fname, "rb") as f:
                    
                    data = pickle.load(f)
                    linecount = 0
                    for line in data.splitlines():   #splitting articles into lines
                            linecount += 1
                            line = line.translate(None, string.punctuation).lower()
                            tokens = line.split()
                            line_tokens = [item, linecount]   #adding guess word in the list of line tokens,to identify which guess word this line belongs to 
                            for word in tokens:    #for each word in the line
                                    if word in stopwords:
                                            pass
                                    else:
                                            line_tokens.append(word) 
                            documents.append(line_tokens)  #adding list of line tokens to a global list. 
        
	qlines_guess_ext = {}
        qlines_inter_top10 = {}
        ques_lines = sentence_finder.split(ques)
        
        for qline_ind,qline in enumerate(ques_lines):
                #purify question text into tokens 
                if '_' in qline:
                        qline = qline.replace('_', ' ')

                qline = re.sub('[%s]' % re.escape(string.punctuation), '', qline)
        
                tagged = nltk.pos_tag(qline.split())
                
               # noun_list = set([x for (x, y) in tagged if y in ['NN', 'NNS', 'NNP', 'NNPS', 'CD', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']])   #use this for NV scores 
                noun_list = set([x for (x, y) in tagged if y in ['NN', 'NNS', 'NNP', 'NNPS']])   #use this Noun scores 
		
		#Kahini
                #calculate IDF scores 
                total_count = len(documents)   #total no. of docs
                idfs = {}
                for word in noun_list:
                        wcount = 0
                        for lst in documents:
                                if lst.count(word) > 0:
                                        wcount += 1
                        if enchant_dict.check(word) == False:
                                wcount = wcount / 100
                        widf = math.log(total_count/float(1+wcount))
                        idfs[word] = widf
		#find intersection between question lines and guess article lines based on noun list
                intersection = [set.intersection(noun_list, set(sublist)) for sublist in documents]
                
		interlen = []
                idf_scores = []
                count = -1

                for sublst in intersection:
                        
                        count += 1
                        idf_score = sum([idfs[x] for x in sublst])
                        interlen.append((sublst,count ,idf_score))

                #sort the interlen 
                interlen_sor = sorted(interlen, key=lambda tup: tup[2] , reverse = True)
                #take top hundred 
                inter_top10 = interlen_sor[:100]
                
		#storing lines of top100 
                lines = []
                guess_ext = []
                for tup in inter_top10:
                        lines.append(documents[tup[1]])
                        guess_ext.append(documents[tup[1]][0])  #in decreasing order of ranking
                qlines_guess_ext[qline_ind] = guess_ext
                qlines_inter_top10[qline_ind] = inter_top10
                #extracting guess word

        #print "qlines_guess_ext :: ",qlines_guess_ext
        #gen dict of ranks and spos 
        rank_dict = {} 
        top = 100
        for key,value in qlines_guess_ext.iteritems():
                for i in xrange(top):
                        guess = value[i]
                        spos = key
                        rank = i+1
                        if guess in rank_dict.keys():
                                rank_dict[guess].append((spos,rank))
                        else: 
                                rank_dict[guess]= [(spos,rank)]

        #cal score - sum of inverse of ranks and then take log 
        score_dict = {} 
        for key,lst in rank_dict.iteritems():
                summ = 0 
                for tup in lst:
                        if tup[1] != 0:
                                summ += 1/float(tup[1])
                score_dict[key] = math.log(summ)
        score_dict_sor = sorted(score_dict.items(), key=operator.itemgetter(1), reverse = True)
        
        return score_dict_sor
        
def remove_punct(guess):
        if '_' in guess:
                guess = guess.replace('_', ' ')
        if '&amp;' in guess:
                guess = guess.replace('&amp;', '&')
        if '&quot;' in guess:
                guess = guess.replace('&quot;', '"')
                                
        guess = re.sub('[%s]' % re.escape(string.punctuation), '', guess)
        
        return guess


#main function for generating scores 
def similarity():
        
        train = DictReader(open("test.csv", 'rU'))
        count = 0 
        correct = 0
        cont = 0
        
	#loading noun txt 
        with open("nouns.txt","rb") as fn: 
                nouns = pickle.load(fn)

        for ii in train:   #reading each question row
                qid = ii['Question ID']
                spos = ii['Sentence Position'] 
                ques = ii['Question Text']
                print "ques ::",ques, " ", ii['Sentence Position']
                guess_o = []   #score dict
                guess_words = []
                guesses = ii['IR_Wiki Scores'] + ", " + ii['QANTA Scores']
                words = re.split(',[^_]', guesses)

               
                words = list(set(words))
		
                for word in words:
                        guess = word.split(":")[0].rstrip().lstrip()
			guess_o.append(guess) #score dict
                        if '_' in guess:
                                guess = guess.replace('_', ' ')
                        if '&amp;' in guess:
                                guess = guess.replace('&amp;', '&')
                        if '&quot;' in guess:
                                guess = guess.replace('&quot;', '"')
                        
                        guess = re.sub('[%s]' % re.escape(string.punctuation), '', guess)
                        guess_words.append(guess)
                
                uniq_guess_words = list(set(guess_words))
		guess_o = list(set(guess_o))  #score dict 
		#guess word is stripped so cannot be directly matched  
		#so mapping stripped guess with orig guess form  
		guess_map = {}
		for word in uniq_guess_words:
			for orig in guess_o:
				orig_stp = remove_punct(orig)
				if orig_stp == word:
					guess_map[word]= orig   #key - strp guess, val - orig guess
		#calling filter_guess func
		guess_ext = filter_guess(ques,guess_words, qid, spos)

		nouns_new = []
		for tup in guess_ext:
			guess = tup[0]
			#guess = guess_words
			nouns_new.append(guess_map[guess] + ":"+ str(tup[1]))
		#print "nouns_new ::", nouns_new
		noun_scores[qid,spos] = nouns_new
		
		#the below commented portion is just for calculating local feature accuracy
		#not required for score generation process
	"""
                sim_res = []
		cont = 0
                for tup in guess_ext:
			cont +=1
			if cont < 4 : 
                		sim_res.append(tup[0])
                #print "sim_res :: ", sim_res
                                
                answer = ii['Answer']
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
                        if answer not in uniq_guess_words:
                                cont += 1
                                print "#################Wrong : Answer not in Guess Words"
                        else:                               
                                print "#################Wrong"
        
	accuracy = (correct/float(count)) * 100 
        print "accuracy :;", correct, count, accuracy

        missing = cont/ float(count) * 100
        print "missing ::  ", missing, cont
           """     

similarity()

#dumping NV scores into a dictionary 
with open('noun_scores_test_redone.txt',"wb") as fp:
        pickle.dump(noun_scores,fp)
        
fp.close()


