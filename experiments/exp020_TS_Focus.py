# ============= #
#    Imports    #
# ============= #
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from heatmap import corrplot
from texttable import Texttable
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from s0_Funcs_Util_v000 import frange
from s1_Funcs_ExploreData_v001 import findUsers_Sensors, findUsers_Swipes, findUsers_Common #TIMESTAMP BASED
from s2_Funcs_CreateDataFrames_v001 import Create_DF_Sensors, Create_DF_Gestures #TIMESTAMP BASED
from s3_Funcs_ExtractFeatures_v002 import Create_DFF_Sensors, Create_DFF_Swipes #TIMESTAMP BASED
from s4_Funcs_CreateSets_v001 import CreateUsersDFFsList, SplitDFF_OrgAtt, SplitRandom, SplitRandom_Synced
from s5_Funcs_HandleClassifiers_v003 import CalculateMeanMetrics, Clf_Train, Clf_GetDecisions, Clf_GetPredictions, Clf_GetTotalPredictions, Clf_Evaluate
from s5_Class_EvaluationMetrics_v001 import EvaluationMetrics


# ============================ #
#    Directories Parameters    #
# ============================ #
SensData_Path = 'D:\_Projects_\Thesis_ContinuousImplicitAuthentication\Datasets\BrainRun\sensors_data'
GestData_DBName = 'BrainRun_GestureDevicesUsersGames'

results_path = './experiments_results'
Exp = 'exp_020'
TypeExp = 'TS'
ScreenName = 'Focus'

Exp_Save_Path = os.path.join(results_path, Exp + '_' + TypeExp + '_' + ScreenName)
if not os.path.exists(Exp_Save_Path):
    os.makedirs(Exp_Save_Path)


# ======================================== #
#    Explore Data - Select Users & Data    #
# ======================================== #
# LOADS
valUsers_Sensors_All = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors_All.pkl'))
valUsers_Sensors = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))
valUsers_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Swipes.pkl'))
DF_Users_Sensors = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensors_All.pkl'))
DF_Users_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Swipes_All.pkl'))

"""
# Find Users with Synced Sensors Data.
# Maybe it it does not matter if the sensors are not synced. I must question this and write the script.
minData_TS = 200
valUsers_Sensors_All = findUsers_Sensors(SensData_Path, ScreenName, minData_TS, 1, float('inf'))
minData_U = 5000
maxData_U = 30000
valUsers_Sensors = valUsers_Sensors_All.loc[(valUsers_Sensors_All['AccSize_U'] >= minData_U) & (valUsers_Sensors_All['AccSize_U'] <= maxData_U)]
valUsers_Sensors = valUsers_Sensors.reset_index(drop=True)

# Find Users with 'valid' Swipes
maxDeviceWidth = 600
maxDeviceHeight = 1000
Fake_Swipe_Limit = 30
minData_Gesture = 4
maxData_Gesture = 10
minGesture_User = 1
valUsers_Swipes = findUsers_Swipes(GestData_DBName, ScreenName, maxDeviceWidth, maxDeviceHeight, Fake_Swipe_Limit, minData_Gesture, maxData_Gesture, minGesture_User)

# Select Users with Synced Sensors data and 'valid' Swipes.
# Thera are not a lot synced sensors and synced gestures data.
Synced_Sensors_Gestures = False
DF_Users_Sensors, DF_Users_Swipes = findUsers_Common(valUsers_Sensors, valUsers_Swipes, Synced_Sensors_Gestures, 1, float('inf'), 1, float('inf'))

# SAVES
valUsers_Sensors_All.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors_All.pkl'))
valUsers_Sensors.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))
valUsers_Swipes.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Swipes.pkl'))
DF_Users_Sensors.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensors_All.pkl'))
DF_Users_Swipes.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Swipes_All.pkl'))
"""


# ============================ #
#    Create Data Dataframes    #
# ============================ #
# LOADS
DF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Acc.pkl'))
DF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr.pkl'))
DF_Gest = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gest.pkl'))

"""
DF_Acc, DF_Gyr = Create_DF_Sensors(SensData_Path, ScreenName, DF_Users_Sensors)
DF_Gest = Create_DF_Gestures(GestData_DBName, DF_Users_Swipes)

# SAVES
DF_Acc.to_pickle(os.path.join(Exp_Save_Path, 'DF_Acc.pkl'))
DF_Gyr.to_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr.pkl'))
DF_Gest.to_pickle(os.path.join(Exp_Save_Path, 'DF_Gest.pkl'))
"""


# ====================== #
#    Extract Features    #
# ====================== #
# LOADS
DFF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc.pkl'))
DFF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr.pkl'))
DFF_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes.pkl'))

"""
# Maybe I can try again other windows & overlaps.
Sensors_Feature = 'Magnitude'
Window = 200
Overlap = 0.9
DFF_Acc, DFF_Gyr = Create_DFF_Sensors(DF_Users_Sensors, DF_Acc, DF_Gyr, Sensors_Feature, Window, Overlap)

Normalize_Swipes = True
DFF_Swipes = Create_DFF_Swipes(DF_Gest, Normalize_Swipes)

# SAVES
DFF_Acc.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc.pkl'))
DFF_Gyr.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr.pkl'))
DFF_Swipes.to_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes.pkl'))
"""


# ====================== #
#    Start Experiment    #
# ====================== #
EvaluationMetrics_Acc_U = EvaluationMetrics()
EvaluationMetrics_Gyr_U = EvaluationMetrics()
EvaluationMetrics_Swipes_U = EvaluationMetrics()

for idx_Org in range(len(DF_Users_Sensors)):

    # ====================================== #
    #    Define Original User & Attackers    #
    # ====================================== #
    OriginalUser = DF_Users_Sensors['User'].values[idx_Org]

    Attackers = []
    for u in list(DF_Users_Sensors['User'].values):
        if u != OriginalUser:
            Attackers.append(u)


    # ================= #
    #    Define DFFs    #
    # ================= #
    DFF_Acc_Org = DFF_Acc.loc[DFF_Acc['User'] == OriginalUser]
    DFF_Acc_Org = DFF_Acc_Org.reset_index(drop = True)
    DFF_Gyr_Org = DFF_Gyr.loc[DFF_Gyr['User'] == OriginalUser]
    DFF_Gyr_Org = DFF_Gyr_Org.reset_index(drop = True)
    DFF_Swipes_Org = DFF_Swipes.loc[DFF_Swipes['User'] == OriginalUser]
    DFF_Swipes_Org = DFF_Swipes_Org.reset_index(drop = True)

    DFF_Acc_Atts = CreateUsersDFFsList(Attackers, DFF_Acc)
    DFF_Gyr_Atts = CreateUsersDFFsList(Attackers, DFF_Gyr)
    DFF_Swipes_Atts = CreateUsersDFFsList(Attackers, DFF_Swipes)


    # 10 Fold-Validation
    EvaluationMetrics_Acc_F = EvaluationMetrics()
    EvaluationMetrics_Gyr_F = EvaluationMetrics()
    EvaluationMetrics_Swipes_F = EvaluationMetrics()

    for Fold in tqdm(range(10), desc = '-> Fold'):
        # ================================= #
        #    Split Original Train & Test    #
        # ================================= #
        Split_Rate = 0.2
        DFF_Acc_Org_Trn, DFF_Acc_Org_Tst = SplitRandom(DFF_Acc_Org, Split_Rate)
        DFF_Gyr_Org_Trn, DFF_Gyr_Org_Tst = SplitRandom(DFF_Gyr_Org, Split_Rate)
        DFF_Swipes_Org_Trn, DFF_Swipes_Org_Tst = SplitRandom(DFF_Swipes_Org, Split_Rate)


        # =========================== #
        #    Select Final Features    #
        # =========================== #
        Features_Acc = ['Mean', 'STD', 'Max', 'Min', 'Range', 'Percentile25', 'Percentile50', 'Percentile75', 'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2']
        DFF_Acc_Org_Trn = DFF_Acc_Org_Trn.loc[:, Features_Acc]
        DFF_Acc_Org_Tst = DFF_Acc_Org_Tst.loc[:, Features_Acc]
        for idx_Att in range(len(DFF_Acc_Atts)):
            DFF_Acc_Atts[idx_Att] = DFF_Acc_Atts[idx_Att].loc[:, Features_Acc]

        Features_Gyr = ['Mean', 'STD', 'Max', 'Min', 'Range', 'Percentile25', 'Percentile50', 'Percentile75', 'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2']
        DFF_Gyr_Org_Trn = DFF_Gyr_Org_Trn.loc[:, Features_Gyr]
        DFF_Gyr_Org_Tst = DFF_Gyr_Org_Tst.loc[:, Features_Gyr]
        for idx_Att in range(len(DFF_Gyr_Atts)):
            DFF_Gyr_Atts[idx_Att] = DFF_Gyr_Atts[idx_Att].loc[:, Features_Gyr]

        Features_Swipes = ['Trace_Length_Horizontal', 'Trace_Length_Vertical', 'Slope', 'Mean_Square_Error', 'Mean_Abs_Error', 'Median_Abs_Error', 'Coef_Determination', 'Mean_Y', 'Acceleration_Horizontal', 'Acceleration_Vertical']
        DFF_Swipes_Org_Trn = DFF_Swipes_Org_Trn.loc[:, Features_Swipes]
        DFF_Swipes_Org_Tst = DFF_Swipes_Org_Tst.loc[:, Features_Swipes]
        for idx_Att in range(len(DFF_Swipes_Atts)):
            DFF_Swipes_Atts[idx_Att] = DFF_Swipes_Atts[idx_Att].loc[:, Features_Swipes]


        # ====================================== #
        #    Normalize Acc & Gyr & Swipes Sets   #
        # ====================================== #
        Scalar_Acc = MinMaxScaler().fit(DFF_Acc_Org_Trn)
        DFF_Acc_Org_Trn = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_Org_Trn), columns = Features_Acc)
        DFF_Acc_Org_Tst = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_Org_Tst), columns = Features_Acc)
        for idx_Att in range(len(DFF_Acc_Atts)):
            DFF_Acc_Atts[idx_Att] = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_Atts[idx_Att]), columns = Features_Acc)

        Scalar_Gyr = MinMaxScaler().fit(DFF_Gyr_Org_Trn)
        DFF_Gyr_Org_Trn = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_Org_Trn), columns = Features_Gyr)
        DFF_Gyr_Org_Tst = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_Org_Tst), columns = Features_Gyr)
        for idx_Att in range(len(DFF_Gyr_Atts)):
            DFF_Gyr_Atts[idx_Att] = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_Atts[idx_Att]), columns = Features_Gyr)

        Scalar_Swipes = MinMaxScaler().fit(DFF_Swipes_Org_Trn)
        DFF_Swipes_Org_Trn = pd.DataFrame(Scalar_Swipes.transform(DFF_Swipes_Org_Trn), columns = Features_Swipes)
        DFF_Swipes_Org_Tst = pd.DataFrame(Scalar_Swipes.transform(DFF_Swipes_Org_Tst), columns = Features_Swipes)
        for idx_Att in range(len(DFF_Swipes_Atts)):
            DFF_Swipes_Atts[idx_Att] = pd.DataFrame(Scalar_Swipes.transform(DFF_Swipes_Atts[idx_Att]), columns = Features_Swipes)


        # ====================== #
        #    Train Classifiers   #
        # ====================== #
        Clfs_Acc = []
        maxDistance_Clfs_Acc = []
        Classifier_Acc = 'LocalOutlierFactor'
        ns_neighbors = [3, 5, 7]
        for n_neighbors in ns_neighbors:
            Parameters = [n_neighbors]
            Clf, maxDistance = Clf_Train(Classifier_Acc, Parameters, DFF_Acc_Org_Trn)
            Clfs_Acc.append(Clf)
            maxDistance_Clfs_Acc.append(maxDistance)

        Clfs_Gyr = []
        maxDistance_Clfs_Gyr = []
        Classifier_Gyr = 'LocalOutlierFactor'
        ns_neighbors = [3, 5, 7]
        for n_neighbors in ns_neighbors:
            Parameters = [n_neighbors]
            Clf, maxDistance = Clf_Train(Classifier_Gyr, Parameters, DFF_Gyr_Org_Trn)
            Clfs_Gyr.append(Clf)
            maxDistance_Clfs_Gyr.append(maxDistance)

        Clfs_Swipes = []
        maxDistance_Clfs_Swipes = []
        Classifier_Swipes = 'OneClassSVM'
        for nu in frange(0.01, 0.3, 0.01):
            for gamma in frange(5.00, 10.00, 0.05):
                Parameters = [gamma, nu]
                Clf, maxDistance = Clf_Train(Classifier_Swipes, Parameters, DFF_Swipes_Org_Trn)
                Clfs_Swipes.append(Clf)
                maxDistance_Clfs_Swipes.append(maxDistance)


        # ======================== #
        #    Test Clfs - Org_Tst   #
        # ======================== #
        Predictions_Clfs_Acc_Org_Tst = []
        for k in range(len(Clfs_Acc)):
            Predictions_Acc_Org_Tst = Clf_GetPredictions(Clfs_Acc[k], DFF_Acc_Org_Tst)
            Predictions_Clfs_Acc_Org_Tst.append(Predictions_Acc_Org_Tst)
        Predictions_Acc_Org_Tst = Clf_GetTotalPredictions(Predictions_Clfs_Acc_Org_Tst)

        Predictions_Clfs_Gyr_Org_Tst = []
        for k in range(len(Clfs_Gyr)):
            Predictions_Gyr_Org_Tst = Clf_GetPredictions(Clfs_Gyr[k], DFF_Gyr_Org_Tst)
            Predictions_Clfs_Gyr_Org_Tst.append(Predictions_Gyr_Org_Tst)
        Predictions_Gyr_Org_Tst = Clf_GetTotalPredictions(Predictions_Clfs_Gyr_Org_Tst)

        Predictions_Clfs_Swipes_Org_Tst = []
        for k in range(len(Clfs_Swipes)):
            Predictions_Swipes_Org_Tst = Clf_GetPredictions(Clfs_Swipes[k], DFF_Swipes_Org_Tst)
            Predictions_Clfs_Swipes_Org_Tst.append(Predictions_Swipes_Org_Tst)
        Predictions_Swipes_Org_Tst = Clf_GetTotalPredictions(Predictions_Clfs_Swipes_Org_Tst)


        # ==================== #
        #    Test Clfs - Att   #
        # ==================== #
        Predictions_Acc_Atts = []
        for idx_Att in range(len(DFF_Acc_Atts)):
            DFF_Acc_Att = DFF_Acc_Atts[idx_Att]
            Predictions_Clfs_Acc_Att = []
            for k in range(len(Clfs_Acc)):
                Predictions_Acc_Att = Clf_GetPredictions(Clfs_Acc[k], DFF_Acc_Att)
                Predictions_Clfs_Acc_Att.append(Predictions_Acc_Att)
            Predictions_Acc_Att = Clf_GetTotalPredictions(Predictions_Clfs_Acc_Att)
            Predictions_Acc_Atts.append(Predictions_Acc_Att)

        Predictions_Gyr_Atts = []
        for idx_Att in range(len(DFF_Gyr_Atts)):
            DFF_Gyr_Att = DFF_Gyr_Atts[idx_Att]
            Predictions_Clfs_Gyr_Att = []
            for k in range(len(Clfs_Gyr)):
                Predictions_Gyr_Att = Clf_GetPredictions(Clfs_Gyr[k], DFF_Gyr_Att)
                Predictions_Clfs_Gyr_Att.append(Predictions_Gyr_Att)
            Predictions_Gyr_Att = Clf_GetTotalPredictions(Predictions_Clfs_Gyr_Att)
            Predictions_Gyr_Atts.append(Predictions_Gyr_Att)

        Predictions_Swipes_Atts = []
        for idx_Att in range(len(DFF_Swipes_Atts)):
            DFF_Swipes_Att = DFF_Swipes_Atts[idx_Att]
            Predictions_Clfs_Swipes_Att = []
            for k in range(len(Clfs_Swipes)):
                Predictions_Swipes_Att = Clf_GetPredictions(Clfs_Swipes[k], DFF_Swipes_Att)
                Predictions_Clfs_Swipes_Att.append(Predictions_Swipes_Att)
            Predictions_Swipes_Att = Clf_GetTotalPredictions(Predictions_Clfs_Swipes_Att)
            Predictions_Swipes_Atts.append(Predictions_Swipes_Att)


        # ======================== #
        #    Evaluation - Folds    #
        # ======================== #
        EvaluationMetrics_Acc_F = Clf_Evaluate(DFF_Acc_Org_Trn, Predictions_Acc_Org_Tst, Predictions_Acc_Atts, EvaluationMetrics_Acc_F)
        EvaluationMetrics_Gyr_F = Clf_Evaluate(DFF_Gyr_Org_Trn, Predictions_Gyr_Org_Tst, Predictions_Gyr_Atts, EvaluationMetrics_Gyr_F)
        EvaluationMetrics_Swipes_F = Clf_Evaluate(DFF_Swipes_Org_Trn, Predictions_Swipes_Org_Tst, Predictions_Swipes_Atts, EvaluationMetrics_Swipes_F)


    # ======================== #
    #    Evaluation - Users    #
    # ======================== #
    EvaluationMetrics_Acc_U = CalculateMeanMetrics(EvaluationMetrics_Acc_F, EvaluationMetrics_Acc_U)
    EvaluationMetrics_Gyr_U = CalculateMeanMetrics(EvaluationMetrics_Gyr_F, EvaluationMetrics_Gyr_U)
    EvaluationMetrics_Swipes_U = CalculateMeanMetrics(EvaluationMetrics_Swipes_F, EvaluationMetrics_Swipes_U)

    pre = 3
    SumaryTable = Texttable()
    SumaryTable.set_max_width(0)
    SumaryTable.header(['User:\n' + OriginalUser, 'OrgTrnSize', 'OrgTstSize', 'AttNum', 'Att_TotalSize', 'Att_AvgSize', 'FRR', 'FRR_Conf', 'FAR_Total', 'FAR_Avg', 'Num_Of_Unlocks', 'Num_Of_Accepted_Avg'])
    SumaryTable.set_cols_align(['c','c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c'])
    SumaryTable.set_cols_valign(['m','m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'])
    SumaryTable.add_row(['Acc',
                         str(round(EvaluationMetrics_Acc_U.getOrgTrnSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Acc_U.getOrgTrnSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Acc_U.getOrgTstSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Acc_U.getOrgTstSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Acc_U.getAttNum()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Acc_U.getAttNum_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Acc_U.getAtt_TotalSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Acc_U.getAtt_TotalSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Acc_U.getAtt_AvgSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Acc_U.getAtt_AvgSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Acc_U.getFRR()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Acc_U.getFRR_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Acc_U.getFRR_Conf()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Acc_U.getFRR_Conf_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Acc_U.getFAR_Total()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Acc_U.getFAR_Total_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Acc_U.getFAR_Avg()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Acc_U.getFAR_Avg_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Acc_U.getNum_Of_Unlocks()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Acc_U.getNum_Of_Unlocks_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Acc_U.getNum_Of_Accepted_Avg()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Acc_U.getNum_Of_Accepted_Avg_Std()[idx_Org], pre)) + ')'])
    SumaryTable.add_row(['Gyr',
                         str(round(EvaluationMetrics_Gyr_U.getOrgTrnSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_U.getOrgTrnSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Gyr_U.getOrgTstSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_U.getOrgTstSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Gyr_U.getAttNum()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_U.getAttNum_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Gyr_U.getAtt_TotalSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_U.getAtt_TotalSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Gyr_U.getAtt_AvgSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_U.getAtt_AvgSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Gyr_U.getFRR()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Gyr_U.getFRR_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Gyr_U.getFRR_Conf()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Gyr_U.getFRR_Conf_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Gyr_U.getFAR_Total()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Gyr_U.getFAR_Total_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Gyr_U.getFAR_Avg()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Gyr_U.getFAR_Avg_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Gyr_U.getNum_Of_Unlocks()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_U.getNum_Of_Unlocks_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Gyr_U.getNum_Of_Accepted_Avg()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_U.getNum_Of_Accepted_Avg_Std()[idx_Org], pre)) + ')'])
    SumaryTable.add_row(['Swipes',
                         str(round(EvaluationMetrics_Swipes_U.getOrgTrnSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_U.getOrgTrnSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Swipes_U.getOrgTstSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_U.getOrgTstSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Swipes_U.getAttNum()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_U.getAttNum_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Swipes_U.getAtt_TotalSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_U.getAtt_TotalSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Swipes_U.getAtt_AvgSize()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_U.getAtt_AvgSize_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Swipes_U.getFRR()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Swipes_U.getFRR_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Swipes_U.getFRR_Conf()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Swipes_U.getFRR_Conf_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Swipes_U.getFAR_Total()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Swipes_U.getFAR_Total_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Swipes_U.getFAR_Avg()[idx_Org]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Swipes_U.getFAR_Avg_Std()[idx_Org]*100, pre)) + ' %)',
                         str(round(EvaluationMetrics_Swipes_U.getNum_Of_Unlocks()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_U.getNum_Of_Unlocks_Std()[idx_Org], pre)) + ')',
                         str(round(EvaluationMetrics_Swipes_U.getNum_Of_Accepted_Avg()[idx_Org], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_U.getNum_Of_Accepted_Avg_Std()[idx_Org], pre)) + ')'])
    print(SumaryTable.draw())


# ======================== #
#    Evaluation - Total    #
# ======================== #
EvaluationMetrics_Acc_T = EvaluationMetrics()
EvaluationMetrics_Acc_T = CalculateMeanMetrics(EvaluationMetrics_Acc_U, EvaluationMetrics_Acc_T)
EvaluationMetrics_Gyr_T = EvaluationMetrics()
EvaluationMetrics_Gyr_T = CalculateMeanMetrics(EvaluationMetrics_Gyr_U, EvaluationMetrics_Gyr_T)
EvaluationMetrics_Swipes_T = EvaluationMetrics()
EvaluationMetrics_Swipes_T = CalculateMeanMetrics(EvaluationMetrics_Swipes_U, EvaluationMetrics_Swipes_T)

pre = 3
SumaryTable = Texttable()
SumaryTable.set_max_width(0)
SumaryTable.header([str(len(DF_Users_Sensors)) + ' Users\n' + ScreenName, 'OrgTrnSize', 'OrgTstSize', 'AttNum', 'Att_TotalSize', 'Att_AvgSize', 'FRR', 'FRR_Conf', 'FAR_Total', 'FAR_Avg', 'Num_Of_Unlocks', 'Num_Of_Accepted_Avg'])
SumaryTable.set_cols_align(['c','c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c'])
SumaryTable.set_cols_valign(['m','m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'])
SumaryTable.add_row(['Acc',
                     str(round(EvaluationMetrics_Acc_T.getOrgTrnSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Acc_T.getOrgTrnSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Acc_T.getOrgTstSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Acc_T.getOrgTstSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Acc_T.getAttNum()[0], pre)) + ' (' + str(round(EvaluationMetrics_Acc_T.getAttNum_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Acc_T.getAtt_TotalSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Acc_T.getAtt_TotalSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Acc_T.getAtt_AvgSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Acc_T.getAtt_AvgSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Acc_T.getFRR()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Acc_T.getFRR_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Acc_T.getFRR_Conf()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Acc_T.getFRR_Conf_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Acc_T.getFAR_Total()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Acc_T.getFAR_Total_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Acc_T.getFAR_Avg()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Acc_T.getFAR_Avg_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Acc_T.getNum_Of_Unlocks()[0], pre)) + ' (' + str(round(EvaluationMetrics_Acc_T.getNum_Of_Unlocks_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Acc_T.getNum_Of_Accepted_Avg()[0], pre)) + ' (' + str(round(EvaluationMetrics_Acc_T.getNum_Of_Accepted_Avg_Std()[0], pre)) + ')'])
SumaryTable.add_row(['Gyr',
                     str(round(EvaluationMetrics_Gyr_T.getOrgTrnSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_T.getOrgTrnSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Gyr_T.getOrgTstSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_T.getOrgTstSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Gyr_T.getAttNum()[0], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_T.getAttNum_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Gyr_T.getAtt_TotalSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_T.getAtt_TotalSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Gyr_T.getAtt_AvgSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_T.getAtt_AvgSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Gyr_T.getFRR()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Gyr_T.getFRR_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Gyr_T.getFRR_Conf()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Gyr_T.getFRR_Conf_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Gyr_T.getFAR_Total()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Gyr_T.getFAR_Total_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Gyr_T.getFAR_Avg()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Gyr_T.getFAR_Avg_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Gyr_T.getNum_Of_Unlocks()[0], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_T.getNum_Of_Unlocks_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Gyr_T.getNum_Of_Accepted_Avg()[0], pre)) + ' (' + str(round(EvaluationMetrics_Gyr_T.getNum_Of_Accepted_Avg_Std()[0], pre)) + ')'])
SumaryTable.add_row(['Swipes',
                     str(round(EvaluationMetrics_Swipes_T.getOrgTrnSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_T.getOrgTrnSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Swipes_T.getOrgTstSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_T.getOrgTstSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Swipes_T.getAttNum()[0], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_T.getAttNum_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Swipes_T.getAtt_TotalSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_T.getAtt_TotalSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Swipes_T.getAtt_AvgSize()[0], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_T.getAtt_AvgSize_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Swipes_T.getFRR()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Swipes_T.getFRR_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Swipes_T.getFRR_Conf()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Swipes_T.getFRR_Conf_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Swipes_T.getFAR_Total()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Swipes_T.getFAR_Total_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Swipes_T.getFAR_Avg()[0]*100, pre)) + ' %' + ' (' + str(round(EvaluationMetrics_Swipes_T.getFAR_Avg_Std()[0]*100, pre)) + ' %)',
                     str(round(EvaluationMetrics_Swipes_T.getNum_Of_Unlocks()[0], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_T.getNum_Of_Unlocks_Std()[0], pre)) + ')',
                     str(round(EvaluationMetrics_Swipes_T.getNum_Of_Accepted_Avg()[0], pre)) + ' (' + str(round(EvaluationMetrics_Swipes_T.getNum_Of_Accepted_Avg_Std()[0], pre)) + ')'])
print(SumaryTable.draw())


"""
# ============= #
#    RESULTS    #
# ============= #
Experiment Description:
    - User Selection and Feature extraction is same with exp000_TS_Mathisis.py
    - Focus
    - Timestamp bases
    - Users selection parametes as shown above
    - 24 users selected
    - 10 fold cross validation
    - Sensors feature extraction with window 200 and overlap 0.9
    - Acc & Gyr are NOT synced split <-----------------------------------------------------------
    - Acc Clfs LOFs
    - Gyr Clf LOF
    - Swipes SVMs
    - Acc and Gyr are normilized and the swipes <-------------------------------------------------
    - Majority voting where needed with precitions and with clf.predict !!!! <--------------------
    - Evaluation with confidence level !!!!!!!!!!! <--------------------
    
+----------+------------------+-----------------+------------+--------------------+-----------------+---------------------+-------------------+-------------------+-------------------+----------------+---------------------+
| 21 Users |    OrgTrnSize    |   OrgTstSize    |   AttNum   |   Att_TotalSize    |   Att_AvgSize   |         FRR         |     FRR_Conf      |     FAR_Total     |      FAR_Avg      | Num_Of_Unlocks | Num_Of_Accepted_Avg |
|  Focus   |                  |                 |            |                    |                 |                     |                   |                   |                   |                |                     |
+==========+==================+=================+============+====================+=================+=====================+===================+===================+===================+================+=====================+
|   Acc    | 217.714 (93.352) | 53.857 (23.406) | 20.0 (0.0) | 5431.429 (116.756) | 271.571 (5.838) |  7.489 % (3.611 %)  | 0.085 % (0.161 %) | 2.06 % (1.433 %)  | 2.084 % (1.447 %) | 0.043 (0.075)  |    1.672 (0.699)    |
+----------+------------------+-----------------+------------+--------------------+-----------------+---------------------+-------------------+-------------------+-------------------+----------------+---------------------+
|   Gyr    | 217.714 (93.352) | 53.857 (23.406) | 20.0 (0.0) | 5431.429 (116.756) | 271.571 (5.838) |  7.408 % (2.831 %)  | 0.072 % (0.203 %) | 3.765 % (1.491 %) | 3.754 % (1.518 %) | 0.024 (0.062)  |    2.124 (0.833)    |
+----------+------------------+-----------------+------------+--------------------+-----------------+---------------------+-------------------+-------------------+-------------------+----------------+---------------------+
|  Swipes  | 320.286 (181.04) | 79.524 (45.305) | 20.0 (0.0) | 7996.19 (226.345)  | 399.81 (11.317) | 31.265 % (11.961 %) | 4.924 % (5.381 %) | 2.455 % (1.956 %) | 2.518 % (1.952 %) | 2.286 (1.071)  |     1.542 (0.9)     |
+----------+------------------+-----------------+------------+--------------------+-----------------+---------------------+-------------------+-------------------+-------------------+----------------+---------------------+
"""
