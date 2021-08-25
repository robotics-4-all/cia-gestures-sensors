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
from s4_Funcs_CreateSets_v000 import SplitDFF_OrgAtt, SplitRandom
from s5_Funcs_HandleClassifiers_v000 import RunML, AppendUserMetrics, CalculateMeanMetrics, Clf_Train, Clf_GetDecisions, Clf_GetPredictions, Clf_Evaluate, frange
from s5_Class_EvaluationMetrics_v000 import EvaluationMetrics


# ======================== #
#    General Parameters    #
# ======================== #
SensData_Path = 'C:\\Users\\John Doe\\Desktop\\CIA\\_CODE_DATASET\\sensors_data\\sensors'
GestData_DBName = 'my_data'
saveDir = '__Saves__'
ScreenName = 'Mathisis'
Exp = '_Exp_007'
Exp_Save_Path = os.path.join(saveDir, ScreenName+Exp)


# ======================== #
#    Load Saved Pickles    #
# ======================== #
DF_Users_Final = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Final.pkl'))
DFF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc.pkl'))
DFF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr.pkl'))


# ========================== #
#    Select Original User    #
# ========================== #
for OriginalUser in DF_Users_Final['User']:
    print(OriginalUser)
    

    # ===================================== #
    #    Split Original & Attackers Sets    #
    # ===================================== #
    DFF_Gyr_Original, DFF_Gyr_Attackers = SplitDFF_OrgAtt(DFF_Gyr, OriginalUser)  
    
    
    EvaluationMetrics_Gyr = EvaluationMetrics()
    k = 10    
    x = 1
    for Fold in tqdm(range(k), desc = '-> Fold'):
    
            
        # ===================================== #
        #    Split Original Train & Test Sets   #
        # ===================================== #
        Split_Rate = 0.2
        DFF_Gyr_Original_Trn, DFF_Gyr_Original_Tst = SplitRandom(DFF_Gyr_Original, Split_Rate)
        
        
        # ================================= #
        #    Split Inputs(X) & Outputs(Y)   #
        # ================================= #
        Features_Gyr = ['Mean', 'STD', 'Max', 'Min', 'Range', 'Percentile25', 'Percentile50', 'Percentile75', 'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2'] #, 'MeanFrequency']
        DFF_Gyr_Org_Trn_X = DFF_Gyr_Original_Trn.loc[:, Features_Gyr]
        DFF_Gyr_Org_Trn_Y = DFF_Gyr_Original_Trn.loc[:, 'Output']
        DFF_Gyr_Org_Tst_X = DFF_Gyr_Original_Tst.loc[:, Features_Gyr]
        DFF_Gyr_Org_Tst_Y = DFF_Gyr_Original_Tst.loc[:, 'Output']
        DFF_Gyr_Att_X = DFF_Gyr_Attackers.loc[:, Features_Gyr]
        DFF_Gyr_Att_Y = DFF_Gyr_Attackers.loc[:, 'Output']
        
        
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
        
        
        # =================== #
        #    Normalize Sets   #
        # =================== #
        Scalar_Gyr = MinMaxScaler().fit(DFF_Gyr_Org_Trn_X.loc[:, Features_Gyr])
        DFF_Gyr_Org_Trn_X = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_Org_Trn_X.loc[:, Features_Gyr]), columns = Features_Gyr)
        DFF_Gyr_Org_Tst_X = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_Org_Tst_X.loc[:, Features_Gyr]), columns = Features_Gyr)
        DFF_Gyr_Att_X = pd.DataFrame(Scalar_Gyr.transform(DFF_Gyr_Att_X.loc[:, Features_Gyr]), columns = Features_Gyr)
        
        
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
        
          
        # ===================== #
        #    Train Classifier   #
        # ===================== #
        Clfs_Gyr = []
        maxDistance_Clfs_Gyr = []    
        
        #Classifier_Gyr = 'OneClassSVM'
        #for nu in frange(0.01, 0.3, 0.01):
        #    for gamma in frange(0.00005, 0.001, 0.00005):
        #        Parameters = [gamma, nu]
        
        Classifier_Gyr = 'LocalOutlierFactor'
        ns_neighbors = [3]
        for n_neighbors in ns_neighbors:
            Parameters = [n_neighbors]
            
            Clf, maxDistance = Clf_Train(Classifier_Gyr, Parameters, DFF_Gyr_Org_Trn_X)
            Clfs_Gyr.append(Clf)
            maxDistance_Clfs_Gyr.append(maxDistance)
            
            
        # ====================================== #
        #    Test Classifier for Original User   #
        # ====================================== #
        Decisions_Clfs_Gyr_Org = []
        for k in range(len(Clfs_Gyr)):
            Decisions_Gyr_Org = Clf_GetDecisions(Clfs_Gyr[k], DFF_Gyr_Org_Tst_X, maxDistance_Clfs_Gyr[k])
            Decisions_Clfs_Gyr_Org.append(Decisions_Gyr_Org)
            
        Predictions_Gyr_Org, Decisions_Gyr_Org = Clf_GetPredictions(Decisions_Clfs_Gyr_Org)
        
        
        # ================================== #
        #    Test Classifier for Attackers   #
        # ================================== #
        Decisions_Clfs_Gyr_Att = []
        for k in range(len(Clfs_Gyr)):
            Decisions_Gyr_Att = Clf_GetDecisions(Clfs_Gyr[k], DFF_Gyr_Att_X, maxDistance_Clfs_Gyr[k])
            Decisions_Clfs_Gyr_Att.append(Decisions_Gyr_Att)
            
        Predictions_Gyr_Att, Decisions_Gyr_Att = Clf_GetPredictions(Decisions_Clfs_Gyr_Att)
        
        
        # =========================== #
        #    Calculate Eval Metrics   #
        # =========================== #
        DFF_Gyr_Trn_Y = DFF_Gyr_Org_Trn_Y
        DFF_Gyr_Tst_Y = DFF_Gyr_Org_Tst_Y.append(DFF_Gyr_Att_Y, ignore_index = True)
        Predictions_Gyr = Predictions_Gyr_Org + Predictions_Gyr_Att
          
        EvaluationMetrics_Gyr = Clf_Evaluate(DFF_Gyr_Trn_Y, DFF_Gyr_Tst_Y, Predictions_Gyr, EvaluationMetrics_Gyr)
        
        
    EvaluationMetricsMean_Gyr = EvaluationMetrics()
    EvaluationMetricsMean_Gyr = CalculateMeanMetrics(EvaluationMetrics_Gyr, EvaluationMetricsMean_Gyr)
    
    EvaluationMetrics_Gyr = EvaluationMetricsMean_Gyr
    
    
    pre = 3
    SumaryTable = Texttable()
    SumaryTable.header(['User:\n' + OriginalUser, 'TrnOrgSize', 'TstOrgSize', 'TstAttSize', 'Mean Accuracy', 'Mean F1Score', 'Mean FAR', 'Mean FRR'])
    SumaryTable.set_cols_align(['c','c', 'c', 'c', 'c', 'c', 'c', 'c'])
    SumaryTable.set_cols_valign(['m','m', 'm', 'm', 'm', 'm', 'm', 'm'])
    SumaryTable.add_row(['Gyr', EvaluationMetrics_Gyr.getTrnOrgSize()[0], EvaluationMetrics_Gyr.getTstOrgSize()[0], EvaluationMetrics_Gyr.getTstAttSize()[0], str(round(EvaluationMetrics_Gyr.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Gyr.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Gyr.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Gyr.getFRR()[0]*100,pre))+' %'])
    print(SumaryTable.draw()) 
