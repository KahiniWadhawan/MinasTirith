''' Extracts features'''
from collections import defaultdict

class extractor:
    def __init__(self):
        None
    
    def features(self, guess, qtext, qscore, wscore, sposition, qscore_top_value, wscore_top_value, qscore_top_3value, qscore_top_5value, qscore_top_10value, wscore_top_3value, wscore_top_5value, wscore_top_10value, QANTA_score_top_set, IR_Wiki_score_top_set, Sim_score_top_set, sscore_top_value,sscore_top_3value ,sscore_top_5value ,sscore_top_10value, sscore, nscore_top_value, nscore_top_3value, nscore_top_5value, nscore, Noun_score_top_set, isguessp_score,  thisr_score, thisc_score, gender_score, subject_group,  nvscore_top_value, nvscore_top_3value ,nvscore_top_5value, nvscore, NV_score_top_set, country_match):
                    
        d = defaultdict(int)

        # Calculates whether in nvscore_top_set           
        if nvscore > NV_score_top_set:
            nvscore_top_set = 1
        else:
            nvscore_top_set = 0
            
	 # Calculates whether in nvscore top {1/3/5/10} values
        if nvscore == nvscore_top_value:
            nvscore_top = 1
            in_nvscore_top3 = 1
            in_nvscore_top5 = 1
            #in_nvscore_top10 = 1
        else:
            if nvscore >= nvscore_top_3value:
                nvscore_top = 0
                in_nvscore_top3 = 1
                in_nvscore_top5 = 1
                #in_nvscore_top10 = 1
            else:
                if nvscore >= nvscore_top_5value:
                    nvscore_top = 0
                    in_nvscore_top3 = 0
                    in_nvscore_top5 = 1
                    #in_nvscore_top10 = 1
                else:
                    nvscore_top = 0
                    in_nvscore_top3 = 0
                    in_nvscore_top5 = 0
                    #in_nvscore_top10 = 0



        # Calculates whether in nscore_top_set           
        if nscore > Noun_score_top_set:
            nscore_top_set = 1
        else:
            nscore_top_set = 0
            
	 # Calculates whether in nscore top {1/3/5/10} values
        if nscore == nscore_top_value:
            nscore_top = 1
            in_nscore_top3 = 1
            in_nscore_top5 = 1
            #in_nscore_top10 = 1
        else:
            if nscore >= nscore_top_3value:
                nscore_top = 0
                in_nscore_top3 = 1
                in_nscore_top5 = 1
                #in_nscore_top10 = 1
            else:
                if nscore >= nscore_top_5value:
                    nscore_top = 0
                    in_nscore_top3 = 0
                    in_nscore_top5 = 1
                    #in_nscore_top10 = 1
                else:
                    nscore_top = 0
                    in_nscore_top3 = 0
                    in_nscore_top5 = 0
                    #in_nscore_top10 = 0



        # Calculates whether in sscore_top_set           
        if sscore > Sim_score_top_set:
            sscore_top_set = 1
        else:
            sscore_top_set = 0


         # Calculates whether in sscore top {1/3/5/10} values
        if sscore == sscore_top_value:
            sscore_top = 1
            in_sscore_top3 = 1
            in_sscore_top5 = 1
            in_sscore_top10 = 1
        else:
            if sscore >= sscore_top_3value:
                sscore_top = 0
                in_sscore_top3 = 1
                in_sscore_top5 = 1
                in_sscore_top10 = 1
            else:
                if sscore >= sscore_top_5value:
                    sscore_top = 0
                    in_sscore_top3 = 0
                    in_sscore_top5 = 1
                    in_sscore_top10 = 1
                else:               
                    if sscore >= sscore_top_10value:
                        sscore_top = 0
                        in_sscore_top3 = 0
                        in_sscore_top5 = 0
                        in_sscore_top10 = 1
                    else:
                        sscore_top = 0
                        in_sscore_top3 = 0
                        in_sscore_top5 = 0
                        in_sscore_top10 = 0

        
        # Calculates whether in qscore_top_set           
        if qscore > QANTA_score_top_set:
            qscore_top_set = 1
        else:
            qscore_top_set = 0



        # Calculates whether in qscore top {1/3/5/10} values
        if qscore == qscore_top_value:
            qscore_top = 1
            in_qscore_top3 = 1
            in_qscore_top5 = 1
            in_qscore_top10 = 1
        else:
            if qscore >= qscore_top_3value:
                qscore_top = 0
                in_qscore_top3 = 1
                in_qscore_top5 = 1
                in_qscore_top10 = 1
            else:
                if qscore >= qscore_top_5value:
                    qscore_top = 0
                    in_qscore_top3 = 0
                    in_qscore_top5 = 1
                    in_qscore_top10 = 1
                else:               
                    if qscore >= qscore_top_10value:
                        qscore_top = 0
                        in_qscore_top3 = 0
                        in_qscore_top5 = 0
                        in_qscore_top10 = 1
                    else:
                        qscore_top = 0
                        in_qscore_top3 = 0
                        in_qscore_top5 = 0
                        in_qscore_top10 = 0


        
            
        # Calculates whether in wscore_top_set 
        if wscore > IR_Wiki_score_top_set:
            wscore_top_set = 1
        else:
            wscore_top_set = 0

            

        # calculating whether in wscore top {1/3/5/10} values           
        if wscore == wscore_top_value:
            wscore_top = 1
            in_wscore_top3 = 1
            in_wscore_top5 = 1
            in_wscore_top10 = 1
        else:
            if wscore >= wscore_top_3value:
                wscore_top = 0
                in_wscore_top3 = 1
                in_wscore_top5 = 1
                in_wscore_top10 = 1
            else:
                if wscore >= wscore_top_5value:
                    wscore_top = 0
                    in_wscore_top3 = 0
                    in_wscore_top5 = 1
                    in_wscore_top10 = 1
                else:
                    if wscore >= wscore_top_10value:
                        wscore_top = 0
                        in_wscore_top3 = 0
                        in_wscore_top5 = 0
                        in_wscore_top10 = 1
                    else:
                        wscore_top = 0
                        in_wscore_top3 = 0
                        in_wscore_top5 = 0
                        in_wscore_top10 = 0
            

        feat_vector = [qscore, qscore_top, qscore_top_set, in_qscore_top5,\
                       wscore, wscore_top, wscore_top_set, in_wscore_top3, in_wscore_top5,\
                       sscore, sscore_top, \
                       nscore, nscore_top_set,\
                       nvscore, nvscore_top_set,\
                       isguessp_score, thisr_score, thisc_score, gender_score,\
                       sposition, subject_group]

            
       
   
        return feat_vector
