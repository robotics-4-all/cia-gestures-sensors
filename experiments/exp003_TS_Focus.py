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
from s4_Funcs_CreateSets_v000 import SplitDFF_OrgAtt, SplitRandom, SplitRandom_Synced
from s5_Funcs_HandleClassifiers_v000 import AppendUserMetrics, CalculateMeanMetrics, Clf_Train, Clf_GetDecisions, Clf_GetPredictions, Clf_Evaluate
from s5_Class_EvaluationMetrics_v000 import EvaluationMetrics


# ============================ #
#    Directories Parameters    #
# ============================ #
SensData_Path = 'D:\_Projects_\Thesis_ContinuousImplicitAuthentication\Datasets\BrainRun\sensors_data'
GestData_DBName = 'BrainRun_GestureDevicesUsersGames'

results_path = './experiments_results'
Exp = 'exp_003'
TypeExp = 'TS'
ScreenName = 'Focus'

Exp_Save_Path = os.path.join(results_path, Exp + '_' + TypeExp + '_' + ScreenName)
if not os.path.exists(Exp_Save_Path):
    os.makedirs(Exp_Save_Path)


# ======================================== #
#    Explore Data - Select Users & Data    #
# ======================================== #
# LOADS
#valUsers_Sensors_All = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors_All.pkl'))
valUsers_Sensors = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))
#valUsers_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'valUsers_Swipes.pkl'))
DF_Users_Sensrors = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensrors_All.pkl'))
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
DF_Users_Sensrors, DF_Users_Swipes = findUsers_Common(valUsers_Sensors, valUsers_Swipes, Synced_Sensors_Gestures, 1, float('inf'), 1, float('inf'))

# SAVES
valUsers_Sensors_All.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors_All.pkl'))
valUsers_Sensors.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Sensors.pkl'))
valUsers_Swipes.to_pickle(os.path.join(Exp_Save_Path, 'valUsers_Swipes.pkl'))
DF_Users_Sensrors.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensrors_All.pkl'))
DF_Users_Swipes.to_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Swipes_All.pkl'))
"""


# ============================ #
#    Create Data Dataframes    #
# ============================ #
# LOADS
#DF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Acc.pkl'))
#DF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gyr.pkl'))
#DF_Gest = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Gest.pkl'))

"""
DF_Acc, DF_Gyr = Create_DF_Sensors(SensData_Path, ScreenName, DF_Users_Sensrors)
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
#DFF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc.pkl'))
#DFF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr.pkl'))
DFF_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes.pkl'))

"""
# Maybe I can try again other windows & overlaps.
Sensors_Feature = 'Magnitude'
Window = 200
Overlap = 0.9
DFF_Acc, DFF_Gyr = Create_DFF_Sensors(DF_Users_Sensrors, DF_Acc, DF_Gyr, Sensors_Feature, Window, Overlap)

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
EvaluationMetrics_Swipes_U = EvaluationMetrics()

for idx_OrgU in range(len(DF_Users_Sensrors)):
    OriginalUser = DF_Users_Sensrors['User'].values[idx_OrgU]
    print(OriginalUser)

    # ================================ #
    #    Split Original & Attackers    #
    # ================================ #
    DFF_Swipes_Original, DFF_Swipes_Attackers = SplitDFF_OrgAtt(DFF_Swipes, OriginalUser)

    # 10 Fold-Validation
    EvaluationMetrics_Swipes_F = EvaluationMetrics()

    for Fold in tqdm(range(10), desc = '-> Fold'):
        # ================================= #
        #    Split Original Train & Test    #
        # ================================= #
        Split_Rate = 0.2
        DFF_Swipes_Original_Trn, DFF_Swipes_Original_Tst = SplitRandom(DFF_Swipes_Original, Split_Rate)


        # ================================= #
        #    Split Inputs(X) & Outputs(Y)   #
        # ================================= #
        Features_Swipes = ['Trace_Length_Horizontal', 'Trace_Length_Vertical', 'Slope', 'Mean_Square_Error', 'Mean_Abs_Error', 'Median_Abs_Error', 'Coef_Determination', 'Mean_Y', 'Acceleration_Horizontal', 'Acceleration_Vertical']
        DFF_Swipes_Org_Trn_X = DFF_Swipes_Original_Trn.loc[:, Features_Swipes]
        DFF_Swipes_Org_Trn_Y = DFF_Swipes_Original_Trn.loc[:, 'Output']
        DFF_Swipes_Org_Tst_X = DFF_Swipes_Original_Tst.loc[:, Features_Swipes]
        DFF_Swipes_Org_Tst_Y = DFF_Swipes_Original_Tst.loc[:, 'Output']
        DFF_Swipes_Att_X = DFF_Swipes_Attackers.loc[:, Features_Swipes]
        DFF_Swipes_Att_Y = DFF_Swipes_Attackers.loc[:, 'Output']


        # ===================== #
        #    Normalize Swipes   #
        # ===================== #
        Scalar_Swipes = MinMaxScaler().fit(DFF_Swipes_Org_Trn_X.loc[:, Features_Swipes])
        DFF_Swipes_Org_Trn_X = pd.DataFrame(Scalar_Swipes.transform(DFF_Swipes_Org_Trn_X.loc[:, Features_Swipes]), columns = Features_Swipes)
        DFF_Swipes_Org_Tst_X = pd.DataFrame(Scalar_Swipes.transform(DFF_Swipes_Org_Tst_X.loc[:, Features_Swipes]), columns = Features_Swipes)
        DFF_Swipes_Att_X = pd.DataFrame(Scalar_Swipes.transform(DFF_Swipes_Att_X.loc[:, Features_Swipes]), columns = Features_Swipes)


        # ====================== #
        #    Train Classifiers   #
        # ====================== #
        Clfs_Swipes = []
        maxDistance_Clfs_Swipes = []
        Classifier_Swipes = 'OneClassSVM'
        for nu in frange(0.01, 0.3, 0.01):
            for gamma in frange(0.00005, 0.001, 0.00005):
                Parameters = [gamma, nu]
                #Parameters = [0.01, 0.00005]
                Clf, maxDistance = Clf_Train(Classifier_Swipes, Parameters, DFF_Swipes_Org_Trn_X)
                Clfs_Swipes.append(Clf)
                maxDistance_Clfs_Swipes.append(maxDistance)


        # ======================== #
        #    Test Clfs - Org_Tst   #
        # ======================== #
        Decisions_Clfs_Swipes_Org_Tst = []
        for k in range(len(Clfs_Swipes)):
            Decisions_Swipes_Org_Tst = Clf_GetDecisions(Clfs_Swipes[k], DFF_Swipes_Org_Tst_X, maxDistance_Clfs_Swipes[k])
            Decisions_Clfs_Swipes_Org_Tst.append(Decisions_Swipes_Org_Tst)
        Predictions_Swipes_Org_Tst, Decisions_Swipes_Org_Tst = Clf_GetPredictions(Decisions_Clfs_Swipes_Org_Tst)


        # ==================== #
        #    Test Clfs - Att   #
        # ==================== #
        Decisions_Clfs_Swipes_Att = []
        for k in range(len(Clfs_Swipes)):
            Decisions_Swipes_Att = Clf_GetDecisions(Clfs_Swipes[k], DFF_Swipes_Att_X, maxDistance_Clfs_Swipes[k])
            Decisions_Clfs_Swipes_Att.append(Decisions_Swipes_Att)
        Predictions_Swipes_Att, Decisions_Swipes_Att = Clf_GetPredictions(Decisions_Clfs_Swipes_Att)


        # ======================== #
        #    Evaluation - Folds    #
        # ======================== #
        DFF_Swipes_Trn_Y = DFF_Swipes_Org_Trn_Y
        DFF_Swipes_Tst_Y = DFF_Swipes_Org_Tst_Y.append(DFF_Swipes_Att_Y, ignore_index = True)
        Predictions_Swipes = Predictions_Swipes_Org_Tst + Predictions_Swipes_Att
        EvaluationMetrics_Swipes_F = Clf_Evaluate(DFF_Swipes_Trn_Y, DFF_Swipes_Tst_Y, Predictions_Swipes, EvaluationMetrics_Swipes_F)


    # ======================== #
    #    Evaluation - Users    #
    # ======================== #
    EvaluationMetrics_Swipes_U = CalculateMeanMetrics(EvaluationMetrics_Swipes_F, EvaluationMetrics_Swipes_U)

    pre = 3
    SumaryTable = Texttable()
    SumaryTable.header(['User:\n' + OriginalUser, 'TrnOrgSize', 'TstOrgSize', 'TstAttSize', 'Accuracy', 'F1Score', 'FAR', 'FRR'])
    SumaryTable.set_cols_align(['c','c', 'c', 'c', 'c', 'c', 'c', 'c'])
    SumaryTable.set_cols_valign(['m','m', 'm', 'm', 'm', 'm', 'm', 'm'])
    SumaryTable.add_row(['Swipes', EvaluationMetrics_Swipes_U.getTrnOrgSize()[idx_OrgU], EvaluationMetrics_Swipes_U.getTstOrgSize()[idx_OrgU], EvaluationMetrics_Swipes_U.getTstAttSize()[idx_OrgU], str(round(EvaluationMetrics_Swipes_U.getAccuracy()[idx_OrgU]*100,pre))+' %', str(round(EvaluationMetrics_Swipes_U.getF1Score()[idx_OrgU]*100,pre))+' %', str(round(EvaluationMetrics_Swipes_U.getFAR()[idx_OrgU]*100,pre))+' %', str(round(EvaluationMetrics_Swipes_U.getFRR()[idx_OrgU]*100,pre))+' %'])
    print(SumaryTable.draw())


# ======================== #
#    Evaluation - Total    #
# ======================== #
EvaluationMetrics_Swipes_T = EvaluationMetrics()
EvaluationMetrics_Swipes_T = EvaluationMetrics()
EvaluationMetrics_Swipes_T = CalculateMeanMetrics(EvaluationMetrics_Swipes_U, EvaluationMetrics_Swipes_T)

pre = 3
SumaryTable = Texttable()
SumaryTable.header(['TOTAL', 'TrnOrgSize', 'TstOrgSize', 'TstAttSize', 'Accuracy', 'F1Score', 'FAR', 'FRR'])
SumaryTable.set_cols_align(['c','c', 'c', 'c', 'c', 'c', 'c', 'c'])
SumaryTable.set_cols_valign(['m','m', 'm', 'm', 'm', 'm', 'm', 'm'])
SumaryTable.add_row(['Swipes', EvaluationMetrics_Swipes_T.getTrnOrgSize()[0], EvaluationMetrics_Swipes_T.getTstOrgSize()[0], EvaluationMetrics_Swipes_T.getTstAttSize()[0], str(round(EvaluationMetrics_Swipes_T.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Swipes_T.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Swipes_T.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Swipes_T.getFRR()[0]*100,pre))+' %'])
print(SumaryTable.draw())


"""
# ============= #
#    RESULTS    #
# ============= #
Experiment Description:
    - User Selection and Feature extraction is same with exp001_TS_Focus.py
    - Focus
    - Timestamp bases
    - Users selection parametes as shown above
    - 21 users selected
    - Sensors feature extraction with window 200 and overlap 0.9
    - Acc & Gyr are synced split trn - tst
    - Acc Clfs LOFs
    - Gyr Clf LOF
    - Swipes SVMs 
    - Acc and Gyr and Swipes are normilized <----------------------- Normilize swipes
    - Majority voting where needed with propabilities-decisions
    - Classic evaluation - no coeficiens
    
+--------+---------+---------+---------+---------+---------+---------+---------+
| TOTAL  | TrnOrgS | TstOrgS | TstAttS | Accurac | F1Score |   FAR   |   FRR   |
|        |   ize   |   ize   |   ize   |    y    |         |         |         |
+========+=========+=========+=========+=========+=========+=========+=========+
| Swipes | 320.286 | 79.524  | 7996.19 | 53.295  | 3.192 % | 47.015  | 30.639  |
|        |         |         |    0    |    %    |         |    %    |    %    |
+--------+---------+---------+---------+---------+---------+---------+---------+

Καλητερα αποτελέσματα

"""
