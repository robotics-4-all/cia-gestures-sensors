"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Labgroup

Author : Christos Emmanouil

Thesis : Continuous implicit authentication of mobile phone users with a combination of navigation and behavior data.

s4_Funcs_CreateSets : This script contains functions in order split the dataset in original user's or atteckers, synced or not and train or test sets.
"""

#################
#    IMPORTS    #
#################
import numpy as np
import pandas as pd
from random import randint


##############################
#    INITIALIZE FUNCTIONS    #
##############################
# ==================================================================
# SplitDFF_OrgAtt : Split the DFFs in Original User & Attackers Sets
# DFF - A Data Frame of features, must have the 'Output' column
# Original_User
# ==================================================================
def SplitDFF_OrgAtt(DFF, Original_User):
    
    DFF_Original = pd.DataFrame()
    DFF_Attackers = pd.DataFrame()
    
    for i in range(len(DFF)):
        row = DFF.loc[i]
        if (row['User'] == Original_User):
            DFF_Original = DFF_Original.append(row, ignore_index = True)
        else:
            DFF_Attackers = DFF_Attackers.append(row, ignore_index = True)
            
    DFF_Original['Output'] = 1
    DFF_Attackers['Output'] = -1
            
    return DFF_Original, DFF_Attackers            
    

# ==================================================================================
# SplitRandom : Split a DFF in train & test set in a random way using the split rate
# DFF - A Data Frame of features
# Split_Rate - The percentage of entries that the test set must contain
# ==================================================================================
def SplitRandom(DFF, Split_Rate):
    
    Trn = DFF
    Tst = pd.DataFrame()
    
    Num_Test_Data = int(np.floor(len(Trn) * Split_Rate))
    
    for i in range(Num_Test_Data):
        rnd = randint(0, len(Trn) - 1)
        row = Trn.loc[rnd]
        Tst = Tst.append(row, ignore_index = True)
        Trn = Trn.drop(rnd)
        Trn = Trn.reset_index(drop = True)
        
    return Trn, Tst


# =====================================================================
# SplitRandom_Synced :
# FDF_1, FDF_2: Must have synced data !!!!
# Split_Rate - The percentage of entries that the test set must contain
# =====================================================================
def SplitRandom_Synced(FDF_1, FDF_2, Split_Rate):
    
    Trn_1 = FDF_1
    Tst_1 = pd.DataFrame()
    Trn_2 = FDF_2
    Tst_2 = pd.DataFrame()
    
    Num_Test_Data = int(np.floor(len(Trn_1) * Split_Rate))
    
    for i in range(Num_Test_Data):
        rnd = randint(0, len(Trn_1) - 1)
        row_1 = Trn_1.loc[rnd]
        row_2 = Trn_2.loc[rnd]
        Tst_1 = Tst_1.append(row_1, ignore_index = True)
        Tst_2 = Tst_2.append(row_2, ignore_index = True)
        Trn_1 = Trn_1.drop(rnd)
        Trn_2 = Trn_2.drop(rnd)
        Trn_1 = Trn_1.reset_index(drop = True)
        Trn_2 = Trn_2.reset_index(drop = True)
        
    return Trn_1, Tst_1, Trn_2, Tst_2