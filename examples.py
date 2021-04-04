### Example for mathisis

########################################
## Imports
########################################
import pandas as pd
from s0_HelpFunctions import SelectUsers
from s1_ExploreData import findUsers_Sensors, findUsers_Swipes, findUsers_Common
from s2_CreateDataFrames import Create_DF_Sensors, Create_DF_Gestures
from s3_CreateFeaturesDataFrames import Create_FDF_Sensors, Create_FDF_Swipes
from s4_CreateTrnTstSets import CreateTrnTst


########################################
## Explore Users
######################################## 
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
ScreenName = 'Mathisis'

# Find all users with valid data (synced or not) senros data
Synced_Sensors = False
minData_Screen = 2
minData_TimeStamp = 1
minData_User = 1
valUsers_Sensors, _ = findUsers_Sensors(SensData_Path, ScreenName, Synced_Sensors, minData_Screen, minData_TimeStamp, minData_User)

# Find all users with valid synced senros data
Synced_Sensors = True
valUsers_Sensors_Sync, _ = findUsers_Sensors(SensData_Path, ScreenName, Synced_Sensors, minData_Screen, minData_TimeStamp, minData_User)

# Find all users with valid swipes
maxDeviceWidth = 600
maxDeviceHeight = 1000
Fake_Swipe_Limit = 30
minData_Gesture = 4
maxData_Gesture = 10
minGesture_User = 1
valUsers_Swipes = findUsers_Swipes(GestData_DBName, ScreenName, maxDeviceWidth, maxDeviceHeight, Fake_Swipe_Limit, minData_Gesture, maxData_Gesture, minGesture_User)

# Find all users have sensros and gestures (synced or not)
Synced_Sensors_Gestures = False
minSensData = 1000
maxSensData = 5000
minGest = 1
maxGest = float('inf')
DF_Users_All, _ = findUsers_Common(valUsers_Sensors, valUsers_Swipes, Synced_Sensors_Gestures, minSensData, maxSensData, minGest, maxGest)

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

"""
# Save to pickles
saveDir = 'savedData'
valUsers_Sensors.to_pickle(saveDir + '\\' + 'valUsers_Sensors.pkl')
valUsers_Sensors_Sync.to_pickle(saveDir + '\\' + 'valUsers_Sensors_Sync.pkl')
valUsers_Swipes.to_pickle(saveDir + '\\' + 'valUsers_Swipes.pkl')

# Load from pickles
saveDir = 'savedData'
valUsers_Sensors = pd.read_pickle(saveDir + '\\' + 'valUsers_Sensors.pkl')
valUsers_Sensors_Sync = pd.read_pickle(saveDir + '\\' + 'valUsers_Sensors_Sync.pkl')
valUsers_Swipes = pd.read_pickle(saveDir + '\\' + 'valUsers_Swipes.pkl')

are_equal_Sens_Sens_Sync = valUsers_Sensors.equals(valUsers_Sensors_Sync)
are_equal_Sens_Sens_Sync = valUsers_Sensors.eq(valUsers_Sensors_Sync)

are_equal_All_SAG_SG = DF_Users_All_SynSAG.equals(DF_Users_All_SynSwipeSensors)
are_equal_All_SAG_SG = DF_Users_All_SynSAG.eq(DF_Users_All_SynSwipeSensors)

Mathisis    : There is only one user that has only gyr data synced with swipes with out having acc data at the same time !! 
Focus       : There is only one user that has only acc data synced with swipes with out having gyr data at the same time !!
"""

########################################
## Select Users
######################################## 
Number_Of_Users = 3
Original_Users, DF_Users_Final = SelectUsers(DF_Users_All, DF_Users_All_SynSwipeSensors, Number_Of_Users)

########################################
## Create Dataframes
########################################
DF_Acc, DF_Gyr = Create_DF_Sensors(SensData_Path, DF_Users_Final)
DF_Gest = Create_DF_Gestures(GestData_DBName, DF_Users_Final)
              
########################################
## Create Features Data Frames
########################################
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
## Select User & Create Train & Test Sets
########################################
Split_Rate = 0.25

#for Original_User in Original_Users:
    #print('Original_User: ', Original_User)
    
Original_User = 'x89587l'
FDFs_Original, FDFs_Attackers = CreateTrnTst(FDF_Swipes, FDF_Acc, FDF_Gyr, Original_User, Split_Rate)

"""
FDFs_Original = [FDFs_Org_Trn, FDFs_Org_Tst, FDFs_Org_Trn_Syn, FDFs_Org_Tst_Syn]
FDFs_Attackers = [FDFs_Att, FDFs_Att_Syn]

FDFs = [Swipes, Acc, Gyr]
"""