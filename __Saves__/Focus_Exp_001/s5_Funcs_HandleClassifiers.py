"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Labgroup

Author : Christos Emmanouil

Thesis : Continuous implicit authentication of mobile phone users with a combination of navigation and behavior data.

s5_Funcs_HandleClassifiers : This script contains functions in order to initialize, train, test and evaluate the classifiers.
"""

#################
#    IMPORTS    #
#################
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn import svm
from texttable import Texttable

from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor

from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MinMaxScaler

from s4_Funcs_CreateSets import CreateFinalSets
from s5_Class_EvaluationMetrics import EvaluationMetrics

##############################
#    INITIALIZE FUNCTIONS    #
##############################
#--------------------------------------------------
# Clf_Train : Split synced swipes, acc & gyr FDFs
# Classifier - 
# Parameters - 
# TrnSet_X - 
#--------------------------------------------------
def Clf_Train(Classifier, Parameters, TrnSet_X):
    
    if (Classifier == 'LocalOutlierFactor'):
        # Parameters = [3]
        Clf = LocalOutlierFactor(n_neighbors = Parameters[0], novelty = True)
        Clf.fit(TrnSet_X)
    elif (Classifier == 'EllipticEnvelope'):
        # parameters = [0]
        Clf = EllipticEnvelope(contamination = Parameters[0]).fit(TrnSet_X)
    elif (Classifier == 'IsolationForest'):
        # Parameters = [100, 0]
        Clf = IsolationForest(n_jobs = -1, n_estimators = Parameters[0], contamination = Parameters[1], bootstrap = False).fit(TrnSet_X)
    elif (Classifier == 'OneClassSVM'):
        # parameters = [0.001, 01]
        Clf = svm.OneClassSVM(gamma = Parameters[0], kernel = 'rbf', nu = Parameters[1], cache_size = 500)
        Clf.fit(TrnSet_X)
    else:
        raise ValueError('No such Algorithm found !!!')
        
    Decision = Clf.decision_function(TrnSet_X)
    maxDistance = max(Decision)
    
    return Clf, maxDistance


#--------------------------------------------------
# Clf_Predict : 
# Model - 
# TstSet_X - 
# maxDistance - 
#--------------------------------------------------
def Clf_Predict(Clf, TstSet_X, maxDistance):
    
    Prediction = Clf.predict(TstSet_X)
    
    Decision = Clf.decision_function(TstSet_X)
    Decision = Decision / maxDistance

    return Decision, Prediction


#--------------------------------------------------
# Clf_Evaluate : 
# Prediction - 
# TstSet_Y - 
# EvaluationMetrics -  
#--------------------------------------------------
def Clf_Evaluate(TrnSet_Y, TstSet_Y, Prediction, EvaluationMetrics):
    
    Accuracy = accuracy_score(TstSet_Y, Prediction)
    F1Score = f1_score(TstSet_Y, Prediction, pos_label = 1)
    ROC = roc_auc_score(TstSet_Y, Prediction)
    CunfusionMatrix = confusion_matrix(TstSet_Y, Prediction, labels = [-1, 1])
    FAR = CunfusionMatrix[0, 1] / np.sum(TstSet_Y == -1)
    FRR = CunfusionMatrix[1, 0] / np.sum(TstSet_Y == 1)
    FalseAccept = CunfusionMatrix[0, 1]
    FalseReject = CunfusionMatrix[1, 0]
    TrueAccept = CunfusionMatrix[1, 1]
    TrueReject = CunfusionMatrix[0, 0]
    TrnSize = len(TrnSet_Y)
    TstSize = len(TstSet_Y)
    
    EvaluationMetrics.setAccuracy(Accuracy)
    EvaluationMetrics.setF1Score(F1Score)
    EvaluationMetrics.setROC(ROC)
    EvaluationMetrics.setFAR(FAR)
    EvaluationMetrics.setFRR(FRR)
    EvaluationMetrics.setFalseAccept(FalseAccept)
    EvaluationMetrics.setFalseReject(FalseReject)
    EvaluationMetrics.setTrueAccept(TrueAccept)
    EvaluationMetrics.setTrueReject(TrueReject)
    EvaluationMetrics.setTrnSize(TrnSize)
    EvaluationMetrics.setTstSize(TstSize)
    
    return EvaluationMetrics


#--------------------------------------------------
# CalculateMeanMetrics : 
# EvaluationMetrics_Folds
# Folds
# EvaluationMetrics
#--------------------------------------------------
def CalculateMeanMetrics(EvaluationMetrics_Folds, EvaluationMetrics):
    
    Accuracy = np.mean(EvaluationMetrics_Folds.getAccuracy())
    F1Score = np.mean(EvaluationMetrics_Folds.getF1Score())
    ROC = np.mean(EvaluationMetrics_Folds.getROC())
    FAR = np.mean(EvaluationMetrics_Folds.getFAR())
    FRR = np.mean(EvaluationMetrics_Folds.getFRR())
    FalseAccept = np.mean(EvaluationMetrics_Folds.getFalseAccept())
    FalseReject = np.mean(EvaluationMetrics_Folds.getFalseReject())
    TrueAccept = np.mean(EvaluationMetrics_Folds.getTrueAccept())
    TrueReject = np.mean(EvaluationMetrics_Folds.getTrueReject())
    TrnSize = np.mean(EvaluationMetrics_Folds.getTrnSize())
    TstSize = np.mean(EvaluationMetrics_Folds.getTstSize())
    
    EvaluationMetrics.setAccuracy(Accuracy)
    EvaluationMetrics.setF1Score(F1Score)
    EvaluationMetrics.setROC(ROC)
    EvaluationMetrics.setFAR(FAR)
    EvaluationMetrics.setFRR(FRR)
    EvaluationMetrics.setFalseAccept(FalseAccept)
    EvaluationMetrics.setFalseReject(FalseReject)
    EvaluationMetrics.setTrueAccept(TrueAccept)
    EvaluationMetrics.setTrueReject(TrueReject)
    EvaluationMetrics.setTrnSize(TrnSize)
    EvaluationMetrics.setTstSize(TstSize)
    
    return EvaluationMetrics


#--------------------------------------------------
# RunML : 
# ScreenName - 
# DF_Users_Final - 
# DFF_Swipes - 
# DFF_Acc - 
# DFF_Gyr - 
# Final_Features_Swipes - 
# Final_Features_Sensors - 
# Split_Rate - 
# Folds - 
#--------------------------------------------------
def frange(start, stop, step):
	
	i = start
	while(i<stop):
		yield i
		i += step

def RunML(ScreenName, DF_Users_Final, DFF_Swipes, DFF_Acc, DFF_Gyr, Final_Features_Swipes, Final_Features_Sensors, Split_Rate, Folds):
    
    F_Swipes = False
    F_Acc = True
    F_Gyr = True
    
    PrintUserStats = False
    
    nus = []
    gammas = []
    for nu in frange(0.01, 0.3, 0.01):
        nus.append(nu)
    for gamma in frange(0.00005, 0.001, 0.00005):
        gammas.append(gamma)
    
    # Initializing FINAL Evaluation Metrics
    #--------------------------------------
    if F_Swipes: EvaluationMetrics_Swipes = EvaluationMetrics()
    if F_Acc: EvaluationMetrics_Acc = EvaluationMetrics()
    if F_Gyr: EvaluationMetrics_Gyr = EvaluationMetrics()
    
    for i in tqdm(range(len(DF_Users_Final)), desc = '-> User'):
        
        OriginalUser = DF_Users_Final['User'].values[i]
    
        # Initializing FOLD Evaluation Metrics
        #--------------------------------------
        if F_Swipes: EvaluationMetrics_Swipes_Folds = EvaluationMetrics()
        if F_Acc: EvaluationMetrics_Acc_Folds = EvaluationMetrics()
        if F_Gyr: EvaluationMetrics_Gyr_Folds = EvaluationMetrics()
        
        for j in tqdm(range(Folds), desc = '-> Fold'):
            
            # Creating Original User's & Attackers Sets
            #------------------------------------------
            # FDFs_Original = [FDFs_Org_Trn, FDFs_Org_Tst]
            # FDFs_Attackers = FDFs_Attackers = [FDF_Att_Swipes, FDF_Att_Acc, FDF_Att_Gyr]
            Synced_Sensors = True
            Set_Original, Set_Attackers = CreateFinalSets(DFF_Swipes, DFF_Acc, DFF_Gyr, OriginalUser, Synced_Sensors, Split_Rate)
        
        
            # Creating Train & Test Sets
            #---------------------------
            # Train Set
            if F_Swipes: 
                TrnSet_Swipes_X = Set_Original[0][0].loc[:, Final_Features_Swipes]
                TrnSet_Swipes_Y = Set_Original[0][0].loc[:, ['Output']].values
            if F_Acc: 
                TrnSet_Acc_X = Set_Original[0][1].loc[:, Final_Features_Sensors]
                TrnSet_Acc_Y = Set_Original[0][1].loc[:, ['Output']].values
            if F_Gyr: 
                TrnSet_Gyr_X = Set_Original[0][2].loc[:, Final_Features_Sensors]
                TrnSet_Gyr_Y = Set_Original[0][2].loc[:, ['Output']].values
            
            # Test Set
            if F_Swipes:
                TstSet_Swipes_X = pd.concat([Set_Attackers[0].loc[:, Final_Features_Swipes], Set_Original[1][0].loc[:, Final_Features_Swipes]], ignore_index=True, sort=False)
                TstSet_Swipes_Y = pd.concat([Set_Attackers[0].loc[:, ['Output']], Set_Original[1][0].loc[:, ['Output']]], ignore_index=True, sort=False).values    
            if F_Acc:
                TstSet_Acc_X = pd.concat([Set_Attackers[1].loc[:, Final_Features_Sensors], Set_Original[1][1].loc[:, Final_Features_Sensors]], ignore_index=True, sort=False)
                TstSet_Acc_Y = pd.concat([Set_Attackers[1].loc[:, ['Output']], Set_Original[1][1].loc[:, ['Output']]], ignore_index=True, sort=False).values
            if F_Gyr:
                TstSet_Gyr_X = pd.concat([Set_Attackers[2].loc[:, Final_Features_Sensors], Set_Original[1][2].loc[:, Final_Features_Sensors]], ignore_index=True, sort=False)
                TstSet_Gyr_Y = pd.concat([Set_Attackers[2].loc[:, ['Output']], Set_Original[1][2].loc[:, ['Output']]], ignore_index=True, sort=False).values
        
    
            # Normilizing Sets (MinMaxScalar)
            #--------------------------------
            if F_Swipes:
                Scalar_Swipes = MinMaxScaler().fit(TrnSet_Swipes_X)
                TrnSet_Swipes_X_Norm = Scalar_Swipes.transform(TrnSet_Swipes_X)
                TstSet_Swipes_X_Norm = Scalar_Swipes.transform(TstSet_Swipes_X)
            if F_Acc:
                Scalar_Acc = MinMaxScaler().fit(TrnSet_Acc_X)
                TrnSet_Acc_X_Norm = Scalar_Acc.transform(TrnSet_Acc_X)
                TstSet_Acc_X_Norm = Scalar_Acc.transform(TstSet_Acc_X)
            if F_Gyr:
                Scalar_Gyr = MinMaxScaler().fit(TrnSet_Gyr_X)
                TrnSet_Gyr_X_Norm = Scalar_Gyr.transform(TrnSet_Gyr_X)
                TstSet_Gyr_X_Norm = Scalar_Gyr.transform(TstSet_Gyr_X)
        
        
            # Training Classifiers
            #---------------------
            Classifier = 'OneClassSVM'

            if F_Swipes:
                Clfs_Swipes = []
                maxDistances_Swipes = []
            if F_Acc:
                Clfs_Acc = []
                maxDistances_Acc = []   
            if F_Gyr:
                Clfs_Gyr = []
                maxDistances_Gyr = []   
                
            for nu in nus:
                for gamma in gammas:
                    Parameters = [gamma, nu]
                    if F_Swipes:
                        Clf_Swipes, maxDistance_Swipes = Clf_Train(Classifier, Parameters, TrnSet_Swipes_X_Norm)
                        Clfs_Swipes.append(Clf_Swipes)
                        maxDistances_Swipes.append(maxDistance_Swipes)
                    if F_Acc:
                        Clf_Acc, maxDistance_Acc = Clf_Train(Classifier, Parameters, TrnSet_Acc_X_Norm)
                        Clfs_Acc.append(Clf_Acc)
                        maxDistances_Acc.append(maxDistance_Acc)
                    if F_Gyr:
                        Clf_Gyr, maxDistance_Gyr = Clf_Train(Classifier, Parameters, TrnSet_Gyr_X_Norm)
                        Clfs_Gyr.append(Clf_Gyr)
                        maxDistances_Gyr.append(maxDistance_Gyr)

                        
            # Testing Classifiers
            #--------------------
            if F_Swipes:
                Decisions_Swipes = []
                Predictions_Swipes = []
            if F_Acc:
                Decisions_Acc = []
                Predictions_Acc = []   
            if F_Gyr:
                Decisions_Gyr = []
                Predictions_Gyr = []
                
            for k in range(len(nus) * len(gammas)):               
                if F_Swipes: 
                    Decision_Swipes, Prediction_Swipes = Clf_Predict(Clfs_Swipes[k], TstSet_Swipes_X_Norm, maxDistances_Swipes[k])
                    Decisions_Swipes.append(Decision_Swipes)
                    Predictions_Swipes.append(Prediction_Swipes)                        
                if F_Acc: 
                    Decision_Acc, Prediction_Acc = Clf_Predict(Clfs_Acc[k], TstSet_Acc_X_Norm, maxDistances_Acc[k])
                    Decisions_Acc.append(Decision_Acc)
                    Predictions_Acc.append(Prediction_Acc)                        
                if F_Gyr: 
                    Decision_Gyr, Prediction_Gyr = Clf_Predict(Clfs_Gyr[k], TstSet_Gyr_X_Norm, maxDistances_Gyr[k])
                    Decisions_Gyr.append(Decision_Gyr)
                    Predictions_Gyr.append(Prediction_Gyr)                        
        
        
            # Evaluating Classifiers
            #-----------------------
            for k in range(len(nus) * len(gammas)):
                if F_Swipes: EvaluationMetrics_Swipes_Folds = Clf_Evaluate(TrnSet_Swipes_Y, TstSet_Swipes_Y, Predictions_Swipes[k], EvaluationMetrics_Swipes_Folds)
                if F_Acc: EvaluationMetrics_Acc_Folds = Clf_Evaluate(TrnSet_Acc_Y, TstSet_Acc_Y, Predictions_Acc[k], EvaluationMetrics_Acc_Folds)
                if F_Gyr: EvaluationMetrics_Gyr_Folds = Clf_Evaluate(TrnSet_Gyr_Y, TstSet_Gyr_Y, Predictions_Gyr[k], EvaluationMetrics_Gyr_Folds)
    
    
        # Calculating Mean of Folds Metrics
        #----------------------------------
        if F_Swipes: EvaluationMetrics_Swipes = CalculateMeanMetrics(EvaluationMetrics_Swipes_Folds, EvaluationMetrics_Swipes)
        if F_Acc: EvaluationMetrics_Acc = CalculateMeanMetrics(EvaluationMetrics_Acc_Folds, EvaluationMetrics_Acc)
        if F_Gyr: EvaluationMetrics_Gyr = CalculateMeanMetrics(EvaluationMetrics_Gyr_Folds, EvaluationMetrics_Gyr)    
    
        
        # Print User Stats
        #-----------------
        if PrintUserStats:
            SumaryTable = Texttable()
            SumaryTable.header(['User:\n' + OriginalUser, 'TrnSize', 'TstSize', 'Mean Accuracy', 'Mean F1Score', 'Mean FAR', 'Mean FRR'])
            SumaryTable.set_cols_align(['c','c', 'c', 'c', 'c', 'c', 'c'])
            SumaryTable.set_cols_valign(['m','m', 'm', 'm', 'm', 'm', 'm'])
            if F_Swipes: SumaryTable.add_row(['Swipes', EvaluationMetrics_Swipes.getTrnSize()[i], EvaluationMetrics_Swipes.getTstSize()[i], EvaluationMetrics_Swipes.getAccuracy()[i], EvaluationMetrics_Swipes.getF1Score()[i], EvaluationMetrics_Swipes.getFAR()[i], EvaluationMetrics_Swipes.getFRR()[i]])
            if F_Acc: SumaryTable.add_row(['Acc', EvaluationMetrics_Acc.getTrnSize()[i], EvaluationMetrics_Acc.getTstSize()[i], EvaluationMetrics_Acc.getAccuracy()[i], EvaluationMetrics_Acc.getF1Score()[i], EvaluationMetrics_Acc.getFAR()[i], EvaluationMetrics_Acc.getFRR()[i]])
            if F_Gyr: SumaryTable.add_row(['Gyr', EvaluationMetrics_Gyr.getTrnSize()[i], EvaluationMetrics_Gyr.getTstSize()[i], EvaluationMetrics_Gyr.getAccuracy()[i], EvaluationMetrics_Gyr.getF1Score()[i], EvaluationMetrics_Gyr.getFAR()[i], EvaluationMetrics_Gyr.getFRR()[i]])
            print(SumaryTable.draw())    
        
    
    # Calculating Total Metrics
    #--------------------------
    if F_Swipes: 
        EvaluationMetrics_Swipes_Total = EvaluationMetrics()
        EvaluationMetrics_Swipes_Total = CalculateMeanMetrics(EvaluationMetrics_Swipes, EvaluationMetrics_Swipes_Total)
    if F_Acc:
        EvaluationMetrics_Acc_Total = EvaluationMetrics()
        EvaluationMetrics_Acc_Total = CalculateMeanMetrics(EvaluationMetrics_Acc, EvaluationMetrics_Acc_Total)
    if F_Gyr:
        EvaluationMetrics_Gyr_Total = EvaluationMetrics()
        EvaluationMetrics_Gyr_Total = CalculateMeanMetrics(EvaluationMetrics_Gyr, EvaluationMetrics_Gyr_Total)
    
    
    # Print Total Stats
    #------------------
    SumaryTable = Texttable()
    SumaryTable.header([ScreenName + '\n' + str(len(DF_Users_Final)) + ' Users' + '\n' + str(Split_Rate) + ' Split' + '\n' + str(Folds) + ' Folds', 'TrnSize', 'TstSize', 'Mean Accuracy', 'Mean F1Score', 'Mean FAR', 'Mean FRR'])
    SumaryTable.set_cols_align(['c','c', 'c', 'c', 'c', 'c', 'c'])
    SumaryTable.set_cols_valign(['m','m', 'm', 'm', 'm', 'm', 'm'])
    if F_Swipes: SumaryTable.add_row(['Swipes', EvaluationMetrics_Swipes_Total.getTrnSize()[0], EvaluationMetrics_Swipes_Total.getTstSize()[0], EvaluationMetrics_Swipes_Total.getAccuracy()[0], EvaluationMetrics_Swipes_Total.getF1Score()[0], EvaluationMetrics_Swipes_Total.getFAR()[0], EvaluationMetrics_Swipes_Total.getFRR()[0]])
    if F_Acc: SumaryTable.add_row(['Acc', EvaluationMetrics_Acc_Total.getTrnSize()[0], EvaluationMetrics_Acc_Total.getTstSize()[0], EvaluationMetrics_Acc_Total.getAccuracy()[0], EvaluationMetrics_Acc_Total.getF1Score()[0], EvaluationMetrics_Acc_Total.getFAR()[0], EvaluationMetrics_Acc_Total.getFRR()[0]])
    if F_Gyr: SumaryTable.add_row(['Gyr', EvaluationMetrics_Gyr_Total.getTrnSize()[0], EvaluationMetrics_Gyr_Total.getTstSize()[0], EvaluationMetrics_Gyr_Total.getAccuracy()[0], EvaluationMetrics_Gyr_Total.getF1Score()[0], EvaluationMetrics_Gyr_Total.getFAR()[0], EvaluationMetrics_Gyr_Total.getFRR()[0]])
    print(SumaryTable.draw())
    
    if F_Swipes: row_Swipes = np.array([[EvaluationMetrics_Swipes_Total.getTrnSize()[0], EvaluationMetrics_Swipes_Total.getTstSize()[0], EvaluationMetrics_Swipes_Total.getAccuracy()[0], EvaluationMetrics_Swipes_Total.getF1Score()[0], EvaluationMetrics_Swipes_Total.getFAR()[0], EvaluationMetrics_Swipes_Total.getFRR()[0]]])
    if F_Acc: row_Acc = np.array([[EvaluationMetrics_Acc_Total.getTrnSize()[0], EvaluationMetrics_Acc_Total.getTstSize()[0], EvaluationMetrics_Acc_Total.getAccuracy()[0], EvaluationMetrics_Acc_Total.getF1Score()[0], EvaluationMetrics_Acc_Total.getFAR()[0], EvaluationMetrics_Acc_Total.getFRR()[0]]])
    if F_Gyr: row_Gyr = np.array([[EvaluationMetrics_Gyr_Total.getTrnSize()[0], EvaluationMetrics_Gyr_Total.getTstSize()[0], EvaluationMetrics_Gyr_Total.getAccuracy()[0], EvaluationMetrics_Gyr_Total.getF1Score()[0], EvaluationMetrics_Gyr_Total.getFAR()[0], EvaluationMetrics_Gyr_Total.getFRR()[0]]])
    
    return row_Acc, row_Gyr