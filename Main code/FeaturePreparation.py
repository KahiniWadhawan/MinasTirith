''' Prepares Features by calling Feature Extractor'''

import threading, Queue, time, re, nltk, numpy, datetime, sys
from FeatureExtractor import extractor
from collections import defaultdict


fe = extractor()
dev_train = []
dev_test_qid = []
dev_test = []
full_train = []
test_feat_dict = defaultdict(list)
test_qid_sposition = []


def prepare(qid, qtext, sposition, qscores, wscores, sscores, nscores, isguessp, thisr, thisc, gender, subject_group, nvscores, country, count, *var_answer):
        
    qtext = qtext
    qid = qid
    sposition = sposition
    qscores = qscores
    wscores = wscores
    sscores = sscores
    nscores = nscores
    nvscores = nvscores
    isguessp = isguessp
    thisr = thisr
    thisc = thisc
    gender = gender
    country = country
    subject_group = subject_group

    
    QANTA_Scores = {}
    IR_Wiki_Scores = {}
    Sim_Scores = {}
    Noun_Scores = {}
    NV_Scores = {}
    isguessp_scores = {}
    thisr_scores = {}
    thisc_scores = {}
    gender_scores = {}
    country_scores = {}


    # Normalized dicts
    QANTA_Scores_Normalized = {}
    IR_Wiki_Scores_Normalized = {}
    Sim_Scores_Normalized = {}
    Noun_Scores_Normalized = {}
    NV_Scores_Normalized = {}

    QANTA_Scores_Double_Normalized = {}
    IR_Wiki_Scores_Double_Normalized = {}
    Sim_Scores_Double_Normalized = {}
    Noun_Scores_Double_Normalized = {}
    NV_Scores_Double_Normalized = {}
    
    answer = None
    for item in var_answer:
        answer = item
        
    # Creates Gender score dictionary 
    gender_Score_split = re.split(',[^_]', gender)
    
    for item in gender_Score_split:
        gender_scores[item.split(':')[0].strip()] = float(item.split(':')[1])

    # Creates Country score dictionary 
    country_Score_split = re.split(',[^_]', country)
   
    for item in country_Score_split:
        country_scores[item.split(':')[0].strip()] = float(item.split(':')[1])


    # Creates ThisR score dictionary 
    thisr_Score_split = re.split(',[^_]', thisr)
    
    for item in thisr_Score_split:
        thisr_scores[item.split(':')[0].strip()] = float(item.split(':')[1])

    # Creates ThisC score dictionary 
    thisc_Score_split = re.split(',[^_]', thisc)
    
    for item in thisc_Score_split:
        thisc_scores[item.split(':')[0].strip()] = float(item.split(':')[1])
 

    # Creates IsGuessP score dictionary 
    isguessp_Score_split = re.split(',[^_]', isguessp)
    
    for item in isguessp_Score_split:
        isguessp_scores[item.split(':')[0].strip()] = float(item.split(':')[1])




    # Creates Noun score related paramters
    # Creates Noun score dictionary 
    Noun_Score_split = re.split(',[^_]', nscores)
    
    for item in Noun_Score_split:
        Noun_Scores[item.split(':')[0].strip()] = float(item.split(':')[1])

    # Normalizes Noun scores
    for item in Noun_Scores:
        if (max(Noun_Scores.values()) - min(Noun_Scores.values())) != 0:
            Noun_Scores_Normalized[item] = (Noun_Scores[item] - min(Noun_Scores.values()))/(max(Noun_Scores.values()) - min(Noun_Scores.values()))
        else:
            Noun_Scores_Normalized[item] = (Noun_Scores[item] - min(Noun_Scores.values()))/ 0.001
    Noun_Scores = Noun_Scores_Normalized

    # Sorts nscores
    nscores_sorted_list = sorted(Noun_Scores.items(), key = lambda t: t[1], reverse = True)
 	
    # Calculates nscore top values
    try:
        nscore_top_value = max(Noun_Scores.values())
    except:
        nscore_top_value = 0.0000001
    try:
        nscore_top_3value = nscores_sorted_list[2][1]
    except:
        nscore_top_3value = min(Noun_Scores.values())
        
    try:
        nscore_top_5value = nscores_sorted_list[4][1]
    except:
        nscore_top_5value = min(Noun_Scores.values())


    # Calculating Nscore top set: divide dist bet top value and median into len(score dict)/2 spaces. values in top space will fall into topset 
    Noun_Scores_median = numpy.median(Noun_Scores.values())
    Noun_score_top_set = (nscore_top_value - Noun_Scores_median)/(len(Noun_Scores)/2)





    # Creates NV score related paramters
    # Creates NV score dictionary 
    NV_Score_split = re.split(',[^_]', nvscores)
    
    for item in Noun_Score_split:
        NV_Scores[item.split(':')[0].strip()] = float(item.split(':')[1])


    # Normalizes NV Scores
    for item in NV_Scores:
        if (max(NV_Scores.values()) - min(NV_Scores.values())) != 0:
            NV_Scores_Normalized[item] = (NV_Scores[item] - min(NV_Scores.values()))/(max(NV_Scores.values()) - min(NV_Scores.values()))
        else:
            NV_Scores_Normalized[item] = (NV_Scores[item] - min(NV_Scores.values()))/ 0.001
    NV_Scores = NV_Scores_Normalized

    # Sorts nvscores
    nvscores_sorted_list = sorted(NV_Scores.items(), key = lambda t: t[1], reverse = True)
 	
    # Calculates nvscore top values
    try:
        nvscore_top_value = max(NV_Scores.values())
    except:
        nvscore_top_value = 0.0000001
        
    try:
        nvscore_top_3value = nvscores_sorted_list[2][1]
    except:
        nvscore_top_3value = min(NV_Scores.values())
        
    try:
        nvscore_top_5value = nvscores_sorted_list[4][1]
    except:
        nvscore_top_5value = min(NV_Scores.values())
        

    # Calculating NVscore top set: divide dist bet top value and median into len(score dict)/2 spaces. values in top space will fall into topset 
    NV_Scores_median = numpy.median(NV_Scores.values())
    NV_score_top_set = (nvscore_top_value - NV_Scores_median)/(len(NV_Scores)/2)





    # Creates Sim score related paramters # LSI and Sim scores are just different names to the same score
    # Creates Sim score dictionary 
    Sim_Score_split = re.split(',[^_]', sscores)
    
    for item in Sim_Score_split:
        Sim_Scores[item.split(':')[0].strip()] = float(item.split(':')[1])

    # Normalizes Sim Scores
    for item in Sim_Scores:
        if (max(Sim_Scores.values()) - min(Sim_Scores.values())) != 0:
            Sim_Scores_Normalized[item] = (Sim_Scores[item] - min(Sim_Scores.values()))/(max(Sim_Scores.values()) - min(Sim_Scores.values()))
        else:
            Sim_Scores_Normalized[item] = (Sim_Scores[item] - min(Sim_Scores.values()))/0.001
    Sim_Scores = Sim_Scores_Normalized

    
    # Sorts sscores
    sscores_sorted_list = sorted(Sim_Scores.items(), key = lambda t: t[1], reverse = True)
  	

    # Calculates sscore top values
    sscore_top_value = max(Sim_Scores.values())
    sscore_top_3value = sscores_sorted_list[2][1]
    sscore_top_5value = sscores_sorted_list[4][1]
    sscore_top_10value = sscores_sorted_list[9][1]

    # Calculating Sscore top set: divide dist bet top value and median into len(score dict)/2 spaces. values in top space will fall into topset 
    Sim_Scores_median = numpy.median(Sim_Scores.values())
    Sim_score_top_set = (sscore_top_value - Sim_Scores_median)/(len(Sim_Scores)/2)



    
    # Creates QANTA score related paramters
    # Creates QANTA Score dictionary
    QANTA_Score_split = re.split(',[^_]', qscores)
    
    for item in QANTA_Score_split:
        QANTA_Scores[item.split(':')[0].strip()] = float(item.split(':')[1])

    # Normalizes QANTA Scores
    for item in QANTA_Scores:
        if (max(QANTA_Scores.values()) - min(QANTA_Scores.values())) != 0:
            QANTA_Scores_Normalized[item] = (QANTA_Scores[item] - min(QANTA_Scores.values()))/(max(QANTA_Scores.values()) - min(QANTA_Scores.values()))
        else:
            QANTA_Scores_Normalized[item] = (QANTA_Scores[item] - min(QANTA_Scores.values()))/ 0.001
    QANTA_Scores = QANTA_Scores_Normalized


    # Sorts Qscores
    qscores_sorted_list = sorted(QANTA_Scores.items(), key = lambda t: t[1], reverse = True)


    # Calculates Qscore top values
    qscore_top_value = max(QANTA_Scores.values())
    qscore_top_3value = qscores_sorted_list[2][1]
    qscore_top_5value = qscores_sorted_list[4][1]
    qscore_top_10value = qscores_sorted_list[9][1]

    # Calculating Qscore top set: divide dist bet top value and median into len(score dict)/2 spaces. values in top space will fall into topset 
    QANTA_Scores_median = numpy.median(QANTA_Scores.values())
    QANTA_score_top_set = (qscore_top_value - QANTA_Scores_median)/(len(QANTA_Scores)/2)




    # Creates IRWiki score related paramters        
    # Creates IRWiki Score dictionary
    IR_Wiki_Score_split = re.split(',[^_]', wscores)
    for item in IR_Wiki_Score_split:
        IR_Wiki_Scores[item.split(':')[0].strip()] = float(item.split(':')[1])


    # Normalized
    for item in IR_Wiki_Scores:
        if (max(IR_Wiki_Scores.values()) - min(IR_Wiki_Scores.values())) != 0:
            IR_Wiki_Scores_Normalized[item] = (IR_Wiki_Scores[item] - min(IR_Wiki_Scores.values()))/(max(IR_Wiki_Scores.values()) - min(IR_Wiki_Scores.values()))
        else:
            IR_Wiki_Scores_Normalized[item] = (IR_Wiki_Scores[item] - min(IR_Wiki_Scores.values()))/ 0.001
    IR_Wiki_Scores = IR_Wiki_Scores_Normalized

       
    # Wscores values sorted
    wscores_sorted_list = sorted(IR_Wiki_Scores.items(), key = lambda t: t[1], reverse = True)

    # Calculating Wscore top values
    wscore_top_value = max(IR_Wiki_Scores.values())
    wscore_top_3value = wscores_sorted_list[2][1]
    wscore_top_5value = wscores_sorted_list[4][1]
    wscore_top_10value= wscores_sorted_list[9][1]
    
    # Calculating Wscore top set: divide dist bet top value and median into len(score dict)/2 spaces. values in top space will fall into topset 
    IR_Wiki_Scores_median = numpy.median(QANTA_Scores.values())
    IR_Wiki_score_top_set = (qscore_top_value - QANTA_Scores_median)/(len(QANTA_Scores)/2)


    
    # Creates parameters for Feature creation
    # For guesses present in Qscore, do this
    for item in QANTA_Scores:
        guess = item

        # Assigns answer category
        if answer != None:
            if guess == answer:
                category = 1
            else:
                category = 0


        qscore = QANTA_Scores[item]
        isguessp_score = isguessp_scores[item]
        thisr_score = thisr_scores[item]
        thisc_score = thisc_scores[item]
        gender_score = gender_scores[item]
        country_match = country_scores[item]
        

        # Gets wscore and removes guess from dictionary
        if IR_Wiki_Scores.has_key(item):
            wscore = IR_Wiki_Scores[item]
            del IR_Wiki_Scores[item]
        else:
            wscore = 0

	# Gets sscore and removes guess from dictionary
        if Sim_Scores.has_key(item):
            sscore = Sim_Scores[item]
            del Sim_Scores[item]
        else:
            sscore = 0
	
	# Gets nscore and removes guess from dictionary
        if Noun_Scores.has_key(item):
            nscore = Noun_Scores[item]
            del Noun_Scores[item]
        else:
            nscore = 0

        # Gets nvscore and removes guess from dictionary
        if NV_Scores.has_key(item):
            nvscore = NV_Scores[item]
            del NV_Scores[item]
        else:
            nvscore = 0

        # Creates feature vector
        feat = fe.features(guess, qtext, qscore, wscore, sposition, qscore_top_value, wscore_top_value, qscore_top_3value, qscore_top_5value, qscore_top_10value, wscore_top_3value, wscore_top_5value, wscore_top_10value, QANTA_score_top_set, IR_Wiki_score_top_set, Sim_score_top_set, sscore_top_value, sscore_top_3value ,sscore_top_5value ,sscore_top_10value, sscore, nscore_top_value, nscore_top_3value ,nscore_top_5value, nscore, Noun_score_top_set, isguessp_score, thisr_score, thisc_score, gender_score, subject_group, nvscore_top_value, nvscore_top_3value ,nvscore_top_5value, nvscore, NV_score_top_set, country_match)

        # Adds features into dev_test/ dev_train/ test_feat_dict
        if answer != None:
            if count % 5 == 0:
                dev_test_qid.append((qid, answer, sposition))
                dev_test.append((guess, qid, sposition, feat, category))
            else:
                dev_train.append((feat, category))

            full_train.append((feat, category))
        else:
            test_qid_sposition.append((qid, sposition))
            test_feat_dict[(qid, sposition)].append((feat, guess))
        

    # For guesses present in Wscore but not in Qscore
    for item in IR_Wiki_Scores:
        guess = item

        # Assigns answer category
        if answer != None:
            if guess == answer:
                category = 1
            else:
                category = 0

    
        wscore = IR_Wiki_Scores[item]
        qscore = 0
        isguessp_score = isguessp_scores[item]
        thisr_score = thisr_scores[item]
        thisc_score = thisc_scores[item]
        gender_score = gender_scores[item]
        country_match = country_scores[item]

	# Gets sscore and removes guess from dictionary
        if Sim_Scores.has_key(item):
            sscore = Sim_Scores[item]
            del Sim_Scores[item]
        else:
            sscore = 0

	# Gets nscore and removes guess from dictionary
        if Noun_Scores.has_key(item):
            nscore = Noun_Scores[item]
            del Noun_Scores[item]
        else:
            nscore = 0

        # Gets nvcore and removes guess from dictionary
        if NV_Scores.has_key(item):
            nvscore = NV_Scores[item]
            del NV_Scores[item]
        else:
            nvscore = 0

        
        # Creates feature vector
        feat = fe.features(guess, qtext, qscore, wscore, sposition, qscore_top_value, wscore_top_value, qscore_top_3value, qscore_top_5value, qscore_top_10value,  wscore_top_3value, wscore_top_5value, wscore_top_10value, QANTA_score_top_set, IR_Wiki_score_top_set, Sim_score_top_set, sscore_top_value,sscore_top_3value ,sscore_top_5value ,sscore_top_10value, sscore, nscore_top_value,nscore_top_3value ,nscore_top_5value , nscore, Noun_score_top_set, isguessp_score, thisr_score, thisc_score, gender_score, subject_group, nvscore_top_value, nvscore_top_3value ,nvscore_top_5value, nvscore, NV_score_top_set, country_match )

        # Add features into dev_test/ dev_train / test_feat_dict
        if answer != None:
            if count % 5 == 0:
                dev_test_qid.append((qid, answer, sposition))
                dev_test.append((guess, qid, sposition, feat, category))
            else:
                dev_train.append((feat, category))

            full_train.append((feat, category))
        else:
            test_qid_sposition.append((qid, sposition))
            test_feat_dict[(qid, sposition)].append((feat, guess))
