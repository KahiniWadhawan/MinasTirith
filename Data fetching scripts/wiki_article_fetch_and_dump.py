import wikipedia
import cPickle as pickle
import string
from csv import DictReader, DictWriter
import re
import nltk

"""
This class is used to fetch articles from wiki and dump it locally so that the runtime for the program is reduced.
"""
class ArticleDump:
    
    def web_lookup(self):
        """
        We made use of the wikipedia package available in python to fetch the articles from Wikipedia. The guesses present in the training data correspond to
        articles in wikipedia and they are fetched and dumped locally.
        """
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
        
        #Unique guess articles are fetched. Below is some code to handle discrepency in the training data
        for guesses in list(set(guess_words)):
            if '&amp;' in guesses:
                guesses = guesses.replace('&amp;', '&')
            elif '&quot;' in guesses:
                guesses = guesses.replace('&quot;', '"')

            guesses = re.sub('[%s]' % re.escape('!"#$%\*+,./:;<=>?@[\\]^_`{|}~'), '', guesses)
            guess_count_score = {}
            
            try:
                #For each guess, we fetch the wikipedia page. The below line shows the code for the same.
                wiki_content = wikipedia.page(guesses).content.lower().encode("utf8")
            except wikipedia.exceptions.DisambiguationError as e:
                wiki_content = wikipedia.page(e.options[0]).content.lower().encode("utf8")
            except wikipedia.exceptions.PageError as pe:
                print "Exception for guess: ", guesses

            guesses = re.sub('[%s]' % re.escape(string.punctuation), '', guesses) 
            guess_filename = "dumps_final1/"+guesses+".txt"
            #Used cPickle to dump wikipedia articles.
            with open(guess_filename, 'wb') as fp:
                pickle.dump(wiki_content, fp)
            fp.close()

            counter+=1
            #Counter maintained for debugging purposes only.
            print "Done ", counter, " Out of ", len(list(set(guess_words)))

        # Same holds good for test data also
        guess_words = []
        train = DictReader(open("test.csv", 'r'))
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
            elif '&quot;' in guesses:
                guesses = guesses.replace('&quot;', '"')

            guesses = re.sub('[%s]' % re.escape('!"#$%\*+,./:;<=>?@[\\]^_`{|}~'), '', guesses)
            guess_count_score = {}
            
            try:
                wiki_content = wikipedia.page(guesses).content.lower().encode("utf8")
            except wikipedia.exceptions.DisambiguationError as e:
                wiki_content = wikipedia.page(e.options[0]).content.lower().encode("utf8")
            except wikipedia.exceptions.PageError as pe:
                print "Exception for guess: ", guesses

            guesses = re.sub('[%s]' % re.escape(string.punctuation), '', guesses) 
            guess_filename = "dumps_final1/"+guesses+".txt"
            with open(guess_filename, 'wb') as fp:
                pickle.dump(wiki_content, fp)
            fp.close()

            with open(filename, 'a') as fp:
                pickle.dump(guesses+"-->"+guess_filename, fp)
            fp.close()

            counter+=1
            #Counter maintained for debugging purposes only.
            print "Done ", counter, " Out of ", len(list(set(guess_words)))

if __name__=="__main__":
    ad = ArticleDump()
    ad.web_lookup()
