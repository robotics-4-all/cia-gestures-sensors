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
# SplitFDF_OrgAtt : Split the FDFs in Original User & Attackers Sets
# FDF - A Data Frame of features, must have the 'Output' column
# Original_User
# ==================================================================
def SplitFDF_OrgAtt(FDF, Original_User):
    
    FDF_Original = pd.DataFrame()
    FDF_Attackers = pd.DataFrame()
    
    for i in range(len(FDF)):
        row = FDF.loc[i]
        if (row['User'] == Original_User):
            FDF_Original = FDF_Original.append(row, ignore_index = True)
        else:
            FDF_Attackers = FDF_Attackers.append(row, ignore_index = True)
            
    FDF_Original['Output'] = 1
    FDF_Attackers['Output'] = -1
            
    return FDF_Original, FDF_Attackers            
    

# ==================================================================================
# SplitRandom : Split a FDF in train & test set in a random way using the split rate
# FDF - A Data Frame of features
# Split_Rate - The percentage of entries that the test set must contain
# ==================================================================================
def SplitRandom(FDF, Split_Rate):
    
    Trn = FDF
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
        Trn_2 = Trn_1.reset_index(drop = True)
        
    return Trn_1, Tst_1, Trn_2, Tst_2
    
    
# ==========================================================================================
# CreateFinalSets : Create Original User & Attackers Sets
# FDF_Swipes - FDF of swipe, same to s3_CreateFeaturesDataFrames -> Create_FDF_Swipes output
# FDF_Acc - FDF of acc, same to s3_CreateFeaturesDataFrames -> Create_FDF_Sensors output
# FDF_Gyr - FDF of gyr, same to s3_CreateFeaturesDataFrames -> Create_FDF_Sensors output
# Original_User
# Split_Rate - The percentage of entries that the test set must contain
# ==========================================================================================
def CreateFinalSets(FDF_Swipes, FDF_Acc, FDF_Gyr, Original_User, Synced_Sensors, Split_Rate):
    
    FDF_Org_Swipes, FDF_Att_Swipes = SplitFDF_OrgAtt(FDF_Swipes, Original_User)
    FDF_Org_Acc, FDF_Att_Acc = SplitFDF_OrgAtt(FDF_Acc, Original_User)
    FDF_Org_Gyr, FDF_Att_Gyr = SplitFDF_OrgAtt(FDF_Gyr, Original_User)
    
    FDF_Org_Swipes_Trn, FDF_Org_Swipes_Tst = SplitRandom(FDF_Org_Swipes, Split_Rate)
    
    if Synced_Sensors:
        FDF_Org_Acc_Trn, FDF_Org_Acc_Tst = SplitRandom(FDF_Org_Acc, Split_Rate)
        FDF_Org_Gyr_Trn, FDF_Org_Gyr_Tst = SplitRandom(FDF_Org_Gyr, Split_Rate)
    else:
        FDF_Org_Acc_Trn, FDF_Org_Acc_Tst, FDF_Org_Gyr_Trn, FDF_Org_Gyr_Tst = SplitRandom_Synced(FDF_Org_Acc, FDF_Org_Gyr, Split_Rate)
        
    FDFs_Org_Trn = [FDF_Org_Swipes_Trn, FDF_Org_Acc_Trn, FDF_Org_Gyr_Trn]
    FDFs_Org_Tst = [FDF_Org_Swipes_Tst, FDF_Org_Acc_Tst, FDF_Org_Gyr_Tst]
    
    FDFs_Original = [FDFs_Org_Trn, FDFs_Org_Tst]
    FDFs_Attackers = [FDF_Att_Swipes, FDF_Att_Acc, FDF_Att_Gyr]
    
    return FDFs_Original, FDFs_Attackers