'''Main file: Classifies answers'''

from collections import defaultdict
from csv import DictReader, DictWriter

import nltk, re, numpy, datetime, sys, sklearn, wikipedia as wiki


from sklearn import svm, tree
from multiprocessing import Value, Array
from FeaturePreparation import prepare
from FeatureExtractor import extractor

from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer
from stemming.porter2 import stem
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier

kTOKENIZER = TreebankWordTokenizer()

    
dev_train_prepare = FeaturePreparation.dev_train
dev_test_qid_prepare = FeaturePreparation.dev_test_qid
dev_test_prepare = FeaturePreparation.dev_test
full_train_prepare = FeaturePreparation.full_train



if __name__ == "__main__":

    time_start = datetime.datetime.now()

##    parser = argparse.ArgumentParser(description='Process some integers.')
##    parser.add_argument('--subsample', type=float, default=1.0,
##                        help='subsample this amount')
##    args = parser.parse_args()
    

    fe = extractor()
    
    # Read in training data
    train = DictReader(open("train_lsi.csv", 'rU'))

    count = 0
    for ii in train:
        count += 1
        
        qid = ii['Question ID']
        qtext = ii['Question Text']
        answer = ii['Answer']
        sposition = ii['Sentence Position']
        qscores = ii['QANTA Scores']
        wscores = ii['IR_Wiki Scores']
        sscores = ii['Sim Scores']
        nscores = ii['Noun Scores']
        isguessp = ii['IsGuessP Scores']
        thisr = ii['ThisR Scores']
        thisc = ii['ThisC Scores']
        gender = ii ['Gender Scores']
        subject_group = ii['category']
        country = ii ['Country Scores']
        nvscores = ii['NV Scores']

        if subject_group == 'history':
            subject_group = 1.0
            
        if subject_group == 'lit':
            subject_group = 2.0
            
        if subject_group == 'science':
            subject_group = 3.0
            
        if subject_group == 'social':
            subject_group = 4.0

        # Sends data for feature preparation
        prepare(qid, qtext, sposition, qscores, wscores, sscores, nscores, isguessp, thisr, thisc, gender, subject_group, nvscores, country, count, answer)
    

    
    dev_train = dev_train_prepare
    dev_test_qid = dev_test_qid_prepare
    dev_test = dev_test_prepare
    full_train = full_train_prepare

    X_dev_train = [feat_list for feat_list, answer in dev_train]
    Y_dev_train = [answer for feat_list, answer in dev_train]

    
    # Trains on dev_train
    print("Training classifier ...")
    clf = svm.SVC(kernel = 'linear', probability = True, verbose=True)
    clf.fit(X_dev_train, Y_dev_train)
    
    
    
    right = 0
    prediction_dict = defaultdict(list)

    # Predicts values on dev_test
    for ii in dev_test:
        prediction = clf.predict_proba([ii[3]])[0][1]
        prediction_dict[(ii[1], ii[2])].append((prediction, ii[0]))

    total = len(set(dev_test_qid))

    
    # Calcuates dev_test accuracy
    for ii in set(dev_test_qid):
        max_prob = 0
        final_guess = None
        for (prob, guess) in prediction_dict[(ii[0], ii[2])]:
            if prob > max_prob:
                max_prob = prob
                final_guess = guess
   
        if final_guess == ii[1]:
            right += 1
        else:
            print ii[0], ii[2]
            print "answer: ", ii[1], " ||  ", "guess: ", final_guess
            
    print("Accuracy on dev: %f" % (float(right) / float(total)))




    # Time for full training now
    # Prepares parameters for classifier
    X_full_train = [feat_list for feat_list, answer in full_train]
    Y_full_train = [answer for feat_list, answer in full_train]


    # Retrains on all data
    clf_ft = svm.SVC(kernel = 'linear', probability = True, verbose=True)

    clf_ft.fit(X_full_train, Y_full_train)


    
    # Reads in test data
    test_prediction_dict = defaultdict(list)
    test_qid_sposition = []

    test = DictReader(open("test_lsi.csv",'rU'))

    count = 0
    for ii in test:
        count += 1
        qid = ii['Question ID']
        qtext = ii['Question Text']


        sposition = ii['Sentence Position']
        qscores = ii['QANTA Scores']
        wscores = ii['IR_Wiki Scores']
        sscores = ii['Sim Scores']
        nscores = ii['Noun Scores']
        isguessp = ii['IsGuessP Scores']
        thisr = ii['ThisR Scores']
        thisc = ii['ThisC Scores']
        gender = ii ['Gender Scores']
        subject_group = ii['category']
        country = ii ['Country Scores']
        nvscores = ii['NV Scores']
    
        if subject_group == 'history':
            subject_group = 1.0
            
        if subject_group == 'lit':
            subject_group = 2.0
            
        if subject_group == 'science':
            subject_group = 3.0
            
        if subject_group == 'social':
            subject_group = 4.0

        prepare(qid, qtext, sposition, qscores, wscores, sscores, nscores, isguessp, thisr, thisc, gender, subject_group, nvscores, country, count)
    
    
    time_end = datetime.datetime.now()
    print "time taken is ", (time_end - time_start)
    print "Completed Test Processes"

    # Gets predicted probability of guess belonging to class '1.0'
    test_feat_dict = FeaturePreparation.test_feat_dict
    for item in test_feat_dict:
        for value in test_feat_dict[item]:
            test_prediction = clf_ft.predict_proba([value[0]])[0][1]
            test_prediction_dict[item].append((test_prediction, value[1]))

    # For each prediction gets the final guess
    test_prediction_finaldict = {}
    test_qid_sposition = set(FeaturePreparation.test_qid_sposition)
    for ii in set(test_qid_sposition):
        max_prob = 0
        final_guess = None
        for (prob, guess) in test_prediction_dict[ii]:
            if prob > max_prob:
                max_prob = prob
                final_guess = guess
        test_prediction_finaldict[ii[0]] = final_guess
        
    # Write predictions
    o = DictWriter(open('pred.csv', 'w'), ['Question ID', 'Answer'])
    o.writeheader()
    for ii in test_prediction_finaldict:
        o.writerow({'Question ID': ii, 'Answer': test_prediction_finaldict[ii]})
            

