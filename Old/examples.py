### Example for mathisis

########################################
## Imports
########################################
from s0_HelpFunctions import SelectUsers
from s1_ExploreData import findUsers_Sensors, findUsers_Swipes, findUsers_Common
from s2_CreateDataFrames import Create_DF_Sensors, Create_DF_Gestures
from s3_CreateFeaturesDataFrames import Create_FDF_Sensors, Create_FDF_Swipes
from s4_CreateFinalSets import CreateFinalSets
from s5_ModelsFunctions import Train_Model, Model_Predict

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler


########################################
## Explore Users
## After expiriments was found that : 
## 1. There are not enought users with synced Sensors & Gestures data neither in Mathisis nor in Focus.
## 2. There is only one user in Mathisis and in Focus that has only gyr and acc data respectively, synced with swipes with out having acc and gyr data respectively at the same time.
## So there are 2 options :
## 1. Use totaly unsyned data
## 2. Use synced sensors and unsynced swipes.
########################################
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
ScreenName = 'Mathisis'

print('######################')
print('--- Exploring Data ---')
print('######################')

#--------------------------------------------------
# Find all users with valid senros data (synced or not)
#--------------------------------------------------
Synced_Sensors = True
minData_Screen = 2
minData_TimeStamp = 1
minData_User = 1
valUsers_Sensors, _ = findUsers_Sensors(SensData_Path, ScreenName, Synced_Sensors, minData_Screen, minData_TimeStamp, minData_User)

#--------------------------------------------------
# Find all users with valid swipes
#--------------------------------------------------
maxDeviceWidth = 600
maxDeviceHeight = 1000
Fake_Swipe_Limit = 30
minData_Gesture = 4
maxData_Gesture = 10
minGesture_User = 1
valUsers_Swipes = findUsers_Swipes(GestData_DBName, ScreenName, maxDeviceWidth, maxDeviceHeight, Fake_Swipe_Limit, minData_Gesture, maxData_Gesture, minGesture_User)

#--------------------------------------------------
# Find all users have sensros and gestures (synced or not)
#--------------------------------------------------
Synced_Sensors_Gestures = False
minSensData = 3000
maxSensData = 6000
minGest = 300
maxGest = 600
DF_Users_All, _ = findUsers_Common(valUsers_Sensors, valUsers_Swipes, Synced_Sensors_Gestures, minSensData, maxSensData, minGest, maxGest)

"""
#--------------------------------------------------
# These were used in synced data exploration.
#--------------------------------------------------
# Find all users with valid synced senros data
Synced_Sensors = True
valUsers_Sensors_Sync, _ = findUsers_Sensors(SensData_Path, ScreenName, Synced_Sensors, minData_Screen, minData_TimeStamp, minData_User)
# Find all users with synced sensors and gestures (swipe & acc & gyr)
Synced_Sensors_Gestures = True
minSensData = 1
maxSensData = float('inf')
minGest = 1            
maxGest = float('inf')
DF_Users_All_SynSAG, _ = findUsers_Common(valUsers_Sensors_Sync, valUsers_Swipes, Synced_Sensors_Gestures, minSensData, maxSensData, minGest, maxGest)
# Find all users with  at least one sensor and gesture synced (swipe & (acc | gyr))
Synced_Sensors_Gestures = True
minSensData = 1
maxSensData = float('inf')
minGest = 1            
maxGest = float('inf')
DF_Users_All_SynSwipeSensors, _ = findUsers_Common(valUsers_Sensors, valUsers_Swipes, Synced_Sensors_Gestures, minSensData, maxSensData, minGest, maxGest)
are_equal_Sens_Sens_Sync = valUsers_Sensors.equals(valUsers_Sensors_Sync)
are_equal_Sens_Sens_Sync = valUsers_Sensors.eq(valUsers_Sensors_Sync)
are_equal_All_SAG_SG = DF_Users_All_SynSAG.equals(DF_Users_All_SynSwipeSensors)
are_equal_All_SAG_SG = DF_Users_All_SynSAG.eq(DF_Users_All_SynSwipeSensors)
"""

"""
#--------------------------------------------------
# Save to pickles
#--------------------------------------------------
saveDir = 'savedData'
valUsers_Sensors.to_pickle(saveDir + '\\' + 'valUsers_Sensors.pkl')
valUsers_Swipes.to_pickle(saveDir + '\\' + 'valUsers_Swipes.pkl')
DF_Users_All.to_pickle(saveDir + '\\' + 'DF_Users_All.pkl')

#--------------------------------------------------
# Load from pickles
#--------------------------------------------------
saveDir = 'savedData'
valUsers_Sensors = pd.read_pickle(saveDir + '\\' + 'valUsers_Sensors.pkl')
valUsers_Swipes = pd.read_pickle(saveDir + '\\' + 'valUsers_Swipes.pkl')
DF_Users_All = pd.read_pickle(saveDir + '\\' + 'DF_Users_All.pkl')
"""


########################################
## Select Users
########################################
print(flush=True)
print('#######################')
print('--- Selecting Users ---')
print('#######################')

Number_Of_Users = 10

if (Number_Of_Users > len(DF_Users_All)):
    raise ValueError('Not so many users : num_of_users > len(DF_Users)')
    
DF_Users_Final = DF_Users_All.sample(n = Number_Of_Users, replace = False)

print(flush=True)
print('->', len(DF_Users_Final), 'Users Selected')

"""
Original_Users, DF_Users_Final = SelectUsers(DF_Users_All, DF_Users_All_SynSwipeSensors, Number_Of_Users)
"""

"""
#--------------------------------------------------
# Save to pickles
#--------------------------------------------------
saveDir = 'savedData'
DF_Users_Final.to_pickle(saveDir + '\\' + 'DF_Users_Final.pkl')

#--------------------------------------------------
# Load from pickles
#--------------------------------------------------
saveDir = 'savedData'
DF_Users_Final = pd.read_pickle(saveDir + '\\' + 'DF_Users_Final.pkl')
"""


########################################
## Create Dataframes
########################################
print(flush=True)
print('############################')
print('--- Creating Data Frames ---')
print('############################')

DF_Acc, DF_Gyr = Create_DF_Sensors(SensData_Path, DF_Users_Final)
DF_Gest = Create_DF_Gestures(GestData_DBName, DF_Users_Final)
              

########################################
## Extract Features
########################################
print(flush=True)
print('###########################')
print('--- Extracting Features ---')
print('###########################', end = '')

Feature = 'Magnitude'
FDF_Acc, FDF_Gyr = Create_FDF_Sensors(DF_Users_Final, DF_Acc, DF_Gyr, Feature)

Normalize = True
FDF_Swipes = Create_FDF_Swipes(DF_Gest, Normalize)

"""
# Save to pickles
saveDir = 'savedData'
FDF_Acc.to_pickle(saveDir + '\\' + 'FDF_Acc.pkl')
FDF_Gyr.to_pickle(saveDir + '\\' + 'FDF_Gyr.pkl')
FDF_Swipes.to_pickle(saveDir + '\\' + 'FDF_Swipes.pkl')

# Load from pickles
saveDir = 'savedData'
FDF_Acc = pd.read_pickle(saveDir + '\\' + 'FDF_Acc.pkl')
FDF_Gyr = pd.read_pickle(saveDir + '\\' + 'FDF_Gyr.pkl')
FDF_Swipes = pd.read_pickle(saveDir + '\\' + 'FDF_Swipes.pkl')
"""


########################################
## Select Original User & Create Final Sets
### FDFs_Original = [FDFs_Org_Trn, FDFs_Org_Tst, FDFs_Org_Trn_Syn, FDFs_Org_Tst_Syn]
### FDFs_Attackers = [FDFs_Att, FDFs_Att_Syn]
### FDFs = [Swipes, Acc, Gyr]
########################################
Split_Rate = 0.25

#for Original_User in Original_Users:
    #print('Original_User: ', Original_User)
    
Original_User = 'x89587l'
FDFs_Original, FDFs_Attackers = CreateFinalSets(FDF_Swipes, FDF_Acc, FDF_Gyr, Original_User, Split_Rate)


########################################
## Select Train & Test Sets
########################################
"""
Final_Features_Swipes = [0, 1, 2, 4, 5, 6, 7, 8, 9, 11, 14, 15]
Final_Features_Sensors = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16]

# Train Set
TrnSet_X_Swipes = FDFs_Original[0][0].iloc[:, Final_Features_Swipes]
TrnSet_Y_Swipes = FDFs_Original[0][0].iloc[:, [18]]

TrnSet_X_Acc = FDFs_Original[0][1].iloc[:, Final_Features_Sensors]
TrnSet_Y_Acc = FDFs_Original[0][1].iloc[:, [19]]

TrnSet_X_Gyr = FDFs_Original[0][2].iloc[:, Final_Features_Sensors]
TrnSet_Y_Gyr = FDFs_Original[0][2].iloc[:, [19]]

# Test Set
TstSet_X_Swipes = FDFs_Attackers[0][0].iloc[:, Final_Features_Swipes]
TstSet_Y_Swipes = FDFs_Attackers[0][0].iloc[:, [18]]

TstSet_X_Acc = FDFs_Attackers[0][1].iloc[:, Final_Features_Sensors]
TstSet_Y_Acc = FDFs_Attackers[0][1].iloc[:, [19]]

TstSet_X_Gyr = FDFs_Attackers[0][2].iloc[:, Final_Features_Sensors]
TstSet_Y_Gyr = FDFs_Attackers[0][2].iloc[:, [19]]
"""


########################################
## Normilize Sets (MinMaxScalar)
########################################
"""
Scalar_Swipes = MinMaxScaler().fit(TrnSet_X_Swipes)
Scalar_Acc = MinMaxScaler().fit(TrnSet_X_Acc)
Scalar_Gyr = MinMaxScaler().fit(TrnSet_X_Gyr)

TrnSet_X_Norm_Swipes = Scalar_Swipes.transform(TrnSet_X_Swipes)
TrnSet_X_Norm_Acc = Scalar_Acc.transform(TrnSet_X_Acc)
TrnSet_X_Norm_Gyr = Scalar_Gyr.transform(TrnSet_X_Gyr)

TstSet_X_Norm_Swipes = Scalar_Swipes.transform(TstSet_X_Swipes)
TstSet_X_Norm_Acc = Scalar_Acc.transform(TstSet_X_Acc)
TstSet_X_Norm_Gyr = Scalar_Gyr.transform(TstSet_X_Gyr)
"""


########################################
## Train Models
########################################
"""
Algorithm = 'LocalOutlierFactor'
Parameters = [3]
Model_Swipes, maxDistance_Swipes = Train_Model(Algorithm, Parameters, TrnSet_X_Norm_Swipes)
Model_Acc, maxDistance_Acc = Train_Model(Algorithm, Parameters, TrnSet_X_Norm_Acc)
Model_Gyr, maxDistance_Gyr = Train_Model(Algorithm, Parameters, TrnSet_X_Norm_Gyr)
"""


########################################
## Test Models
########################################
"""
Decision_Swipes, Prediction_Swipes = Model_Predict(Model_Swipes, TstSet_X_Norm_Swipes, maxDistance_Swipes)
Decision_Acc, Prediction_Acc = Model_Predict(Model_Acc, TstSet_X_Norm_Acc, maxDistance_Acc)
Decision_Gyr, Prediction_Gyr = Model_Predict(Model_Gyr, TstSet_X_Norm_Gyr, maxDistance_Gyr)
"""