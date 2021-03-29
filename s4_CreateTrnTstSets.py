"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Labgroup

Author : Christos Emmanouil

Thesis : Continuous implicit authentication of mobile phone users with a combination of navigation and behavior data.

CreateTrnTstSets : This script contains functions in order to create train and test sets.
"""

########################################
# Imports
########################################
import numpy as np
import pandas as pd
from random import randint


########################################
# Initialize Functions
########################################
#--------------------------------------------------
# SplitFDF_OrgAtt : Split the FDFs in Original User & Attackers Sets
# FDF - A Data Frame of features, must have the 'Output' column
# Original_User
#--------------------------------------------------
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
    FDF_Attackers['Output'] = 0
            
    return FDF_Original, FDF_Attackers            


#--------------------------------------------------
# SplitFDF_SyncedOrNot : Take Swipes, Acc & Gyr FDFs anf find those that happened in the same time
# FDF_Swipes - FDF of swipe, same to s3_CreateFeaturesDataFrames -> Create_FDF_Swipes output
# FDF_Acc - FDF of acc, same to s3_CreateFeaturesDataFrames -> Create_FDF_Sensors output
# FDF_Gyr - FDF of gyr, same to s3_CreateFeaturesDataFrames -> Create_FDF_Sensors output
#--------------------------------------------------
def SplitFDF_SyncedOrNot(FDF_Swipes, FDF_Acc, FDF_Gyr):
    
    FDF_Swipes_Synced = pd.DataFrame()
    FDF_Acc_Synced = pd.DataFrame()
    FDF_Gyr_Synced = pd.DataFrame()
    
    for Swipe_Index in range(len(FDF_Swipes)):
        Swipe_User = FDF_Swipes.loc[Swipe_Index]['User']
        Swipe_Screen = FDF_Swipes.loc[Swipe_Index]['Screen']
        Swipe_tStart = FDF_Swipes.loc[Swipe_Index]['Time_Start']
        Swipe_tStop = FDF_Swipes.loc[Swipe_Index]['Time_Stop']
        
        Acc_Index = FDF_Acc.loc[(FDF_Acc['User'] == Swipe_User) & (FDF_Acc['Screen'] == Swipe_Screen) & (FDF_Acc['TimeStamp'] >= Swipe_tStart) & (FDF_Acc['TimeStamp'] <= Swipe_tStop)].index
        if len(Acc_Index) > 1:
            raise ValueError('len(Acc_Index) > 1 : Something is wrong !!!')
        
        Gyr_Index = FDF_Gyr.loc[(FDF_Gyr['User'] == Swipe_User) & (FDF_Gyr['Screen'] == Swipe_Screen) & (FDF_Gyr['TimeStamp'] >= Swipe_tStart) & (FDF_Gyr['TimeStamp'] <= Swipe_tStop)].index
        if len(Gyr_Index) > 1:
            raise ValueError('len(Gyr_Index) > 1 : Something is wrong !!!')
            
        # If there are Acc & Gyr Data
        if ((len(Acc_Index) == 1) and (len(Gyr_Index) == 1)):
            Swipe = FDF_Swipes.loc[Swipe_Index]
            FDF_Swipes_Synced = FDF_Swipes_Synced.append(Swipe, ignore_index=True)
            FDF_Swipes = FDF_Swipes.drop(Swipe_Index)
            Acc = FDF_Acc.loc[Acc_Index]
            FDF_Acc_Synced = FDF_Acc_Synced.append(Acc, ignore_index=True)
            FDF_Acc = FDF_Acc.drop(Acc_Index)
            Gyr = FDF_Gyr.loc[Gyr_Index]
            FDF_Gyr_Synced = FDF_Gyr_Synced.append(Gyr, ignore_index=True)
            FDF_Gyr = FDF_Gyr.drop(Gyr_Index)
        
        # If there are only Acc Data
        if ((len(Acc_Index) == 1) and (len(Gyr_Index) == 0)):
            Swipe = FDF_Swipes.loc[Swipe_Index]
            FDF_Swipes_Synced = FDF_Swipes_Synced.append(Swipe, ignore_index=True)
            FDF_Swipes = FDF_Swipes.drop(Swipe_Index)
            Acc = FDF_Acc.loc[Acc_Index]
            FDF_Acc_Synced = FDF_Acc_Synced.append(Acc, ignore_index=True)
            FDF_Acc = FDF_Acc.drop(Acc_Index)
            FDF_Gyr_Synced = FDF_Gyr_Synced.append(pd.Series(), ignore_index=True)
        
        # If there are only Gyr Data
        if ((len(Acc_Index) == 0) and (len(Gyr_Index) == 1)):
            Swipe = FDF_Swipes.loc[Swipe_Index]
            FDF_Swipes_Synced = FDF_Swipes_Synced.append(Swipe, ignore_index=True)
            FDF_Swipes = FDF_Swipes.drop(Swipe_Index)
            Gyr = FDF_Gyr.loc[Gyr_Index]
            FDF_Gyr_Synced = FDF_Gyr_Synced.append(Gyr, ignore_index=True)
            FDF_Gyr = FDF_Gyr.drop(Gyr_Index)
            FDF_Acc_Synced = FDF_Acc_Synced.append(pd.Series(), ignore_index=True)
            
    FDF_Swipes = FDF_Swipes.reset_index(drop = True)
    FDF_Acc = FDF_Acc.reset_index(drop = True)
    FDF_Gyr = FDF_Gyr.reset_index(drop = True)
    
    FDFs_Unsynced = [FDF_Swipes, FDF_Acc, FDF_Gyr]
    FDFs_Synced = [FDF_Swipes_Synced, FDF_Acc_Synced, FDF_Gyr_Synced]
            
    return FDFs_Unsynced, FDFs_Synced
    

#--------------------------------------------------
# SplitRandom : Split a FDF in train & test set in a random way using the split rate
# FDF - A Data Frame of features
# Split_Rate - The percentage of entries that the test set must contain
#--------------------------------------------------
def SplitRandom(FDF, Split_Rate):
    
    Train = FDF
    Test = pd.DataFrame()
    
    Num_Test_Data = int(np.floor(len(Train) * Split_Rate))
    
    for i in range(Num_Test_Data):
        rnd = randint(0, len(Train) - 1)
        row = Train.loc[rnd]
        Test = Test.append(row, ignore_index = True)
        Train = Train.drop(rnd)
        Train = Train.reset_index(drop = True)
        
    return Train, Test


#--------------------------------------------------
# SplitFDF_TrnTst_UnSynced : Split swipes, acc & gyr FDFs in a random way
# FDFs_Org_UnSynced - A list contains [FDF_Swipes, FDF_Acc, FDF_Gyr]
# Split_Rate - The percentage of entries that the test set must contain
#--------------------------------------------------
def SplitFDF_TrnTst_UnSynced(FDFs_Org_UnSynced, Split_Rate):
    
    FDF_Swipes = FDFs_Org_UnSynced[0]
    FDF_Acc = FDFs_Org_UnSynced[1]
    FDF_Gyr = FDFs_Org_UnSynced[2]
    
    FDF_Swipes_Trn, FDF_Swipes_Tst = SplitRandom(FDF_Swipes, Split_Rate)
    FDF_Acc_Trn, FDF_Acc_Tst = SplitRandom(FDF_Acc, Split_Rate)
    FDF_Gyr_Trn, FDF_Gyr_Tst = SplitRandom(FDF_Gyr, Split_Rate)
    
    FDFs_Org_Trn = [FDF_Swipes_Trn, FDF_Acc_Trn, FDF_Gyr_Trn]
    FDFs_Org_Tst = [FDF_Swipes_Tst, FDF_Acc_Tst, FDF_Gyr_Tst]
    
    return FDFs_Org_Trn, FDFs_Org_Tst
    

#--------------------------------------------------
# SplitFDF_TrnTst_Synced : Split synced swipes, acc & gyr FDFs
# FDFs_Org_Synced - A list contains [FDF_Swipes, FDF_Acc, FDF_Gyr], the i row in FDF_Swipes in synced with the i row in FDF_Acc & FDF_Gyr
# Split_Rate - The percentage of entries that the test set must contain
#--------------------------------------------------
def SplitFDF_TrnTst_Synced(FDFs_Org_Synced, Split_Rate):
    
    FDF_Swipes_Trn = FDFs_Org_Synced[0]
    FDF_Acc_Trn = FDFs_Org_Synced[1]
    FDF_Gyr_Trn = FDFs_Org_Synced[2]
    
    FDF_Swipes_Tst = pd.DataFrame()
    FDF_Acc_Tst = pd.DataFrame()
    FDF_Gyr_Tst = pd.DataFrame()
    
    Num_Test_Data = int(np.floor(len(FDF_Swipes_Trn) * Split_Rate))
    
    for i in range(Num_Test_Data):
        rnd = randint(0, len(FDF_Swipes_Trn) - 1)
        swipe = FDF_Swipes_Trn.loc[rnd]
        acc = FDF_Acc_Trn.loc[rnd]
        gyr = FDF_Gyr_Trn.loc[rnd]
        FDF_Swipes_Tst = FDF_Swipes_Tst.append(swipe, ignore_index = True)
        FDF_Acc_Tst = FDF_Acc_Tst.append(acc, ignore_index = True)
        FDF_Gyr_Tst = FDF_Gyr_Tst.append(gyr, ignore_index = True)
        FDF_Swipes_Trn = FDF_Swipes_Trn.drop(rnd)
        FDF_Acc_Trn = FDF_Acc_Trn.drop(rnd)
        FDF_Gyr_Trn = FDF_Gyr_Trn.drop(rnd)
        FDF_Swipes_Trn = FDF_Swipes_Trn.reset_index(drop = True)
        FDF_Acc_Trn = FDF_Acc_Trn.reset_index(drop = True)
        FDF_Gyr_Trn = FDF_Gyr_Trn.reset_index(drop = True)
        
    FDFs_Org_Trn_Synced = [FDF_Swipes_Trn, FDF_Acc_Trn, FDF_Gyr_Trn]
    FDFs_Org_Tst_Synced = [FDF_Swipes_Tst, FDF_Acc_Tst, FDF_Gyr_Tst]
    
    return FDFs_Org_Trn_Synced, FDFs_Org_Tst_Synced
    
    
#--------------------------------------------------
# CreateTrnTst : Create Train & Test lists. Train - > [FDFs_Org_Trn, FDFs_Org_Trn_Syn], Test -> [FDFs_Org_Tst, FDFs_Org_Tst_Syn, FDFs_Att, FDFs_Att_Syn]
# FDF_Swipes - FDF of swipe, same to s3_CreateFeaturesDataFrames -> Create_FDF_Swipes output
# FDF_Acc - FDF of acc, same to s3_CreateFeaturesDataFrames -> Create_FDF_Sensors output
# FDF_Gyr - FDF of gyr, same to s3_CreateFeaturesDataFrames -> Create_FDF_Sensors output
# Original_User
# Split_Rate - The percentage of entries that the test set must contain
#--------------------------------------------------
def CreateTrnTst(FDF_Swipes, FDF_Acc, FDF_Gyr, Original_User, Split_Rate):
    
    FDF_Swipes_Org, FDF_Swipes_Att = SplitFDF_OrgAtt(FDF_Swipes, Original_User)
    FDF_Acc_Org, FDF_Acc_Att = SplitFDF_OrgAtt(FDF_Acc, Original_User)
    FDF_Gyr_Org, FDF_Gyr_Att = SplitFDF_OrgAtt(FDF_Gyr, Original_User)
    
    FDFs_Org, FDFs_Org_Syn = SplitFDF_SyncedOrNot(FDF_Swipes_Org, FDF_Acc_Org, FDF_Gyr_Org)
    FDFs_Att, FDFs_Att_Syn = SplitFDF_SyncedOrNot(FDF_Swipes_Att, FDF_Acc_Att, FDF_Gyr_Att) # All for testing
    
    FDFs_Org_Trn, FDFs_Org_Tst = SplitFDF_TrnTst_UnSynced(FDFs_Org, Split_Rate)
    FDFs_Org_Trn_Syn, FDFs_Org_Tst_Syn = SplitFDF_TrnTst_Synced(FDFs_Org_Syn, Split_Rate)
    
    FDFs_Trn = [FDFs_Org_Trn, FDFs_Org_Trn_Syn]
    FDFs_Tst = [FDFs_Org_Tst, FDFs_Org_Tst_Syn, FDFs_Att, FDFs_Att_Syn]
    
    return FDFs_Trn, FDFs_Tst