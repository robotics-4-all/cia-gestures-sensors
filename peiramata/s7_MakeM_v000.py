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

from s1_Funcs_ExploreData import findUsers_Sensors, findUsers_Swipes, findUsers_Common
from s2_Funcs_CreateDataFrames import Create_DF_Sensors, Create_DF_Gestures
from s3_Funcs_ExtractFeatures import Create_DFF_Sensors, Create_DFF_Swipes
from s4_Funcs_CreateSets import SplitDFF_OrgAtt, SplitRandom
from s5_Funcs_HandleClassifiers import RunML, AppendUserMetrics, CalculateMeanMetrics
from s5_Class_EvaluationMetrics import EvaluationMetrics


# ======================== #
#    General Parameters    #
# ======================== #
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
saveDir = '__Saves__'
ScreenName = 'Mathisis'
Exp = '_Exp_003'
Exp_Save_Path = os.path.join(saveDir, ScreenName+Exp)


# ================== #
#    Explore Data    #
# ================== #
# Load from pickles
# -----------------
valUsers_Sensors = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))
valUsers_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Swipes.pkl'))
DF_Users_All = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_All.pkl'))


# ================== #
#    Select Users    #
# ================== #
# Load from pickles
#------------------
DF_Users_Final = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Final.pkl'))


# ======================= #
#    Create Dataframes    #
# ======================= #
# Load from pickles
# -----------------
DF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Acc.pkl'))
DF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr.pkl'))
DF_Gest = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gest.pkl'))


# ====================== #
#    Extract Features    #
# ====================== #
# Load from pickles
# -----------------
DFF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc.pkl'))
DFF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr.pkl'))
DFF_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes.pkl'))


# ========================== #
#    Select Original User    #
# ========================== #
# l1doqao, 3xhmhs7, 7ksck80, 36z77qn, agmp5h7, w8f2wrs
OriginalUser = 'w8f2wrs'


# ===================================== #
#    Split Original & Attackers Sets    #
# ===================================== #
DFF_Acc_Original, DFF_Acc_Attackers = SplitDFF_OrgAtt(DFF_Acc, OriginalUser)
DFF_Gyr_Original, DFF_Gyr_Attackers = SplitDFF_OrgAtt(DFF_Gyr, OriginalUser)
DFF_Swipes_Original, DFF_Swipes_Attackers = SplitDFF_OrgAtt(DFF_Swipes, OriginalUser)


# ====================== #
#    k-Fold Validation   #
# ====================== #
k = 10
for Fold in tqdm(range(k), desc = '-> Fold'):
    
    
    # ===================================== #
    #    Split Original Train & Test Sets   #
    # ===================================== #
    Split_Rate = 0.2
    DFF_Acc_Original_Trn, DFF_Acc_Original_Tst = SplitRandom(DFF_Acc_Original, Split_Rate)
    DFF_Gyr_Original_Trn, DFF_Gyr_Original_Tst = SplitRandom(DFF_Gyr_Original, Split_Rate)
    DFF_Swipes_Original_Trn, DFF_Swipes_Original_Tst = SplitRandom(DFF_Swipes_Original, Split_Rate)
    
    
    # ================================= #
    #    Split Inputs(X) & Outputs(Y)   #
    # ================================= #
    Features_Acc = ['Mean', 'STD', 'Max', 'Min', 'Range', 'Percentile25', 'Percentile50', 'Percentile75', 'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2', 'MeanFrequency']
    DFF_Acc_Org_Trn_X = DFF_Acc_Original_Trn.loc[:, Features_Acc]
    DFF_Acc_Org_Trn_Y = DFF_Acc_Original_Trn.loc[:, 'Output']
    DFF_Acc_Org_Tst_X = DFF_Acc_Original_Tst.loc[:, Features_Acc]
    DFF_Acc_Org_Tst_Y = DFF_Acc_Original_Tst.loc[:, 'Output']
    DFF_Acc_Att_X = DFF_Acc_Attackers.loc[:, Features_Acc]
    DFF_Acc_Att_Y = DFF_Acc_Attackers.loc[:, 'Output']
    
    Features_Gyr = ['Mean', 'STD', 'Max', 'Min', 'Range', 'Percentile25', 'Percentile50', 'Percentile75', 'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2', 'MeanFrequency']
    DFF_Gyr_Org_Trn_X = DFF_Gyr_Original_Trn.loc[:, Features_Gyr]
    DFF_Gyr_Org_Trn_Y = DFF_Gyr_Original_Trn.loc[:, 'Output']
    DFF_Gyr_Org_Tst_X = DFF_Gyr_Original_Tst.loc[:, Features_Gyr]
    DFF_Gyr_Org_Tst_Y = DFF_Gyr_Original_Tst.loc[:, 'Output']
    DFF_Gyr_Att_X = DFF_Gyr_Attackers.loc[:, Features_Gyr]
    DFF_Gyr_Att_Y = DFF_Gyr_Attackers.loc[:, 'Output']    
    
    Features_Swipes = ['Duration', 'Trace_Length_Horizontal', 'Trace_Length_Vertical', 'Slope', 'Mean_Square_Error', 'Mean_Abs_Error', 'Median_Abs_Error', 'Coef_Determination', 'Mean_X', 'Mean_Y', 'Acceleration_Horizontal', 'Acceleration_Vertical']
    DFF_Swipes_Org_Trn_X = DFF_Swipes_Original_Trn.loc[:, Features_Swipes]
    DFF_Swipes_Org_Trn_Y = DFF_Swipes_Original_Trn.loc[:, 'Output']
    DFF_Swipes_Org_Tst_X = DFF_Swipes_Original_Tst.loc[:, Features_Swipes]
    DFF_Swipes_Org_Tst_Y = DFF_Swipes_Original_Tst.loc[:, 'Output']
    DFF_Swipes_Att_X = DFF_Swipes_Attackers.loc[:, Features_Swipes]
    DFF_Swipes_Att_Y = DFF_Swipes_Attackers.loc[:, 'Output']
    
    
    # =================== #
    #    Normalize Sets   #
    # =================== #
    Scalar_Acc = MinMaxScaler().fit(DFF_Acc_Org_Trn_X)
    DFF_Acc_Org_Trn_X = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_Org_Trn_X), columns = Features_Acc)
    DFF_Acc_Org_Tst_X = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_Org_Tst_X), columns = Features_Acc)
    DFF_Acc_Att_X = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_Att_X), columns = Features_Acc)
    
    Scalar_Gyr = MinMaxScaler().fit(DFF_Gyr_Org_Trn_X)
    DFF_Gyr_Org_Trn_X = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_Org_Trn_X), columns = Features_Gyr)
    DFF_Gyr_Org_Tst_X = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_Org_Tst_X), columns = Features_Gyr)
    DFF_Gyr_Att_X = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_Att_X), columns = Features_Gyr)
    
    """
    Scalar_Swipes = MinMaxScaler().fit(DFF_Swipes_Org_Trn_X)
    DFF_Swipes_Org_Trn_X = pd.DataFrame(Scalar_Swipes.transform(DFF_Swipes_Org_Trn_X), columns = Features_Swipes)
    DFF_Swipes_Org_Tst_X = pd.DataFrame(Scalar_Swipes.transform(DFF_Swipes_Org_Tst_X), columns = Features_Swipes)
    DFF_Swipes_Att_X = pd.DataFrame(Scalar_Swipes.transform(DFF_Swipes_Att_X), columns = Features_Swipes)
    """
    
    
    # ==================== #
    #    Select Features   #
    # ==================== #
    plt.figure(figsize=(8, 8))
    corrplot(DFF_Acc_Org_Trn_X.loc[:, Features_Acc].corr(), size_scale=300)
    
    
    
    
    
    
    
    
    
    
    
    
    


    





