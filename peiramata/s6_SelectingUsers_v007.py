"""
- FOCUS & MATHISIS
- TIMESTAMP
- minData_TS = 200
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

from s1_Funcs_ExploreData_v001 import findUsers_Sensors, findUsers_Swipes, findUsers_Common
from s2_Funcs_CreateDataFrames_v001 import Create_DF_Sensors, Create_DF_Gestures
from s3_Funcs_ExtractFeatures_v002 import Create_DFF_Sensors, Create_DFF_Swipes


############################
#    GENERAL PARAMETERS    #
############################
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
saveDir = '__Saves__'
ScreenName = 'Mathisis'
Exp = '_Exp_008'
Exp_Save_Path = os.path.join(saveDir, ScreenName+Exp)

if not os.path.exists(Exp_Save_Path):
    os.makedirs(Exp_Save_Path)


########################
#    EXPLORING DATA    #
########################
# -------------
# Sensors Users
# -------------
minData_TS = 200
valUsers_Sensors_All = findUsers_Sensors(SensData_Path, ScreenName, minData_TS, 1, float('inf'))
# valUsers_Sensors_All.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors_All.pkl'))
# valUsers_Sensors_All = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors_All.pkl'))

minData_U = 3000
maxData_U = 25000
valUsers_Sensors = valUsers_Sensors_All.loc[(valUsers_Sensors_All['AccSize_U'] >= minData_U) & (valUsers_Sensors_All['AccSize_U'] <= maxData_U)]
valUsers_Sensors = valUsers_Sensors.reset_index(drop=True)
# valUsers_Sensors.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))
# valUsers_Sensors = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))


# ------------
# Swipes Users
# ------------
maxDeviceWidth = 600
maxDeviceHeight = 1000
Fake_Swipe_Limit = 30
minData_Gesture = 4
maxData_Gesture = 10
minGesture_User = 1
valUsers_Swipes = findUsers_Swipes(GestData_DBName, ScreenName, maxDeviceWidth, maxDeviceHeight, Fake_Swipe_Limit, minData_Gesture, maxData_Gesture, minGesture_User)
# valUsers_Swipes.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Swipes.pkl'))
# valUsers_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Swipes.pkl'))


# ------------
# Common Users
# ------------
Synced_Sensors_Gestures = False
DF_Users_Sensrors_All, DF_Users_Swipes_All = findUsers_Common(valUsers_Sensors, valUsers_Swipes, Synced_Sensors_Gestures, 1, float('inf'), 1, float('inf'))

Synced_Sensors_Gestures = True
DF_Users_Sensrors_S, DF_Users_Swipes_S = findUsers_Common(valUsers_Sensors, valUsers_Swipes, Synced_Sensors_Gestures, 1, float('inf'), 1, float('inf'))

DF_Users_Sensrors_NS = DF_Users_Sensrors_All
for i in range(len(DF_Users_Sensrors_NS)):
    if DF_Users_Sensrors_NS.loc[i]['User'] not in DF_Users_Sensrors_S['User'].values:
        DF_Users_Sensrors_NS = DF_Users_Sensrors_NS.drop(i)
DF_Users_Sensrors_NS = DF_Users_Sensrors_NS.reset_index(drop = True)
for i in range(len(DF_Users_Sensrors_NS)):
    for j in range(len(DF_Users_Sensrors_S.loc[i]['List_Of_TS'])):
        ts_index = DF_Users_Sensrors_NS.loc[i]['List_Of_TS'].index(DF_Users_Sensrors_S.loc[i]['List_Of_TS'][j])
        DF_Users_Sensrors_NS.loc[i]['AccSize_U'] = DF_Users_Sensrors_NS.loc[i]['AccSize_U'] - DF_Users_Sensrors_NS.loc[i]['AccGyrSize_Of_TS'][ts_index][0]
        DF_Users_Sensrors_NS.loc[i]['GyrSize_U'] = DF_Users_Sensrors_NS.loc[i]['GyrSize_U'] - DF_Users_Sensrors_NS.loc[i]['AccGyrSize_Of_TS'][ts_index][1]
        DF_Users_Sensrors_NS.loc[i]['List_Of_TS'].pop(ts_index)
        DF_Users_Sensrors_NS.loc[i]['AccGyrSize_Of_TS'].pop(ts_index)
    DF_Users_Sensrors_NS.loc[i]['Num_Of_TS'] = len(DF_Users_Sensrors_NS.loc[i]['List_Of_TS'])
    
DF_Users_Swipes_NS = DF_Users_Swipes_All
for i in range(len(DF_Users_Swipes_NS)):
    if DF_Users_Swipes_NS.loc[i]['User'] not in DF_Users_Swipes_S['User'].values:
        DF_Users_Swipes_NS = DF_Users_Swipes_NS.drop(i)
DF_Users_Swipes_NS = DF_Users_Swipes_NS.reset_index(drop = True)
for i in range(len(DF_Users_Swipes_NS)):
    for j in range(len(DF_Users_Swipes_S.loc[i]['Gestures_IDs'])):
        g_index = DF_Users_Swipes_NS.loc[i]['Gestures_IDs'].index(DF_Users_Swipes_S.loc[i]['Gestures_IDs'][j])
        DF_Users_Swipes_NS.loc[i]['Gestures_IDs'].pop(ts_index)
        DF_Users_Swipes_NS.loc[i]['Screen_Of_Gestures'].pop(ts_index)
        DF_Users_Swipes_NS.loc[i]['tStartStop_Of_Gestures'].pop(ts_index)
    DF_Users_Swipes_NS.loc[i]['Num_Of_Gestures'] = len(DF_Users_Swipes_NS.loc[i]['Gestures_IDs'])

"""
# SAVES
DF_Users_Sensrors_All.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensrors_All.pkl'))
DF_Users_Swipes_All.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Swipes_All.pkl'))
DF_Users_Sensrors_S.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensrors_S.pkl'))
DF_Users_Swipes_S.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Swipes_S.pkl'))
DF_Users_Sensrors_NS.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensrors_NS.pkl'))
DF_Users_Swipes_NS.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Swipes_NS.pkl'))

# LOADS
DF_Users_Sensrors_All = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensrors_All.pkl'))
DF_Users_Swipes_All = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Swipes_All.pkl'))
DF_Users_Sensrors_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensrors_S.pkl'))
DF_Users_Swipes_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Swipes_S.pkl'))
DF_Users_Sensrors_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensrors_NS.pkl'))
DF_Users_Swipes_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Swipes_NS.pkl'))
"""


#############################
#    CREATING DATAFRAMES    #
#############################
DF_Acc_S, DF_Gyr_S = Create_DF_Sensors(SensData_Path, ScreenName, DF_Users_Sensrors_S)
DF_Gest_S = Create_DF_Gestures(GestData_DBName, DF_Users_Swipes_S)
DF_Acc_NS, DF_Gyr_NS = Create_DF_Sensors(SensData_Path, ScreenName, DF_Users_Sensrors_NS)
DF_Gest_NS = Create_DF_Gestures(GestData_DBName, DF_Users_Swipes_NS)

"""
# SAVES
DF_Acc_S.to_pickle(os.path.join(Exp_Save_Path, 'DF_Acc_S.pkl'))
DF_Gyr_S.to_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr_S.pkl'))
DF_Gest_S.to_pickle(os.path.join(Exp_Save_Path, 'DF_Gest_S.pkl'))
DF_Acc_NS.to_pickle(os.path.join(Exp_Save_Path, 'DF_Acc_NS.pkl'))
DF_Gyr_NS.to_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr_NS.pkl'))
DF_Gest_NS.to_pickle(os.path.join(Exp_Save_Path, 'DF_Gest_NS.pkl'))

# LOADS
DF_Acc_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Acc_S.pkl'))
DF_Gyr_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr_S.pkl'))
DF_Gest_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gest_S.pkl'))
DF_Acc_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Acc_NS.pkl'))
DF_Gyr_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr_NS.pkl'))
DF_Gest_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gest_NS.pkl'))
"""


#############################
#    EXTRACTING FEATURES    #
#############################
# --------------------------------
# Extracting sensors data features
# --------------------------------
Sensors_Feature = 'Magnitude'
Window = 200
Overlap = 0.9
DFF_Acc_S, DFF_Gyr_S = Create_DFF_Sensors(DF_Users_Sensrors_S, DF_Acc_S, DF_Gyr_S, Sensors_Feature, Window, Overlap)
DFF_Acc_NS, DFF_Gyr_NS = Create_DFF_Sensors(DF_Users_Sensrors_NS, DF_Acc_NS, DF_Gyr_NS, Sensors_Feature, Window, Overlap)

"""
# SAVES
DFF_Acc_S.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc_S.pkl'))
DFF_Gyr_S.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr_S.pkl'))
DFF_Acc_NS.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc_NS.pkl'))
DFF_Gyr_NS.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr_NS.pkl'))

# LOADS
DFF_Acc_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc_S.pkl'))
DFF_Gyr_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr_S.pkl'))
DFF_Acc_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc_NS.pkl'))
DFF_Gyr_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr_NS.pkl'))
"""


# --------------------------
# Extracting swipes features
# --------------------------
Normalize_Swipes = True
DFF_Swipes_S = Create_DFF_Swipes(DF_Gest_S, Normalize_Swipes)
DFF_Swipes_NS = Create_DFF_Swipes(DF_Gest_NS, Normalize_Swipes)

"""
# SAVES
DFF_Swipes_S.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes_S.pkl'))
DFF_Swipes_NS.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes_NS.pkl'))

# LOADS
DFF_Swipes_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes_S.pkl'))
DFF_Swipes_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes_NS.pkl'))
"""