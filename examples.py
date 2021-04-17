###############
#--- Notes ---#
###############
## After expiriments was found that : 
## 1. There are not enought users with synced Sensors & Gestures data neither in Mathisis nor in Focus.
## 2. There is only one user in Mathisis and in Focus that has only gyr and acc data respectively, synced with swipes with out having acc and gyr data respectively at the same time.
## So there are 2 options :
## 1. Use totaly unsyned data
## 2. Use synced sensors and unsynced swipes.


#################
#    IMPORTS    #
#################
import numpy as np
import pandas as pd
from tqdm import tqdm
from texttable import Texttable

from s1_Funcs_ExploreData import findUsers_Sensors, findUsers_Swipes, findUsers_Common
from s2_Funcs_CreateDataFrames import Create_DF_Sensors, Create_DF_Gestures
from s3_Funcs_ExtractFeatures import Create_DFF_Sensors, Create_DFF_Swipes
from s5_Funcs_HandleClassifiers import RunML, AppendUserMetrics, CalculateMeanMetrics
from s5_Class_EvaluationMetrics import EvaluationMetrics


############################
#    GENERAL PARAMETERS    #
############################
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
ScreenName = 'Mathisis'
saveDir = '__Saves__\\' + ScreenName + '_Exp_002'


########################
#    EXPLORING DATA    #
########################
# Find all users with valid senros data (synced or not)
# -----------------------------------------------------
Synced_Sensors = True
minData_Screen = 300
minData_TimeStamp = 1
minData_User = 1
valUsers_Sensors, _ = findUsers_Sensors(SensData_Path, ScreenName, Synced_Sensors, minData_Screen, minData_TimeStamp, minData_User)

# Find all users with valid swipes
# --------------------------------
maxDeviceWidth = 600
maxDeviceHeight = 1000
Fake_Swipe_Limit = 30
minData_Gesture = 4
maxData_Gesture = 10
minGesture_User = 1
valUsers_Swipes = findUsers_Swipes(GestData_DBName, ScreenName, maxDeviceWidth, maxDeviceHeight, Fake_Swipe_Limit, minData_Gesture, maxData_Gesture, minGesture_User)

# Find all users with valid sensros data (synced or not) and swipes
# -----------------------------------------------------------------
Synced_Sensors_Gestures = False
minSensData = 3000
maxSensData = 30000
minGest = 10
maxGest = float('inf')
DF_Users_All, _ = findUsers_Common(valUsers_Sensors, valUsers_Swipes, Synced_Sensors_Gestures, minSensData, maxSensData, minGest, maxGest)

"""
# Load from pickles
# -----------------
valUsers_Sensors = pd.read_pickle(saveDir + '\\' + 'valUsers_Sensors.pkl')
valUsers_Swipes = pd.read_pickle(saveDir + '\\' + 'valUsers_Swipes.pkl')
DF_Users_All = pd.read_pickle(saveDir + '\\' + 'DF_Users_All.pkl')

# Save to pickles
# ---------------
valUsers_Sensors.to_pickle(saveDir + '\\' + 'valUsers_Sensors.pkl')
valUsers_Swipes.to_pickle(saveDir + '\\' + 'valUsers_Swipes.pkl')
DF_Users_All.to_pickle(saveDir + '\\' + 'DF_Users_All.pkl')
"""


#########################
#    SELECTING USERS    #
#########################    
# Select a number of users
# ------------------------
Number_Of_Users = 5
if (Number_Of_Users > len(DF_Users_All)):
    raise ValueError('Not so many users : num_of_users > len(DF_Users)')

DF_Users_Final = DF_Users_All.sample(n = Number_Of_Users, replace = False)

"""
# Load from pickles
#------------------
DF_Users_Final = pd.read_pickle(saveDir + '\\' + 'DF_Users_Final.pkl')

# Save to pickles
#----------------
DF_Users_Final.to_pickle(saveDir + '\\' + 'DF_Users_Final.pkl')
"""


#############################
#    CREATING DATAFRAMES    #
#############################
# Creating Dataframes
# -------------------
DF_Acc, DF_Gyr = Create_DF_Sensors(SensData_Path, DF_Users_Final)
DF_Gest = Create_DF_Gestures(GestData_DBName, DF_Users_Final)

"""
# Load from pickles
# -----------------
DF_Acc = pd.read_pickle(saveDir + '\\' + 'DF_Acc.pkl')
DF_Gyr = pd.read_pickle(saveDir + '\\' + 'DF_Gyr.pkl')
DF_Gest = pd.read_pickle(saveDir + '\\' + 'DF_Gest.pkl')

# Save to pickles
# ---------------
DF_Acc.to_pickle(saveDir + '\\' + 'DF_Acc.pkl')
DF_Gyr.to_pickle(saveDir + '\\' + 'DF_Gyr.pkl')
DF_Gest.to_pickle(saveDir + '\\' + 'DF_Gest.pkl')
""" 


#############################
#    EXTRACTING FEATURES    #
#############################
import sys
orig_stdout = sys.stdout
f = open(saveDir + '\\__Results3__.txt', 'w')
sys.stdout = f

mat_Swipes = np.array([[1111, 2222, 3333, 4444, 5555, 6666]])
mat_Acc = np.array([[1111, 2222, 3333, 4444, 5555, 6666]])
mat_Gyr = np.array([[1111, 2222, 3333, 4444, 5555, 6666]])
mat_Sensors = np.array([[1111, 2222, 3333, 4444, 5555, 6666]])

#Window = 200
#Overlap = 0.9

Windows = [150]
Overlaps = [0.9]
for Window in tqdm(Windows, desc = '-> Window'):
    for Overlap in tqdm(Overlaps, desc = '-> Overlap'):

        # Extracting sensors data features
        # --------------------------------
        Sensors_Feature = 'Magnitude'
        Synced_Sensors = True
        DFF_Acc, DFF_Gyr = Create_DFF_Sensors(DF_Users_Final, DF_Acc, DF_Gyr, Sensors_Feature, Synced_Sensors, Window, Overlap)
        
        # Extracting swipes features
        # --------------------------
        Normalize_Swipes = True
        DFF_Swipes = Create_DFF_Swipes(DF_Gest, Normalize_Swipes)
                
        """
        # Load from pickles
        # -----------------
        DFF_Acc = pd.read_pickle(saveDir + '\\' + 'DFF_Acc.pkl')
        DFF_Gyr = pd.read_pickle(saveDir + '\\' + 'DFF_Gyr.pkl')
        DFF_Swipes = pd.read_pickle(saveDir + '\\' + 'DFF_Swipes.pkl')
        
        # Save to pickles
        # ---------------
        DFF_Acc.to_pickle(saveDir + '\\' + 'DFF_Acc.pkl')
        DFF_Gyr.to_pickle(saveDir + '\\' + 'DFF_Gyr.pkl')
        DFF_Swipes.to_pickle(saveDir + '\\' + 'DFF_Swipes.pkl')
        """
        
        
        ##############################
        #    COREELATION MATRICES    #
        ##############################
        #corrMatrix_Swipes = DFF_Swipes.corr()
        #corrMatrix_Acc = DFF_Acc.corr()
        #corrMatrix_Gyr = DFF_Gyr.corr()       
        
        # Final_Features_Swipes = ['Duration', 'Trace_Length_Horizontal', 'Trace_Length_Vertical', 'Slope', 'Mean_Square_Error', 'Mean_Abs_Error', 'Median_Abs_Error', 'Coef_Determination', 'Mean_X', 'Mean_Y', 'Acceleration_Horizontal', 'Acceleration_Vertical']
        Final_Features_Swipes = ['Trace_Length_Horizontal', 'Trace_Length_Vertical', 'Slope', 'Mean_Square_Error', 'Mean_Abs_Error', 'Median_Abs_Error', 'Coef_Determination', 'Mean_Y', 'Acceleration_Horizontal', 'Acceleration_Vertical']
        
        # Final_Features_Sensors = ['Mean', 'STD', 'Max', 'Min', 'Range', 'Percentile25', 'Percentile50', 'Percentile75', 'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2', 'MeanFrequency']
        Final_Features_Sensors = ['Mean', 'STD', 'Max', 'Min', 'Percentile25', 'Percentile50', 'Percentile75', 'Kurtosis', 'Skewness', 'Amplitude1', 'Amplitude2', 'Frequency2', 'MeanFrequency']
        
              
        #####################
        #    CLASSIFIERS    #
        #####################
        Split_Rate = 0.2
        Folds = 10
        
        EvaluationMetrics_Swipes_All = EvaluationMetrics()
        EvaluationMetrics_Acc_All = EvaluationMetrics()
        EvaluationMetrics_Gyr_All = EvaluationMetrics()
        EvaluationMetrics_Sensors_All = EvaluationMetrics()
        
        for i in tqdm(range(len(DF_Users_Final)), desc = '-> User'):
            
            OriginalUser = DF_Users_Final['User'].values[i]   
            EvaluationMetrics_Swipes_User, EvaluationMetrics_Acc_User, EvaluationMetrics_Gyr_User, EvaluationMetrics_Sensors_User = RunML(OriginalUser, DFF_Swipes, DFF_Acc, DFF_Gyr, Final_Features_Swipes, Final_Features_Sensors, Split_Rate, Folds)
        
            EvaluationMetrics_Swipes_All = AppendUserMetrics(EvaluationMetrics_Swipes_User, EvaluationMetrics_Swipes_All)
            EvaluationMetrics_Acc_All = AppendUserMetrics(EvaluationMetrics_Acc_User, EvaluationMetrics_Acc_All)
            EvaluationMetrics_Gyr_All = AppendUserMetrics(EvaluationMetrics_Gyr_User, EvaluationMetrics_Gyr_All)
            EvaluationMetrics_Sensors_All = AppendUserMetrics(EvaluationMetrics_Sensors_User, EvaluationMetrics_Sensors_All)
        
        
        #################
        #    RESULTS    #
        #################
        # Calculating Average Metrics
        # ---------------------------
        EvaluationMetrics_Swipes_Avg = EvaluationMetrics()
        EvaluationMetrics_Swipes_Avg = CalculateMeanMetrics(EvaluationMetrics_Swipes_All, EvaluationMetrics_Swipes_Avg)
        EvaluationMetrics_Acc_Avg = EvaluationMetrics()
        EvaluationMetrics_Acc_Avg = CalculateMeanMetrics(EvaluationMetrics_Acc_All, EvaluationMetrics_Acc_Avg)
        EvaluationMetrics_Gyr_Avg = EvaluationMetrics()
        EvaluationMetrics_Gyr_Avg = CalculateMeanMetrics(EvaluationMetrics_Gyr_All, EvaluationMetrics_Gyr_Avg)
        EvaluationMetrics_Sensors_Avg = EvaluationMetrics()
        EvaluationMetrics_Sensors_Avg = CalculateMeanMetrics(EvaluationMetrics_Sensors_All, EvaluationMetrics_Sensors_Avg)
            
        # Print Average Stats
        # -------------------
        pre = 3
        SumaryTable = Texttable()
        SumaryTable.header([ScreenName + '\n' + str(len(DF_Users_Final)) + ' Users' + '\n' + str(Split_Rate) + ' Split' + '\n' + str(Folds) + ' Folds', 'TrnSize', 'TstSize', 'Mean Accuracy', 'Mean F1Score', 'Mean FAR', 'Mean FRR'])
        SumaryTable.set_cols_align(['c','c', 'c', 'c', 'c', 'c', 'c'])
        SumaryTable.set_cols_valign(['m','m', 'm', 'm', 'm', 'm', 'm'])
        SumaryTable.add_row(['Swipes', EvaluationMetrics_Swipes_Avg.getTrnSize()[0], EvaluationMetrics_Swipes_Avg.getTstSize()[0], str(round(EvaluationMetrics_Swipes_Avg.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Swipes_Avg.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Swipes_Avg.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Swipes_Avg.getFRR()[0]*100,pre))+' %'])
        SumaryTable.add_row(['Acc', EvaluationMetrics_Acc_Avg.getTrnSize()[0], EvaluationMetrics_Acc_Avg.getTstSize()[0], str(round(EvaluationMetrics_Acc_Avg.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Acc_Avg.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Acc_Avg.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Acc_Avg.getFRR()[0]*100,pre))+' %'])
        SumaryTable.add_row(['Gyr', EvaluationMetrics_Gyr_Avg.getTrnSize()[0], EvaluationMetrics_Gyr_Avg.getTstSize()[0], str(round(EvaluationMetrics_Gyr_Avg.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Gyr_Avg.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Gyr_Avg.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Gyr_Avg.getFRR()[0]*100,pre))+' %'])
        SumaryTable.add_row(['Sensors', EvaluationMetrics_Sensors_Avg.getTrnSize()[0], EvaluationMetrics_Sensors_Avg.getTstSize()[0], str(round(EvaluationMetrics_Sensors_Avg.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Sensors_Avg.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Sensors_Avg.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Sensors_Avg.getFRR()[0]*100,pre))+' %'])
        print(SumaryTable.draw())
        
        row_Swipes = np.array([[EvaluationMetrics_Swipes_Avg.getTrnSize()[0], EvaluationMetrics_Swipes_Avg.getTstSize()[0], EvaluationMetrics_Swipes_Avg.getAccuracy()[0], EvaluationMetrics_Swipes_Avg.getF1Score()[0], EvaluationMetrics_Swipes_Avg.getFAR()[0], EvaluationMetrics_Swipes_Avg.getFRR()[0]]])
        row_Acc = np.array([[EvaluationMetrics_Acc_Avg.getTrnSize()[0], EvaluationMetrics_Acc_Avg.getTstSize()[0], EvaluationMetrics_Acc_Avg.getAccuracy()[0], EvaluationMetrics_Acc_Avg.getF1Score()[0], EvaluationMetrics_Acc_Avg.getFAR()[0], EvaluationMetrics_Acc_Avg.getFRR()[0]]])
        row_Gyr = np.array([[EvaluationMetrics_Gyr_Avg.getTrnSize()[0], EvaluationMetrics_Gyr_Avg.getTstSize()[0], EvaluationMetrics_Gyr_Avg.getAccuracy()[0], EvaluationMetrics_Gyr_Avg.getF1Score()[0], EvaluationMetrics_Gyr_Avg.getFAR()[0], EvaluationMetrics_Gyr_Avg.getFRR()[0]]])
        row_Sensors = np.array([[EvaluationMetrics_Sensors_Avg.getTrnSize()[0], EvaluationMetrics_Sensors_Avg.getTstSize()[0], EvaluationMetrics_Sensors_Avg.getAccuracy()[0], EvaluationMetrics_Sensors_Avg.getF1Score()[0], EvaluationMetrics_Sensors_Avg.getFAR()[0], EvaluationMetrics_Sensors_Avg.getFRR()[0]]])
        
        mat_Swipes = np.append(mat_Swipes, row_Swipes, axis=0)
        mat_Acc = np.append(mat_Acc, row_Acc, axis=0)
        mat_Gyr = np.append(mat_Gyr, row_Gyr, axis=0)
        mat_Sensors = np.append(mat_Sensors, row_Sensors, axis=0)
        print('---Window:', Window, '---Overlap:', Overlap)
        
sys.stdout = orig_stdout
f.close()





