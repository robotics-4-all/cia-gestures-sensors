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


"""
Gia TIMESTAMP
"""


############################
#    GENERAL PARAMETERS    #
############################
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
saveDir = '__Saves__'
ScreenName = 'Focus'
Exp = '_Exp_002'
Exp_Save_Path = os.path.join(saveDir, ScreenName+Exp)

if not os.path.exists(Exp_Save_Path):
    os.makedirs(Exp_Save_Path)


########################
#    EXPLORING DATA    #
########################
# Sensors Users
# -------------
minData_TS = 200
minData_U = 1
maxData_U = 9999999
valUsers_Sensors = findUsers_Sensors(SensData_Path, ScreenName, minData_TS, minData_U, maxData_U)
# valUsers_Sensors = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))
# valUsers_Sensors.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))

minData_U = 5000
maxData_U = 20000
DF_Users_Final = valUsers_Sensors.loc[(valUsers_Sensors['AccSize_U'] >= 5000) & (valUsers_Sensors['AccSize_U'] <= 20000)]
DF_Users_Final = DF_Users_Final.reset_index(drop=True)


# Swipes Users
# ------------
maxDeviceWidth = 600
maxDeviceHeight = 1000
Fake_Swipe_Limit = 30
minData_Gesture = 4
maxData_Gesture = 10
minGesture_User = 1
valUsers_Swipes = findUsers_Swipes(GestData_DBName, ScreenName, maxDeviceWidth, maxDeviceHeight, Fake_Swipe_Limit, minData_Gesture, maxData_Gesture, minGesture_User)
# valUsers_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Swipes.pkl'))
# valUsers_Swipes.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Swipes.pkl'))

# Common Users
# ------------
Synced_Sensors_Gestures = True
minSensData = 1
maxSensData = 9999999
minGest = 1
maxGest = 9999999
DF_Users_Sensrors, DF_Users_Swipes = findUsers_Common(valUsers_Sensors, valUsers_Swipes, Synced_Sensors_Gestures, minSensData, maxSensData, minGest, maxGest)

Synced_Sensors_Gestures = False
minSensData = 1
maxSensData = 9999999
minGest = 1
maxGest = 9999999
DF_Users_Sensrors_F, DF_Users_Swipes_F = findUsers_Common(valUsers_Sensors, valUsers_Swipes, Synced_Sensors_Gestures, minSensData, maxSensData, minGest, maxGest)