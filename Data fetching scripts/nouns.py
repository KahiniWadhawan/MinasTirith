import cPickle as pickle
import string
from csv import DictReader, DictWriter
import re
import nltk
from pattern.en import tag

"""
This class is used to get all the nouns and adjectives from the training and test data.
"""
class NounDump:

    def tagging(self, sentence):
        filename = "nouns.txt"
        filename1 = "adjectives.txt"
        tags = tag(sentence)
        #POS tagging to get the required words corresponding to the below Noun and Adjective Tags
        tags_n = [word for word, pos in tags if pos in ['NN','NNS','NNP','NNPS']]
        tags_adj = [word for word, pos in tags if pos in ['JJ','JJS','JJR']]
        #Dumping noun and adjective tags respectively
        with open(filename, 'a') as fp:
            pickle.dump(tags_n, fp)
        fp.close()
        with open(filename1, 'a') as fp:
            pickle.dump(tags_adj, fp)
        fp.close()

if __name__ =="__main__":

    nd = NounDump()
    train = DictReader(open("train_final.csv", 'r'))
    all_questions = []
    for ii in train:
        qtext = ii['Question Text']
        all_questions.append(qtext)
    test = DictReader(open("test.csv", 'r'))
    for ii in test:
        qtext = ii['Question Text']
        all_questions.append(qtext)
    nd.tagging(" ".join(all_questions))
        
    
