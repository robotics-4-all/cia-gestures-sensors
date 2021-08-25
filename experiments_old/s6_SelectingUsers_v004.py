"""
- Select Mathisis Users
- Synced sensors
- No synced gestures
- Sensors Feature Extraction in Timestamp
- Window 200 | Overlap 0.9
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

from s1_Funcs_ExploreData_v002 import findUsers_Sensors, findUsers_Swipes, findUsers_Common
from s2_Funcs_CreateDataFrames_v002 import Create_DF_Sensors, Create_DF_Gestures
from s3_Funcs_ExtractFeatures_v003 import Create_DFF_Sensors, Create_DFF_Swipes


############################
#    GENERAL PARAMETERS    #
############################
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
saveDir = '__Saves__'
ScreenName = 'Mathisis'
Exp = '_Exp_007'
Exp_Save_Path = os.path.join(saveDir, ScreenName+Exp)

if not os.path.exists(Exp_Save_Path):
    os.makedirs(Exp_Save_Path)


########################
#    EXPLORING DATA    #
########################
minData_S = 500
minData_U = 1
maxData_U = 999999
valUsers_Sensors = findUsers_Sensors(SensData_Path, ScreenName, minData_S, minData_U, maxData_U)

"""
# Load from pickles
# -----------------
valUsers_Sensors = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))

# Save to pickles
# ---------------
valUsers_Sensors.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))
"""

minData_U = 5000
maxData_U = 20000
DF_Users_Final = valUsers_Sensors.loc[(valUsers_Sensors['AccSize_U'] >= 5000) & (valUsers_Sensors['AccSize_U'] <= 20000)]
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

"""
# Load from pickles
# -----------------
DF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Acc.pkl'))
DF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr.pkl'))

# Save to pickles
# ---------------
DF_Acc.to_pickle(os.path.join(Exp_Save_Path, 'DF_Acc.pkl'))
DF_Gyr.to_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr.pkl'))
""" 


#############################
#    EXTRACTING FEATURES    #
#############################χ
# Extracting sensors data features
# --------------------------------
Sensors_Feature = 'Magnitude'
Window = 200
Overlap = 0.9
DFF_Acc, DFF_Gyr = Create_DFF_Sensors(DF_Users_Final, DF_Acc, DF_Gyr, Sensors_Feature, Window, Overlap)


        
"""
# Load from pickles
# -----------------
DFF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc.pkl'))
DFF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr.pkl'))

# Save to pickles
# ---------------
DFF_Acc.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc.pkl'))
DFF_Gyr.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr.pkl'))
"""