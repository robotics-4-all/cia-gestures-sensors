"""
Mathisis_Exp_004
- Select Mathisis Users
- No synced sensors
- No synced gestures
- Sensors Feature Extraction in Timestamp
- Window 500 | Overlap 0.9
"""

#################
#    IMPORTS    #
#################
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from heatmap import corrplot
from texttable import Texttable
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from s1_Funcs_ExploreData_v000 import findUsers_Sensors, findUsers_Swipes, findUsers_Common
from s2_Funcs_CreateDataFrames_v000 import Create_DF_Sensors, Create_DF_Gestures
from s3_Funcs_ExtractFeatures_v000 import Create_DFF_Sensors, Create_DFF_Swipes
from s5_Funcs_HandleClassifiers_v000 import RunML, AppendUserMetrics, CalculateMeanMetrics
from s5_Class_EvaluationMetrics_v000 import EvaluationMetrics


############################
#    GENERAL PARAMETERS    #
############################
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
saveDir = '__Saves__'
ScreenName = 'Mathisis'
Exp = '_Exp_004'
Exp_Save_Path = os.path.join(saveDir, ScreenName+Exp)


########################
#    EXPLORING DATA    #
########################
# Find all users with valid senros data (synced or not)
# -----------------------------------------------------
Synced_Sensors = False
minData_Screen = 1
minData_TimeStamp = 500
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
maxSensData = 20000
minGest = 1
maxGest = float('inf')
DF_Users_All, _ = findUsers_Common(valUsers_Sensors, valUsers_Swipes, Synced_Sensors_Gestures, minSensData, maxSensData, minGest, maxGest)

"""
# Load from pickles
# -----------------
valUsers_Sensors = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))
valUsers_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Swipes.pkl'))
DF_Users_All = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_All.pkl'))

# Save to pickles
# ---------------
valUsers_Sensors.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))
valUsers_Swipes.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Swipes.pkl'))
DF_Users_All.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_All.pkl'))
"""


#########################
#    SELECTING USERS    #
#########################    
# Select a number of users
# ------------------------
Number_Of_Users = 13
if (Number_Of_Users > len(DF_Users_All)):
    raise ValueError('Not so many users : num_of_users > len(DF_Users)')

DF_Users_Final = DF_Users_All.sample(n = Number_Of_Users, replace = False)
DF_Users_Final = DF_Users_Final.reset_index(drop=True)

"""
# Load from pickles
#------------------
DF_Users_Final = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Final.pkl'))

# Save to pickles
#----------------
DF_Users_Final.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Final.pkl'))
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
DF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Acc.pkl'))
DF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr.pkl'))
DF_Gest = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gest.pkl'))

# Save to pickles
# ---------------
DF_Acc.to_pickle(os.path.join(Exp_Save_Path, 'DF_Acc.pkl'))
DF_Gyr.to_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr.pkl'))
DF_Gest.to_pickle(os.path.join(Exp_Save_Path, 'DF_Gest.pkl'))
""" 


#############################
#    EXTRACTING FEATURES    #
#############################χ
# Extracting sensors data features
# --------------------------------
Sensors_Feature = 'Magnitude'
Synced_Sensors = False
Window = 500
Overlap = 0.9
DFF_Acc, DFF_Gyr = Create_DFF_Sensors(DF_Users_Final, DF_Acc, DF_Gyr, Sensors_Feature, Synced_Sensors, Window, Overlap)

# Extracting swipes features
# --------------------------
Normalize_Swipes = True
DFF_Swipes = Create_DFF_Swipes(DF_Gest, Normalize_Swipes)
        
"""
# Load from pickles
# -----------------
DFF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc.pkl'))
DFF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr.pkl'))
DFF_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes.pkl'))

# Save to pickles
# ---------------
DFF_Acc.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc.pkl'))
DFF_Gyr.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr.pkl'))
DFF_Swipes.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes.pkl'))
"""