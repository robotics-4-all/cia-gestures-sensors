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
from s4_Funcs_CreateSets_v000 import SplitDFF_OrgAtt, SplitRandom, SplitRandom_Synced
from s5_Funcs_HandleClassifiers_v000 import RunML, AppendUserMetrics, CalculateMeanMetrics, Clf_Train, Clf_GetDecisions, Clf_GetPredictions, Clf_Evaluate, frange
from s5_Class_EvaluationMetrics_v000 import EvaluationMetrics


# ======================== #
#    General Parameters    #
# ======================== #
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
saveDir = '__Saves__'
ScreenName = 'Mathisis'
Exp = '_Exp_008'
Exp_Save_Path = os.path.join(saveDir, ScreenName+Exp)


# ======================== #
#    Load Saved Pickles    #
# ======================== #
DF_Users_Sensrors_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensrors_S.pkl'))
DF_Users_Swipes_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Swipes_S.pkl'))
DF_Users_Sensrors_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Sensrors_NS.pkl'))
DF_Users_Swipes_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Swipes_NS.pkl'))

DFF_Acc_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc_S.pkl'))
DFF_Gyr_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr_S.pkl'))
DFF_Acc_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc_NS.pkl'))
DFF_Gyr_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr_NS.pkl'))

DFF_Swipes_S = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes_S.pkl'))
DFF_Swipes_NS = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes_NS.pkl'))


# ========================== #
#    Select Original User    #
# ========================== #
for OriginalUser in DF_Users_Sensrors_S['User']:
    print(OriginalUser)
    
    
    # ===================================== #
    #    Split Original & Attackers Sets    #
    # ===================================== #
    DFF_Acc_S_Original, DFF_Acc_S_Attackers = SplitDFF_OrgAtt(DFF_Acc_S, OriginalUser)
    DFF_Gyr_S_Original, DFF_Gyr_S_Attackers = SplitDFF_OrgAtt(DFF_Gyr_S, OriginalUser)
    DFF_Acc_NS_Original, DFF_Acc_NS_Attackers = SplitDFF_OrgAtt(DFF_Acc_NS, OriginalUser) 
    DFF_Gyr_NS_Original, DFF_Gyr_NS_Attackers = SplitDFF_OrgAtt(DFF_Gyr_NS, OriginalUser)
    DFF_Swipes_S_Original, DFF_Swipes_S_Attackers = SplitDFF_OrgAtt(DFF_Swipes_S, OriginalUser)
    DFF_Swipes_NS_Original, DFF_Swipes_NS_Attackers = SplitDFF_OrgAtt(DFF_Swipes_NS, OriginalUser)
    
    EvaluationMetrics_Acc = EvaluationMetrics()
    EvaluationMetrics_Gyr = EvaluationMetrics()
    EvaluationMetrics_Sensors_UniqueModel = EvaluationMetrics()
    EvaluationMetrics_Sensors_SeperatedModels = EvaluationMetrics()
    EvaluationMetrics_Swipes = EvaluationMetrics()
    
    k = 10
    for Fold in tqdm(range(k), desc = '-> Fold'):
        # ======================================== #
        #    Split Original NS Train & Test Sets   #
        # ======================================== #
        Split_Rate = 0.2        
        DFF_Acc_NS_Original_Trn, DFF_Acc_NS_Original_Tst, DFF_Gyr_NS_Original_Trn, DFF_Gyr_NS_Original_Tst = SplitRandom_Synced(DFF_Acc_NS_Original, DFF_Gyr_NS_Original, Split_Rate)
        DFF_Swipes_NS_Original_Trn, DFF_Swipes_NS_Original_Tst = SplitRandom(DFF_Swipes_NS_Original, Split_Rate)
        
        
        # ================================= #
        #    Split Inputs(X) & Outputs(Y)   #
        # ================================= #
        Features_Acc = ['Mean', 'STD', 'Max', 'Min', 'Range', 'Percentile25', 'Percentile50', 'Percentile75', 'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2']
        DFF_Acc_NS_Org_Trn_X = DFF_Acc_NS_Original_Trn.loc[:, Features_Acc]
        DFF_Acc_NS_Org_Trn_Y = DFF_Acc_NS_Original_Trn.loc[:, 'Output']
        DFF_Acc_NS_Org_Tst_X = DFF_Acc_NS_Original_Tst.loc[:, Features_Acc]
        DFF_Acc_NS_Org_Tst_Y = DFF_Acc_NS_Original_Tst.loc[:, 'Output']
        DFF_Acc_S_Org_X = DFF_Acc_S_Original.loc[:, Features_Acc]
        DFF_Acc_S_Org_Y = DFF_Acc_S_Original.loc[:, 'Output']
        DFF_Acc_NS_Att_X = DFF_Acc_NS_Attackers.loc[:, Features_Acc]
        DFF_Acc_NS_Att_Y = DFF_Acc_NS_Attackers.loc[:, 'Output']
        DFF_Acc_S_Att_X = DFF_Acc_S_Attackers.loc[:, Features_Acc]
        DFF_Acc_S_Att_Y = DFF_Acc_S_Attackers.loc[:, 'Output']
        
        Features_Gyr = ['Mean', 'STD', 'Max', 'Min', 'Range', 'Percentile25', 'Percentile50', 'Percentile75', 'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2']
        DFF_Gyr_NS_Org_Trn_X = DFF_Gyr_NS_Original_Trn.loc[:, Features_Gyr]
        DFF_Gyr_NS_Org_Trn_Y = DFF_Gyr_NS_Original_Trn.loc[:, 'Output']
        DFF_Gyr_NS_Org_Tst_X = DFF_Gyr_NS_Original_Tst.loc[:, Features_Gyr]
        DFF_Gyr_NS_Org_Tst_Y = DFF_Gyr_NS_Original_Tst.loc[:, 'Output']
        DFF_Gyr_S_Org_X = DFF_Gyr_S_Original.loc[:, Features_Gyr]
        DFF_Gyr_S_Org_Y = DFF_Gyr_S_Original.loc[:, 'Output']
        DFF_Gyr_NS_Att_X = DFF_Gyr_NS_Attackers.loc[:, Features_Gyr]
        DFF_Gyr_NS_Att_Y = DFF_Gyr_NS_Attackers.loc[:, 'Output']
        DFF_Gyr_S_Att_X = DFF_Gyr_S_Attackers.loc[:, Features_Gyr]
        DFF_Gyr_S_Att_Y = DFF_Gyr_S_Attackers.loc[:, 'Output']
        
        Features_Swipes = ['Trace_Length_Horizontal', 'Trace_Length_Vertical', 'Slope', 'Mean_Square_Error', 'Mean_Abs_Error', 'Median_Abs_Error', 'Coef_Determination', 'Mean_Y', 'Acceleration_Horizontal', 'Acceleration_Vertical']
        DFF_Swipes_NS_Org_Trn_X = DFF_Swipes_NS_Original_Trn.loc[:, Features_Swipes]
        DFF_Swipes_NS_Org_Trn_Y = DFF_Swipes_NS_Original_Trn.loc[:, 'Output']
        DFF_Swipes_NS_Org_Tst_X = DFF_Swipes_NS_Original_Tst.loc[:, Features_Swipes]
        DFF_Swipes_NS_Org_Tst_Y = DFF_Swipes_NS_Original_Tst.loc[:, 'Output']
        DFF_Swipes_S_Org_X = DFF_Swipes_S_Original.loc[:, Features_Swipes]
        DFF_Swipes_S_Org_Y = DFF_Swipes_S_Original.loc[:, 'Output']
        DFF_Swipes_NS_Att_X = DFF_Swipes_NS_Attackers.loc[:, Features_Swipes]
        DFF_Swipes_NS_Att_Y = DFF_Swipes_NS_Attackers.loc[:, 'Output']
        DFF_Swipes_S_Att_X = DFF_Swipes_S_Attackers.loc[:, Features_Swipes]
        DFF_Swipes_S_Att_Y = DFF_Swipes_S_Attackers.loc[:, 'Output']
        
        
        """
        # ==================== #
        #    Select Features   #
        # ==================== #
        if x == 1:
            corr_Gyr = DFF_Gyr_Org_Trn_X.loc[:, Features_Gyr].corr()
            plt.figure(figsize=(8, 8))
            corrplot(corr_Gyr, size_scale=300)
            x = 0
        
        
        features_corr = pd.DataFrame(columns= ['Feature', 'sum_corr'])
        for i in range(len(Features_Gyr)):
            sum_corr = 0
            for j in range(len(Features_Gyr)):
                sum_corr = sum_corr + abs(corr_Gyr.iloc[i, j])
            df = {'Feature': Features_Gyr[i], 'sum_corr': sum_corr}
            features_corr = features_corr.append(df, ignore_index=True)
        
        # drop 2 max
        features_corr['sum_corr'] = features_corr['sum_corr'].astype(float)
        max_index = features_corr['sum_corr'].idxmax()
        features_corr = features_corr.drop(max_index)
        features_corr = features_corr.reset_index(drop = True)
        max_index = features_corr['sum_corr'].idxmax()
        features_corr = features_corr.drop(max_index)
        features_corr = features_corr.reset_index(drop = True)
        
        Features_Gyr = list(features_corr['Feature'])
        """
        
        
        # ============================= #
        #    Normalize Acc & Gyr Sets   #
        # ============================= #
        Scalar_Acc = MinMaxScaler().fit(DFF_Acc_NS_Org_Trn_X.loc[:, Features_Acc])
        DFF_Acc_NS_Org_Trn_X = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_NS_Org_Trn_X.loc[:, Features_Acc]), columns = Features_Acc)
        DFF_Acc_NS_Org_Tst_X = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_NS_Org_Tst_X.loc[:, Features_Acc]), columns = Features_Acc)
        DFF_Acc_S_Org_X = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_S_Org_X.loc[:, Features_Acc]), columns = Features_Acc)
        DFF_Acc_NS_Att_X = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_NS_Att_X.loc[:, Features_Acc]), columns = Features_Acc)
        DFF_Acc_S_Att_X = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_S_Att_X.loc[:, Features_Acc]), columns = Features_Acc)
        
        Scalar_Gyr = MinMaxScaler().fit(DFF_Gyr_NS_Org_Trn_X.loc[:, Features_Gyr])
        DFF_Gyr_NS_Org_Trn_X = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_NS_Org_Trn_X.loc[:, Features_Gyr]), columns = Features_Gyr)
        DFF_Gyr_NS_Org_Tst_X = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_NS_Org_Tst_X.loc[:, Features_Gyr]), columns = Features_Gyr)
        DFF_Gyr_S_Org_X = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_S_Org_X.loc[:, Features_Gyr]), columns = Features_Gyr)
        DFF_Gyr_NS_Att_X = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_NS_Att_X.loc[:, Features_Gyr]), columns = Features_Gyr)
        DFF_Gyr_S_Att_X = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_S_Att_X.loc[:, Features_Gyr]), columns = Features_Gyr)
        
        
        # ==================================== #
        #    Create Sensors_UniqueModel Sets   #
        # ==================================== #
        DFF_Sensors_UniqueModel_NS_Org_Trn_X = pd.concat([DFF_Acc_NS_Org_Trn_X, DFF_Gyr_NS_Org_Trn_X], axis=1)
        DFF_Sensors_UniqueModel_NS_Org_Trn_Y = DFF_Acc_NS_Org_Trn_Y
        DFF_Sensors_UniqueModel_NS_Org_Tst_X = pd.concat([DFF_Acc_NS_Org_Tst_X, DFF_Gyr_NS_Org_Tst_X], axis=1)
        DFF_Sensors_UniqueModel_NS_Org_Tst_Y = DFF_Acc_NS_Org_Tst_Y
        DFF_Sensors_UniqueModel_S_Org_X = pd.concat([DFF_Acc_S_Org_X, DFF_Gyr_S_Org_X], axis=1)
        DFF_Sensors_UniqueModel_S_Org_Y = DFF_Acc_S_Org_Y
        DFF_Sensors_UniqueModel_NS_Att_X = pd.concat([DFF_Acc_NS_Att_X, DFF_Gyr_NS_Att_X], axis=1)
        DFF_Sensors_UniqueModel_NS_Att_Y = DFF_Acc_NS_Att_Y
        DFF_Sensors_UniqueModel_S_Att_X = pd.concat([DFF_Acc_S_Att_X, DFF_Gyr_S_Att_X], axis=1)
        DFF_Sensors_UniqueModel_S_Att_Y = DFF_Acc_S_Att_Y
        
        
        """
        # ================== #
        #    Find OUtliers   #
        # ================== #
        from sklearn.neighbors import LocalOutlierFactor
        
        inliers = pd.DataFrame(columns = Features_Gyr)
         
        clf = LocalOutlierFactor(n_neighbors=3, contamination=0.1)		# Find inliers and outliers of one user's swipes
        y_pred = clf.fit_predict(DFF_Gyr_Org_Trn_X)
        for i in range(len(y_pred)):
        	if(y_pred[i]==1):
        		inliers = inliers.append(DFF_Gyr_Org_Trn_X.iloc[i], ignore_index=True)
        
        DFF_Gyr_Org_Trn_X = inliers
        DFF_Gyr_Org_Trn_Y = DFF_Gyr_Org_Trn_Y[0:len(inliers)]
        """
        
          
        # ====================== #
        #    Train Classifiers   #
        # ====================== #
        Clfs_Acc = []
        maxDistance_Clfs_Acc = []  
        Classifier_Acc = 'LocalOutlierFactor'
        ns_neighbors = [3, 5, 7]
        for n_neighbors in ns_neighbors:
            Parameters = [n_neighbors]
            Clf, maxDistance = Clf_Train(Classifier_Acc, Parameters, DFF_Acc_NS_Org_Trn_X)
            Clfs_Acc.append(Clf)
            maxDistance_Clfs_Acc.append(maxDistance)
            
        Clfs_Gyr = []
        maxDistance_Clfs_Gyr = []       
        Classifier_Gyr = 'LocalOutlierFactor'
        ns_neighbors = [3]
        for n_neighbors in ns_neighbors:
            Parameters = [n_neighbors]
            Clf, maxDistance = Clf_Train(Classifier_Gyr, Parameters, DFF_Gyr_NS_Org_Trn_X)
            Clfs_Gyr.append(Clf)
            maxDistance_Clfs_Gyr.append(maxDistance)
            
        Clfs_Sensors_UniqueModel = []
        maxDistance_Clfs_Sensors_UniqueModel = []  
        Classifier_Sensors_UniqueModel = 'LocalOutlierFactor'
        ns_neighbors = [3, 7]
        for n_neighbors in ns_neighbors:
            Parameters = [n_neighbors]
            Clf, maxDistance = Clf_Train(Classifier_Sensors_UniqueModel, Parameters, DFF_Sensors_UniqueModel_NS_Org_Trn_X)
            Clfs_Sensors_UniqueModel.append(Clf)
            maxDistance_Clfs_Sensors_UniqueModel.append(maxDistance)
            
        Clfs_Swipes = []
        maxDistance_Clfs_Swipes = []       
        Classifier_Swipes = 'OneClassSVM'
        for nu in frange(0.01, 0.3, 0.01):
            for gamma in frange(0.00005, 0.001, 0.00005):
                Parameters = [gamma, nu]
                Clf, maxDistance = Clf_Train(Classifier_Swipes, Parameters, DFF_Swipes_NS_Org_Trn_X)
                Clfs_Swipes.append(Clf)
                maxDistance_Clfs_Swipes.append(maxDistance)            
            
            
        # =========================== #
        #    Test Clfs - NS_Org_Tst   #
        # =========================== #
        Decisions_Clfs_Acc_NS_Org_Tst = []
        for k in range(len(Clfs_Acc)):
            Decisions_Acc_NS_Org_Tst = Clf_GetDecisions(Clfs_Acc[k], DFF_Acc_NS_Org_Tst_X, maxDistance_Clfs_Acc[k])
            Decisions_Clfs_Acc_NS_Org_Tst.append(Decisions_Acc_NS_Org_Tst)
        Predictions_Acc_NS_Org_Tst, Decisions_Acc_NS_Org_Tst = Clf_GetPredictions(Decisions_Clfs_Acc_NS_Org_Tst)
        
        Decisions_Clfs_Gyr_NS_Org_Tst = []
        for k in range(len(Clfs_Gyr)):
            Decisions_Gyr_NS_Org_Tst = Clf_GetDecisions(Clfs_Gyr[k], DFF_Gyr_NS_Org_Tst_X, maxDistance_Clfs_Gyr[k])
            Decisions_Clfs_Gyr_NS_Org_Tst.append(Decisions_Gyr_NS_Org_Tst)
        Predictions_Gyr_NS_Org_Tst, Decisions_Gyr_NS_Org_Tst = Clf_GetPredictions(Decisions_Clfs_Gyr_NS_Org_Tst)
        
        Decisions_Clfs_Sensors_UniqueModel_NS_Org_Tst = []
        for k in range(len(Clfs_Sensors_UniqueModel)):
            Decisions_Sensors_UniqueModel_NS_Org_Tst = Clf_GetDecisions(Clfs_Sensors_UniqueModel[k], DFF_Sensors_UniqueModel_NS_Org_Tst_X, maxDistance_Clfs_Sensors_UniqueModel[k])
            Decisions_Clfs_Sensors_UniqueModel_NS_Org_Tst.append(Decisions_Sensors_UniqueModel_NS_Org_Tst)
        Predictions_Sensors_UniqueModel_NS_Org_Tst, Decisions_Sensors_UniqueModel_NS_Org_Tst = Clf_GetPredictions(Decisions_Clfs_Sensors_UniqueModel_NS_Org_Tst)
        
        Decisions_Clfs_Sensors_SeperatedModels_NS_Org_Tst = [Decisions_Acc_NS_Org_Tst, Decisions_Gyr_NS_Org_Tst]
        Predictions_Sensors_SeperatedModels_NS_Org_Tst, Decisions_Sensors_SeperatedModels_NS_Org_Tst = Clf_GetPredictions(Decisions_Clfs_Sensors_SeperatedModels_NS_Org_Tst)
        
        Decisions_Clfs_Swipes_NS_Org_Tst = []
        for k in range(len(Clfs_Swipes)):
            Decisions_Swipes_NS_Org_Tst = Clf_GetDecisions(Clfs_Swipes[k], DFF_Swipes_NS_Org_Tst_X, maxDistance_Clfs_Swipes[k])
            Decisions_Clfs_Swipes_NS_Org_Tst.append(Decisions_Swipes_NS_Org_Tst)
        Predictions_Swipes_NS_Org_Tst, Decisions_Swipes_NS_Org_Tst = Clf_GetPredictions(Decisions_Clfs_Swipes_NS_Org_Tst)
        
        
        # ======================= #
        #    Test Clfs - NS_Att   #
        # ======================= #
        Decisions_Clfs_Acc_NS_Att = []
        for k in range(len(Clfs_Acc)):
            Decisions_Acc_NS_Att = Clf_GetDecisions(Clfs_Acc[k], DFF_Acc_NS_Att_X, maxDistance_Clfs_Acc[k])
            Decisions_Clfs_Acc_NS_Att.append(Decisions_Acc_NS_Att)
        Predictions_Acc_NS_Att, Decisions_Acc_NS_Att = Clf_GetPredictions(Decisions_Clfs_Acc_NS_Att)
        
        Decisions_Clfs_Gyr_NS_Att = []
        for k in range(len(Clfs_Gyr)):
            Decisions_Gyr_NS_Att = Clf_GetDecisions(Clfs_Gyr[k], DFF_Gyr_NS_Att_X, maxDistance_Clfs_Gyr[k])
            Decisions_Clfs_Gyr_NS_Att.append(Decisions_Gyr_NS_Att)
        Predictions_Gyr_NS_Att, Decisions_Gyr_NS_Att = Clf_GetPredictions(Decisions_Clfs_Gyr_NS_Att)
        
        Decisions_Clfs_Sensors_UniqueModel_NS_Att = []
        for k in range(len(Clfs_Sensors_UniqueModel)):
            Decisions_Sensors_UniqueModel_NS_Att = Clf_GetDecisions(Clfs_Sensors_UniqueModel[k], DFF_Sensors_UniqueModel_NS_Att_X, maxDistance_Clfs_Sensors_UniqueModel[k])
            Decisions_Clfs_Sensors_UniqueModel_NS_Att.append(Decisions_Sensors_UniqueModel_NS_Att)
        Predictions_Sensors_UniqueModel_NS_Att, Decisions_Sensors_UniqueModel_NS_Att = Clf_GetPredictions(Decisions_Clfs_Sensors_UniqueModel_NS_Att)
        
        Decisions_Clfs_Sensors_SeperatedModels_NS_Att = [Decisions_Acc_NS_Att, Decisions_Gyr_NS_Att]
        Predictions_Sensors_SeperatedModels_NS_Att, Decisions_Sensors_SeperatedModels_NS_Att = Clf_GetPredictions(Decisions_Clfs_Sensors_SeperatedModels_NS_Att)
        
        Decisions_Clfs_Swipes_NS_Att = []
        for k in range(len(Clfs_Swipes)):
            Decisions_Swipes_NS_Att = Clf_GetDecisions(Clfs_Swipes[k], DFF_Swipes_NS_Att_X, maxDistance_Clfs_Swipes[k])
            Decisions_Clfs_Swipes_NS_Att.append(Decisions_Swipes_NS_Att)
        Predictions_Swipes_NS_Att, Decisions_Swipes_NS_Att = Clf_GetPredictions(Decisions_Clfs_Swipes_NS_Att)
        
        
        # ====================== #
        #    Test Clfs - S_Org   #
        # ====================== #
        
        # ====================== #
        #    Test Clfs - S_Att   #
        # ====================== #
        
        
        # =========================== #
        #    Calculate Eval Metrics   #
        # =========================== #
        DFF_Acc_Trn_Y = DFF_Acc_NS_Org_Trn_Y
        DFF_Acc_Tst_Y = DFF_Acc_NS_Org_Tst_Y.append(DFF_Acc_NS_Att_Y, ignore_index = True)
        Predictions_Acc = Predictions_Acc_NS_Org_Tst + Predictions_Acc_NS_Att
        EvaluationMetrics_Acc = Clf_Evaluate(DFF_Acc_Trn_Y, DFF_Acc_Tst_Y, Predictions_Acc, EvaluationMetrics_Acc)

        DFF_Gyr_Trn_Y = DFF_Gyr_NS_Org_Trn_Y
        DFF_Gyr_Tst_Y = DFF_Gyr_NS_Org_Tst_Y.append(DFF_Gyr_NS_Att_Y, ignore_index = True)
        Predictions_Gyr = Predictions_Gyr_NS_Org_Tst + Predictions_Gyr_NS_Att
        EvaluationMetrics_Gyr = Clf_Evaluate(DFF_Gyr_Trn_Y, DFF_Gyr_Tst_Y, Predictions_Gyr, EvaluationMetrics_Gyr)
        
        DFF_Sensors_UniqueModel_Trn_Y = DFF_Sensors_UniqueModel_NS_Org_Trn_Y
        DFF_Sensors_UniqueModel_Tst_Y = DFF_Sensors_UniqueModel_NS_Org_Tst_Y.append(DFF_Sensors_UniqueModel_NS_Att_Y, ignore_index = True)
        Predictions_Sensors_UniqueModel = Predictions_Sensors_UniqueModel_NS_Org_Tst + Predictions_Sensors_UniqueModel_NS_Att
        EvaluationMetrics_Sensors_UniqueModel = Clf_Evaluate(DFF_Sensors_UniqueModel_Trn_Y, DFF_Sensors_UniqueModel_Tst_Y, Predictions_Sensors_UniqueModel, EvaluationMetrics_Sensors_UniqueModel)
        
        Predictions_Sensors_SeperatedModels = Predictions_Sensors_SeperatedModels_NS_Org_Tst + Predictions_Sensors_SeperatedModels_NS_Att
        EvaluationMetrics_Sensors_SeperatedModels = Clf_Evaluate(DFF_Acc_Trn_Y, DFF_Acc_Tst_Y, Predictions_Sensors_SeperatedModels, EvaluationMetrics_Sensors_SeperatedModels)
        
        DFF_Swipes_Trn_Y = DFF_Swipes_NS_Org_Trn_Y
        DFF_Swipes_Tst_Y = DFF_Swipes_NS_Org_Tst_Y.append(DFF_Swipes_NS_Att_Y, ignore_index = True)
        Predictions_Swipes = Predictions_Swipes_NS_Org_Tst + Predictions_Swipes_NS_Att
        EvaluationMetrics_Swipes = Clf_Evaluate(DFF_Swipes_Trn_Y, DFF_Swipes_Tst_Y, Predictions_Swipes, EvaluationMetrics_Swipes)
        
        
    EvaluationMetricsMean_Acc = EvaluationMetrics()
    EvaluationMetricsMean_Acc = CalculateMeanMetrics(EvaluationMetrics_Acc, EvaluationMetricsMean_Acc)
    EvaluationMetrics_Acc = EvaluationMetricsMean_Acc
    
    EvaluationMetricsMean_Gyr = EvaluationMetrics()
    EvaluationMetricsMean_Gyr = CalculateMeanMetrics(EvaluationMetrics_Gyr, EvaluationMetricsMean_Gyr)
    EvaluationMetrics_Gyr = EvaluationMetricsMean_Gyr

    EvaluationMetricsMean_Sensors_UniqueModel = EvaluationMetrics()
    EvaluationMetricsMean_Sensors_UniqueModel = CalculateMeanMetrics(EvaluationMetrics_Sensors_UniqueModel, EvaluationMetricsMean_Sensors_UniqueModel)
    EvaluationMetrics_Sensors_UniqueModel = EvaluationMetricsMean_Sensors_UniqueModel

    EvaluationMetricsMean_Sensors_SeperatedModels = EvaluationMetrics()
    EvaluationMetricsMean_Sensors_SeperatedModels = CalculateMeanMetrics(EvaluationMetrics_Sensors_SeperatedModels, EvaluationMetricsMean_Sensors_SeperatedModels)
    EvaluationMetrics_Sensors_SeperatedModels = EvaluationMetricsMean_Sensors_SeperatedModels

    EvaluationMetricsMean_Swipes = EvaluationMetrics()
    EvaluationMetricsMean_Swipes = CalculateMeanMetrics(EvaluationMetrics_Swipes, EvaluationMetricsMean_Swipes)
    EvaluationMetrics_Swipes = EvaluationMetricsMean_Swipes    
    
    pre = 3
    SumaryTable = Texttable()
    SumaryTable.header(['User:\n' + OriginalUser, 'TrnOrgSize', 'TstOrgSize', 'TstAttSize', 'Mean Accuracy', 'Mean F1Score', 'Mean FAR', 'Mean FRR'])
    SumaryTable.set_cols_align(['c','c', 'c', 'c', 'c', 'c', 'c', 'c'])
    SumaryTable.set_cols_valign(['m','m', 'm', 'm', 'm', 'm', 'm', 'm'])
    SumaryTable.add_row(['Acc', EvaluationMetrics_Acc.getTrnOrgSize()[0], EvaluationMetrics_Acc.getTstOrgSize()[0], EvaluationMetrics_Acc.getTstAttSize()[0], str(round(EvaluationMetrics_Acc.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Acc.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Acc.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Acc.getFRR()[0]*100,pre))+' %'])
    SumaryTable.add_row(['Gyr', EvaluationMetrics_Gyr.getTrnOrgSize()[0], EvaluationMetrics_Gyr.getTstOrgSize()[0], EvaluationMetrics_Gyr.getTstAttSize()[0], str(round(EvaluationMetrics_Gyr.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Gyr.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Gyr.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Gyr.getFRR()[0]*100,pre))+' %'])
    SumaryTable.add_row(['Sensors_UniqueModel', EvaluationMetrics_Sensors_UniqueModel.getTrnOrgSize()[0], EvaluationMetrics_Sensors_UniqueModel.getTstOrgSize()[0], EvaluationMetrics_Sensors_UniqueModel.getTstAttSize()[0], str(round(EvaluationMetrics_Sensors_UniqueModel.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Sensors_UniqueModel.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Sensors_UniqueModel.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Sensors_UniqueModel.getFRR()[0]*100,pre))+' %'])
    SumaryTable.add_row(['Sensors_SeperatedModels', EvaluationMetrics_Sensors_SeperatedModels.getTrnOrgSize()[0], EvaluationMetrics_Sensors_SeperatedModels.getTstOrgSize()[0], EvaluationMetrics_Sensors_SeperatedModels.getTstAttSize()[0], str(round(EvaluationMetrics_Sensors_SeperatedModels.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Sensors_SeperatedModels.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Sensors_SeperatedModels.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Sensors_SeperatedModels.getFRR()[0]*100,pre))+' %'])
    SumaryTable.add_row(['Swipes', EvaluationMetrics_Swipes.getTrnOrgSize()[0], EvaluationMetrics_Swipes.getTstOrgSize()[0], EvaluationMetrics_Swipes.getTstAttSize()[0], str(round(EvaluationMetrics_Swipes.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Swipes.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Swipes.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Swipes.getFRR()[0]*100,pre))+' %'])
    print(SumaryTable.draw()) 
