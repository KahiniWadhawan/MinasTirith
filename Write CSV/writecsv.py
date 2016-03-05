#Script for reading dumped dictionaries of scores and writing it to csv 
#Read questionId and Sentence position from training.csv or test.csv
#Generate a new csv with columns - Question ID, Sentence Position & Scores

from csv import DictReader, DictWriter
import cPickle as pickle
import csv


#load scores dictionary 
with open('sim_scores_test_dict.txt',"rb") as fp:
	dicti = pickle.load(fp)
	#print dicti
	fp.close()


train = DictReader(open("train.csv", 'rU'))

o = DictWriter(open('train_sim.csv', 'wb'), ['Question ID', 'Sentence Position', 'Sim Scores'])
o.writeheader()
            
cont = 0
for ii in train:
	if(2 == 2 ):
		print "cont :: ", cont 
		qid = ii['Question ID']
		spos = ii['Sentence Position'] 
		sim_scores = dicti[(qid,spos)]
		print "sim_scores ::", sim_scores
		sim = ""
		count = 0
		for s in sim_scores:
			if count == 0: 
				sim = s
			else:
				sim += "," + s
			count += 1
		#write
		o.writerow({'Question ID': qid, 'Sentence Position': spos, 'Sim Scores': sim})
		cont +=1
		print "count :: ", cont	
