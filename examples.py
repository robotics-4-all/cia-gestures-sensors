########################################
# s1_DataExplorer - Example
########################################
# Imports
from s1_DataExplorer import findUsers_SensorsData, findUsers_GesturesData, findUsers_SGdata
import pandas as pd

# Parameters
SensorsData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GesturesData_DatabaseName = 'my_data'


#--------------------------------------------------
# Find valid users for Mathisis
ScreenName = 'Mathisis'
#--------------------------------------------------
## Find users with valid sensors data
valUsers_Mathisis_S, valUsers_Mathisis_S_isSynced = findUsers_SensorsData(SensorsData_Path, ScreenName=ScreenName, syncSensorsData=False, minSensorsData=1, maxSensorsData=float('inf'))
valUsers_Mathisis_S_Synced, valUsers_Mathisis_S_Synced_isSynced = findUsers_SensorsData(SensorsData_Path, ScreenName=ScreenName, syncSensorsData=True, minSensorsData=1, maxSensorsData=float('inf'))

## Find users with valid gestures (swipes) data 
valUsers_Mathisis_G = findUsers_GesturesData(GesturesData_DatabaseName, GesturesType='swipe', ScreenName=ScreenName, minGestureData=4, maxGestureData=10, minGestures=1, maxGestures=float('inf'))

## Find valid common users
valUsers_Mathisis_SG, valUsers_Mathisis_SG_isSynced = findUsers_SGdata(valUsers_Mathisis_S, valUsers_Mathisis_S_isSynced, valUsers_Mathisis_G, syncSensorsGesturesData=False, minSensorsData=3000, maxSensorsData=float('inf'), minGestures=10, maxGestures=float('inf'))
valUsers_Mathisis_SG_Synced, valUsers_Mathisis_SG_Synced_isSynced = findUsers_SGdata(valUsers_Mathisis_S_Synced, valUsers_Mathisis_S_Synced_isSynced, valUsers_Mathisis_G, syncSensorsGesturesData=True, minSensorsData=3000, maxSensorsData=float('inf'), minGestures=10, maxGestures=float('inf'))

#--------------------------------------------------
# Find valid users for Focus
ScreenName = 'Focus'
#--------------------------------------------------
## Find users with valid sensors data
valUsers_Focus_S, valUsers_Focus_S_isSynced = findUsers_SensorsData(SensorsData_Path, ScreenName=ScreenName, syncSensorsData=False, minSensorsData=1, maxSensorsData=float('inf'))
valUsers_Focus_S_Synced, valUsers_Focus_S_Synced_isSynced = findUsers_SensorsData(SensorsData_Path, ScreenName=ScreenName, syncSensorsData=True, minSensorsData=1, maxSensorsData=float('inf'))

## Find users with valid gestures (swipes) data 
valUsers_Focus_G = findUsers_GesturesData(GesturesData_DatabaseName, GesturesType='swipe', ScreenName=ScreenName, minGestureData=4, maxGestureData=10, minGestures=1, maxGestures=float('inf'))

## Find valid common users
valUsers_Focus_SG, valUsers_Focus_SG_isSynced = findUsers_SGdata(valUsers_Focus_S, valUsers_Focus_S_isSynced, valUsers_Focus_G, syncSensorsGesturesData=False, minSensorsData=3000, maxSensorsData=float('inf'), minGestures=10, maxGestures=float('inf'))
valUsers_Focus_SG_Synced, valUsers_Focus_SG_Synced_isSynced = findUsers_SGdata(valUsers_Focus_S_Synced, valUsers_Focus_S_Synced_isSynced, valUsers_Focus_G, syncSensorsGesturesData=True, minSensorsData=3000, maxSensorsData=float('inf'), minGestures=10, maxGestures=float('inf'))

"""
#--------------------------------------------------
# Save to pickles
saveDir = 'savedData'
#--------------------------------------------------
## Mathisis
valUsers_Mathisis_S.to_pickle(saveDir + '\\' + 'valUsers_Mathisis_S.pkl')
valUsers_Mathisis_S_Synced.to_pickle(saveDir + '\\' + 'valUsers_Mathisis_S_Synced.pkl')
valUsers_Mathisis_G.to_pickle(saveDir + '\\' + 'valUsers_Mathisis_G.pkl')
valUsers_Mathisis_SG.to_pickle(saveDir + '\\' + 'valUsers_Mathisis_SG.pkl')
valUsers_Mathisis_SG_Synced.to_pickle(saveDir + '\\' + 'valUsers_Mathisis_SG_Synced.pkl')
## Focus
valUsers_Focus_S.to_pickle(saveDir + '\\' + 'valUsers_Focus_S.pkl')
valUsers_Focus_S_Synced.to_pickle(saveDir + '\\' + 'valUsers_Focus_S_Synced.pkl')
valUsers_Focus_G.to_pickle(saveDir + '\\' + 'valUsers_Focus_G.pkl')
valUsers_Focus_SG.to_pickle(saveDir + '\\' + 'valUsers_Focus_SG.pkl')
valUsers_Focus_SG_Synced.to_pickle(saveDir + '\\' + 'valUsers_Focus_SG_Synced.pkl')
        
#--------------------------------------------------
# Load from pickles
saveDir = 'savedData'
#--------------------------------------------------
## Mathisis
valUsers_Mathisis_S = pd.read_pickle(saveDir + '\\' + 'valUsers_Mathisis_S.pkl')
valUsers_Mathisis_S_isSynced = False
valUsers_Mathisis_S_Synced = pd.read_pickle(saveDir + '\\' + 'valUsers_Mathisis_S_Synced.pkl')
valUsers_Mathisis_S_Synced_isSynced = True
valUsers_Mathisis_G = pd.read_pickle(saveDir + '\\' + 'valUsers_Mathisis_G.pkl')
valUsers_Mathisis_SG = pd.read_pickle(saveDir + '\\' + 'valUsers_Mathisis_SG.pkl')
valUsers_Mathisis_SG_isSynced = False
valUsers_Mathisis_SG_Synced = pd.read_pickle(saveDir + '\\' + 'valUsers_Mathisis_SG_Synced.pkl')
valUsers_Mathisis_SG_Synced_isSynced = True
## Focus
valUsers_Focus_S = pd.read_pickle(saveDir + '\\' + 'valUsers_Focus_S.pkl')
valUsers_Focus_S_isSynced = False
valUsers_Focus_S_Synced = pd.read_pickle(saveDir + '\\' + 'valUsers_Focus_S_Synced.pkl')
valUsers_Focus_S_Synced_isSynced = True
valUsers_Focus_G = pd.read_pickle(saveDir + '\\' + 'valUsers_Focus_G.pkl')
valUsers_Focus_SG = pd.read_pickle(saveDir + '\\' + 'valUsers_Focus_SG.pkl')
valUsers_Focus_SG_isSynced = False
valUsers_Focus_SG_Synced = pd.read_pickle(saveDir + '\\' + 'valUsers_Focus_SG_Synced.pkl')
valUsers_Focus_SG_Synced_isSynced = True
"""

########################################
# s2_DataFramesCreator - Example
########################################
# Imports
from s2_DataFramesCreator import Create_SensorsGestures_DataFrames
import pandas as pd

# General Parameters
SensorsData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GesturesData_DatabaseName = 'my_data'

#--------------------------------------------------
# Example for not synced data in Mathisis
ScreenName = 'Mathisis'
#--------------------------------------------------
## Load Data 
saveDir = 'savedData'
valUsers_Mathisis_SG = pd.read_pickle(saveDir + '\\' + 'valUsers_Mathisis_SG.pkl')
valUsers_Mathisis_SG_isSynced = False

## Select a number of random users
num_of_users = 5
if (num_of_users > len(valUsers_Mathisis_SG)):
    raise ValueError('Not so many users : num_of_users > len(valUsers)')

DF_valUsers_Mathisis_SG = valUsers_Mathisis_SG.sample(n = num_of_users, replace = False)

## Create Data Frames
DF_Accelerometer_M_NS, DF_Gyroscope_M_NS, DF_Gestures_M_NS = Create_SensorsGestures_DataFrames(SensorsData_Path, GesturesData_DatabaseName, ScreenName, DF_valUsers_Mathisis_SG, valUsers_Mathisis_SG_isSynced)

#--------------------------------------------------
# Example for synced data in Focus
ScreenName = 'Focus'
#--------------------------------------------------
## Load Data 
saveDir = 'savedData'
valUsers_Focus_SG_Synced = pd.read_pickle(saveDir + '\\' + 'valUsers_Focus_SG_Synced.pkl')
valUsers_Focus_SG_Synced_isSynced = True

## Select a number of random users
num_of_users = 1
if (num_of_users > len(valUsers_Focus_SG_Synced)):
    raise ValueError('Not so many users : num_of_users > len(valUsers)')

DF_valUsers_Focus_SG_Synced = valUsers_Focus_SG_Synced.sample(n = num_of_users, replace = False)

## Create Data Frames
DF_Accelerometer_F_S, DF_Gyroscope_F_S, DF_Gestures_F_S = Create_SensorsGestures_DataFrames(SensorsData_Path, GesturesData_DatabaseName, ScreenName, DF_valUsers_Focus_SG_Synced, valUsers_Focus_SG_Synced_isSynced)
    