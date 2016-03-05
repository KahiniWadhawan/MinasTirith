import wikipedia
import cPickle as pickle
import string
from csv import DictReader, DictWriter
import re
import nltk

"""
This is a utility class which helps dumping all the unique guesses from the training and test data.
"""
class GuessDump:
    
    def web_lookup(self):

        filename = "guessdump.txt"
        all_guesses = []
        
        guess_words = []
        train = DictReader(open("train_final.csv", 'r'))
        for ii in train:
            guesses = ii['IR_Wiki Scores'] + ii['QANTA Scores']
            words = re.split(',[^_]', guesses)

            for word in words:
                guess = word.split(":")[0].rstrip().lstrip()
                if '_' in guess:
                    guess_words.append(guess.replace('_', ' '))
                else:
                    guess_words.append(guess)

        counter = 0
        for guesses in list(set(guess_words)):
            if '&amp;' in guesses:
                guesses = guesses.replace('&amp;', '&')
            if '&quot;' in guesses:
                guesses = guesses.replace('&quot;', '"')

            guesses = re.sub('[%s]' % re.escape('!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'), '', guesses)

            all_guesses.append(guesses)
            counter+=1

            print "Done ", counter, " Out of ", len(list(set(guess_words)))


        guess_words = []
        test = DictReader(open("test.csv", 'r'))
        for ii in test:
            guesses = ii['IR_Wiki Scores'] + ii['QANTA Scores']
            words = re.split(',[^_]', guesses)

            for word in words:
                guess = word.split(":")[0].rstrip().lstrip()
                if '_' in guess:
                    guess_words.append(guess.replace('_', ' '))
                else:
                    guess_words.append(guess)

        counter = 0
        for guesses in list(set(guess_words)):
            if '&amp;' in guesses:
                guesses = guesses.replace('&amp;', '&')
            elif '&quot;' in guesses:
                guesses = guesses.replace('&quot;', '"')

            guesses = re.sub('[%s]' % re.escape(string.punctuation), '', guesses)

            all_guesses.append(guesses)
            counter+=1

            print "Done ", counter, " Out of ", len(list(set(guess_words)))


        with open(filename, 'wb') as fp:
            pickle.dump(all_guesses, fp)
        fp.close()


if __name__=="__main__":
    ad = GuessDump()
    ad.web_lookup()
