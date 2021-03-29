########################################
########################################
# s1_ExplloreData
########################################
########################################
# Imports
import pandas as pd
from s1_ExploreData import findUsers_Sensors, findUsers_Swipes, findUsers_Common


# General Parameters
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
ScreenName = 'Mathisis'


# Find users with valid sensors data
Synced_Sensors = False
minTmStData = 1 # -> Mhpws toulaxiston 2 gia na bwrei na ginei feature extraction?? 
minUserData = 1
valUsers_Sensors, Synced_Sensors = findUsers_Sensors(SensData_Path, ScreenName, Synced_Sensors, minTmStData, minUserData)


# Find users with valid swipes data
maxDeviceWidth = 600
maxDeviceHeight = 1000
Fake_Swipe_Limit = 30
minGestData = 4
maxGestData = 10
minUserGest = 1
valUsers_Swipes = findUsers_Swipes(GestData_DBName, ScreenName, maxDeviceWidth, maxDeviceHeight, Fake_Swipe_Limit, minGestData, maxGestData, minUserGest)


# Find valid common users
Synced_Common = False
minSensData = 3000
minGest = 10
valUsers_Common, Synced_Common = findUsers_Common(valUsers_Sensors, Synced_Sensors, valUsers_Swipes, Synced_Common, minSensData, minGest)


"""
# Save to pickles
saveDir = 'savedData'
valUsers_Sensors.to_pickle(saveDir + '\\' + 'valUsers_Sensors.pkl')
valUsers_Swipes.to_pickle(saveDir + '\\' + 'valUsers_Swipes.pkl')
valUsers_Common.to_pickle(saveDir + '\\' + 'valUsers_Common.pkl')

# Load from pickles
saveDir = 'savedData'
valUsers_Sensors = pd.read_pickle(saveDir + '\\' + 'valUsers_Sensors.pkl')
Synced_Sensors = False
valUsers_Swipes = pd.read_pickle(saveDir + '\\' + 'valUsers_Swipes.pkl')
valUsers_Common = pd.read_pickle(saveDir + '\\' + 'valUsers_Common.pkl')
Synced_Common = False
"""


########################################
########################################
# s2_CreareDataFrames
########################################
########################################
# Imports
import pandas as pd
from s2_CreateDataFrames import Create_DF_Sensors, Create_DF_Gestures


# General Parameters
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
ScreenName = 'Mathisis'

"""
saveDir = 'savedData'
DF_Users = pd.read_pickle(saveDir + '\\' + 'valUsers_Common.pkl')
"""
DF_Users = valUsers_Common


# Select a number of random users
num_of_users = 5
if (num_of_users > len(DF_Users)):
    raise ValueError('Not so many users : num_of_users > len(DF_Users)')
DF_Users = DF_Users.sample(n = num_of_users, replace = False)


# Create DFs
DF_Acc, DF_Gyr = Create_DF_Sensors(SensData_Path, DF_Users, ScreenName)
DF_Gest = Create_DF_Gestures(GestData_DBName, DF_Users, ScreenName)
 

"""
# Save to pickles
saveDir = 'savedData'
DF_Users.to_pickle(saveDir + '\\' + 'DF_Users.pkl')
DF_Acc.to_pickle(saveDir + '\\' + 'DF_Acc.pkl')
DF_Gyr.to_pickle(saveDir + '\\' + 'DF_Gyr.pkl')
DF_Gest.to_pickle(saveDir + '\\' + 'DF_Gest.pkl')

# Load from pickles
saveDir = 'savedData'
DF_Users = pd.read_pickle(saveDir + '\\' + DF_Users.pkl')
DF_Acc = pd.read_pickle(saveDir + '\\' + 'DF_Acc.pkl')
DF_Gyr = pd.read_pickle(saveDir + '\\' + 'DF_Gyr.pkl')
DF_Gest = pd.read_pickle(saveDir + '\\' + 'DF_Gest.pkl')
"""


########################################
########################################
# s3_CreareFeaturesDataFrames
########################################
########################################
# Imports
import pandas as pd
from s3_CreateFeaturesDataFrames import Create_FDF_Sensors, Create_FDF_Swipes


# Parameters
"""
saveDir = 'savedData'
DF_Users = pd.read_pickle(saveDir + '\\' + 'DF_Users.pkl')
DF_Acc = pd.read_pickle(saveDir + '\\' + 'DF_Acc.pkl')
DF_Gyr = pd.read_pickle(saveDir + '\\' + 'DF_Gyr.pkl')
DF_Gest = pd.read_pickle(saveDir + '\\' + 'DF_Gest.pkl')
"""

Original_User = DF_Users.sample(1, replace = False)['User'].values[0]
Original_Num_Acc = len(DF_Acc[DF_Acc['User'] == Original_User])
Original_Num_Gyr = len(DF_Gyr[DF_Gyr['User'] == Original_User])
Original_Num_Gest = len(DF_Gest[DF_Gest['User'] == Original_User])


# Create FDFs
Feature = 'Magnitude'
WindowSize = 500
Overlap = 50  
FDF_Acc, FDF_Gyr = Create_FDF_Sensors(Original_User, DF_Users, DF_Acc, DF_Gyr, Feature, WindowSize, Overlap)

Normalize = True
FDF_Swipes = Create_FDF_Swipes(Original_User, DF_Gest, Normalize)


"""
# Save to pickles
saveDir = 'savedData'
FDF_Acc.to_pickle(saveDir + '\\' + 'FDF_Acc.pkl')
FDF_Gyr.to_pickle(saveDir + '\\' + 'FDF_Gyr.pkl')
FDF_Swipes.to_pickle(saveDir + '\\' + 'FDF_Swipes.pkl')

# Load from pickles
saveDir = 'savedData'
Original_User = 'adj01eb'
FDF_Acc = pd.read_pickle(saveDir + '\\' + 'FDF_Acc.pkl')
FDF_Gyr = pd.read_pickle(saveDir + '\\' + 'FDF_Gyr.pkl')
FDF_Swipes = pd.read_pickle(saveDir + '\\' + 'FDF_Swipes.pkl')
"""


########################################
########################################
# Slit in train & test sets
########################################
########################################
import numpy as np
import pandas as pd
from random import randint


def GetIndexes(Dataset, Slit_Rate):
    
    Indexes = []
    Num_Data = int(np.floor(len(Dataset) * Split_Rate))
    
    for i in range(Num_Data):
        rnd = randint(0, len(Dataset) - 1)
        while(Dataset[rnd] in Indexes):
            rnd = randint(0, len(Dataset) - 1)
        Indexes.append(Dataset[rnd])
        
    return Indexes


def CreateSets(Dataset, Indexes):
    
    Train = pd.DataFrame()
    Test = pd.DataFrame()
    
    for idx in range(len(Dataset)):
        row = Dataset.loc[idx]
        if idx in Indexes:
            Test = Test.append(row, ignore_index=True)
        else:
            if (row['Output'] == 0):
                Test = Test.append(row, ignore_index=True)
            elif (row['Output'] == 1):
                Train = Train.append(row, ignore_index=True)
                
    return Train, Test

# Get original users indexes for test
Original_User_Idx_Acc = FDF_Acc.loc[FDF_Acc['Output'] == 1].index
Original_User_Idx_Gyr = FDF_Gyr.loc[FDF_Gyr['Output'] == 1].index
Original_User_Idx_Swipes = FDF_Swipes.loc[FDF_Swipes['Output'] == 1].index

Synced_Sensors = False
Synced_Common = False
Split_Rate = 0.25

if ((not(Synced_Sensors))and(not(Synced_Common))): # No synced data
    Indexes_Acc = GetIndexes(Original_User_Idx_Acc, Split_Rate)
    Indexes_Gyr = GetIndexes(Original_User_Idx_Gyr, Split_Rate)
    Indexes_Swipes = GetIndexes(Original_User_Idx_Swipes, Split_Rate)

if ((Synced_Sensors)and(not(Synced_Common))): # Sensors Data are synced
    Indexes_Acc = GetIndexes(Original_User_Idx_Acc, Split_Rate)
    Indexes_Gyr = Indexes_Acc
    Indexes_Swipes = GetIndexes(Original_User_Idx_Swipes, Split_Rate)
    
#if ((Synced_Sensors)and(Synced_Common)): # Sensors & Gestures Data are synced


# Greate Train, Test Sets
sTrain_Acc, sTest_Acc = CreateSets(FDF_Acc, Indexes_Acc)
sTrain_Gyr, sTest_Gyr = CreateSets(FDF_Gyr, Indexes_Gyr)
sTrain_Swipes, sTest_Swipes = CreateSets(FDF_Swipes, Indexes_Swipes)
                
                
                    
                    

    
    

    