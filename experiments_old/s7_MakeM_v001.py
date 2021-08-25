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
Exp = '_Exp_005'
Exp_Save_Path = os.path.join(saveDir, ScreenName+Exp)


# ======================== #
#    Load Saved Pickles    #
# ======================== #
DF_Users_Final = pd.read_pickle(os.path.join(Exp_Save_Path, 'DF_Users_Final.pkl'))
DFF_Acc = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Acc.pkl'))
DFF_Gyr = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Gyr.pkl'))
DFF_Swipes = pd.read_pickle(os.path.join(Exp_Save_Path, 'DFF_Swipes.pkl'))


# ========================== #
#    Select Original User    #
# ========================== #
OriginalUser = 'frl4fzq'

for OriginalUser in DF_Users_Final['User']:
    print(OriginalUser)
    

    # ===================================== #
    #    Split Original & Attackers Sets    #
    # ===================================== #
    DFF_Acc_Original, DFF_Acc_Attackers = SplitDFF_OrgAtt(DFF_Acc, OriginalUser)
    DFF_Gyr_Original, DFF_Gyr_Attackers = SplitDFF_OrgAtt(DFF_Gyr, OriginalUser)
    DFF_Swipes_Original, DFF_Swipes_Attackers = SplitDFF_OrgAtt(DFF_Swipes, OriginalUser)
    
    
    
    k = 10
    EvaluationMetrics_Acc = EvaluationMetrics()
    
    for Fold in tqdm(range(k), desc = '-> Fold'):
    
            
        # ===================================== #
        #    Split Original Train & Test Sets   #
        # ===================================== #
        Split_Rate = 0.2
        DFF_Acc_Original_Trn, DFF_Acc_Original_Tst = SplitRandom(DFF_Acc_Original, Split_Rate)
        DFF_Gyr_Original_Trn, DFF_Gyr_Original_Tst = SplitRandom(DFF_Gyr_Original, Split_Rate)
        DFF_Swipes_Original_Trn, DFF_Swipes_Original_Tst = SplitRandom(DFF_Swipes_Original, Split_Rate)
        
        if len(DFF_Acc_Original_Tst) == 0:
            print('malakia')
            break
        
        
        # ================================= #
        #    Split Inputs(X) & Outputs(Y)   #
        # ================================= #
        Features_Acc = ['Mean', 'STD', 'Max', 'Min', 'Range', 'Percentile25', 'Percentile50', 'Percentile75', 'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2'] #, 'MeanFrequency']
        DFF_Acc_Org_Trn_X = DFF_Acc_Original_Trn.loc[:, Features_Acc]
        DFF_Acc_Org_Trn_Y = DFF_Acc_Original_Trn.loc[:, 'Output']
        DFF_Acc_Org_Tst_X = DFF_Acc_Original_Tst.loc[:, Features_Acc]
        DFF_Acc_Org_Tst_Y = DFF_Acc_Original_Tst.loc[:, 'Output']
        DFF_Acc_Att_X = DFF_Acc_Attackers.loc[:, Features_Acc]
        DFF_Acc_Att_Y = DFF_Acc_Attackers.loc[:, 'Output']
        
        
        # ==================== #
        #    Select Features   #
        # ==================== #
        #plt.figure(figsize=(8, 8))
        #corr_Acc = DFF_Acc_Org_Trn_X.loc[:, Features_Acc].corr()
        
        #corrplot(corr_Acc, size_scale=300)
        
        #final_features = pd.DataFrame(columns= ['Feature', 'SAC'])
        #for i in range(len(Features_Acc)):
        #    sum = 0
        #    for j in range(len(Features_Acc)):
        #        if i == j:
        #            continue
        #        sum = sum + abs(corr_Acc.iloc[i, j])
        #    df = {'Feature': Features_Acc[i], 'SAC': sum}
        #    final_features = final_features.append(df, ignore_index=True)
                
        Features_Acc = ['Mean', 'Max', 'Min', 'Percentile25', 'Percentile50', 'Percentile75', 'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2']
            
        
        
        # =================== #
        #    Normalize Sets   #
        # =================== #
        Scalar_Acc = MinMaxScaler().fit(DFF_Acc_Org_Trn_X.loc[:, Features_Acc])
        DFF_Acc_Org_Trn_X = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_Org_Trn_X.loc[:, Features_Acc]), columns = Features_Acc)
        DFF_Acc_Org_Tst_X = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_Org_Tst_X.loc[:, Features_Acc]), columns = Features_Acc)
        DFF_Acc_Att_X = pd.DataFrame(Scalar_Acc.transform(DFF_Acc_Att_X.loc[:, Features_Acc]), columns = Features_Acc)
        
        # ================== #
        #    Find OUtliers   #
        # ================== #
        from sklearn.neighbors import LocalOutlierFactor
        
        inliers = pd.DataFrame(columns = Features_Acc)
         
        clf = LocalOutlierFactor(n_neighbors=5, contamination=0.1)		# Find inliers and outliers of one user's swipes
        y_pred = clf.fit_predict(DFF_Acc_Org_Trn_X)
        for i in range(len(y_pred)):
        	if(y_pred[i]==1):
        		inliers = inliers.append(DFF_Acc_Org_Trn_X.iloc[i], ignore_index=True)
        
        DFF_Acc_Org_Trn_X = inliers
        DFF_Acc_Org_Trn_Y = DFF_Acc_Org_Trn_Y[0:len(inliers)]
          
        
        # ===================== #
        #    Train Classifier   #
        # ===================== #
        Clfs_Acc = []
        maxDistance_Clfs_Acc = []    
        
        #Classifier_Acc = 'OneClassSVM'
        #for nu in frange(0.01, 0.3, 0.01):
        #    for gamma in frange(0.00005, 0.001, 0.00005):
        #        Parameters = [gamma, nu]
        
        Classifier_Acc = 'LocalOutlierFactor'
        ns_neighbors = [3]
        for n_neighbors in ns_neighbors:
            Parameters = [n_neighbors]
            
            Clf, maxDistance = Clf_Train(Classifier_Acc, Parameters, DFF_Acc_Org_Trn_X)
            Clfs_Acc.append(Clf)
            maxDistance_Clfs_Acc.append(maxDistance)
            
            
        # ====================================== #
        #    Test Classifier for Original User   #
        # ====================================== #
        Decisions_Clfs_Acc_Org = []
        for k in range(len(Clfs_Acc)):
            Decisions_Acc_Org = Clf_GetDecisions(Clfs_Acc[k], DFF_Acc_Org_Tst_X, maxDistance_Clfs_Acc[k])
            Decisions_Clfs_Acc_Org.append(Decisions_Acc_Org)
            
        Predictions_Acc_Org, Decisions_Acc_Org = Clf_GetPredictions(Decisions_Clfs_Acc_Org)
        
        
        # ================================== #
        #    Test Classifier for Attackers   #
        # ================================== #
        Decisions_Clfs_Acc_Att = []
        for k in range(len(Clfs_Acc)):
            Decisions_Acc_Att = Clf_GetDecisions(Clfs_Acc[k], DFF_Acc_Att_X, maxDistance_Clfs_Acc[k])
            Decisions_Clfs_Acc_Att.append(Decisions_Acc_Att)
            
        Predictions_Acc_Att, Decisions_Acc_Att = Clf_GetPredictions(Decisions_Clfs_Acc_Att)
        
        
        # =========================== #
        #    Calculate Eval Metrics   #
        # =========================== #
        DFF_Acc_Trn_Y = DFF_Acc_Org_Trn_Y
        DFF_Acc_Tst_Y = DFF_Acc_Org_Tst_Y.append(DFF_Acc_Att_Y, ignore_index = True)
        Predictions_Acc = Predictions_Acc_Org + Predictions_Acc_Att
          
        EvaluationMetrics_Acc = Clf_Evaluate(DFF_Acc_Trn_Y, DFF_Acc_Tst_Y, Predictions_Acc, EvaluationMetrics_Acc)
        
        
    EvaluationMetricsMean_Acc = EvaluationMetrics()
    EvaluationMetricsMean_Acc = CalculateMeanMetrics(EvaluationMetrics_Acc, EvaluationMetricsMean_Acc)
    
    EvaluationMetrics_Acc = EvaluationMetricsMean_Acc
    
    
    pre = 3
    SumaryTable = Texttable()
    SumaryTable.header(['User:\n' + OriginalUser, 'TrnOrgSize', 'TstOrgSize', 'TstAttSize', 'Mean Accuracy', 'Mean F1Score', 'Mean FAR', 'Mean FRR'])
    SumaryTable.set_cols_align(['c','c', 'c', 'c', 'c', 'c', 'c', 'c'])
    SumaryTable.set_cols_valign(['m','m', 'm', 'm', 'm', 'm', 'm', 'm'])
    SumaryTable.add_row(['Acc', EvaluationMetrics_Acc.getTrnOrgSize()[0], EvaluationMetrics_Acc.getTstOrgSize()[0], EvaluationMetrics_Acc.getTstAttSize()[0], str(round(EvaluationMetrics_Acc.getAccuracy()[0]*100,pre))+' %', str(round(EvaluationMetrics_Acc.getF1Score()[0]*100,pre))+' %', str(round(EvaluationMetrics_Acc.getFAR()[0]*100,pre))+' %', str(round(EvaluationMetrics_Acc.getFRR()[0]*100,pre))+' %'])
    print(SumaryTable.draw()) 
