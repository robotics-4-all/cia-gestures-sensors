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
        Clf = svm.OneClassSVM(gamma = Parameters[0], kernel = 'rbf', nu = Parameters[1])
        Clf.fit(TrnSet_X)
    else:
        raise ValueError('No such Algorithm found !!!')
        
    Decision = Clf.decision_function(TrnSet_X)
    maxDistance = max(Decision)
    
    return Clf, maxDistance


#--------------------------------------------------
# SwipesMultClassifier :
#--------------------------------------------------
def SwipesMultClassifier(Decisions_Swipes):
    
    Predictions_Swipes = []
    
    for j in range(len(Decisions_Swipes[0])):
        Desisions_Sum = 0 
        for i in range(len(Decisions_Swipes)):
            Desisions_Sum = Desisions_Sum + Decisions_Swipes[i][j]
            
        if Desisions_Sum >= 0:
            Predictions_Swipes.append(1)
        else:
            Predictions_Swipes.append(-1)  
            
    return Predictions_Swipes
    


#--------------------------------------------------
# SensorsClassifier :
#--------------------------------------------------
def SensorsClassifier(Decisions_Acc, Decisions_Gyr):
    
    Predictions_Sensors = []
    
    for i in range(len(Decisions_Acc)):
        Decision_Sensors = Decisions_Acc[i] + Decisions_Gyr[i]
        
        if Decision_Sensors >= 0:
            Predictions_Sensors.append(1)
        else:
            Predictions_Sensors.append(-1)
    
    return Predictions_Sensors


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
# AppendUserMetrics : 
# EvaluationMetrics_User
# EvaluationMetrics_All
#--------------------------------------------------
def AppendUserMetrics(EvaluationMetrics_User, EvaluationMetrics_All):
    
    Accuracy = EvaluationMetrics_User.getAccuracy()[0]
    F1Score = EvaluationMetrics_User.getF1Score()[0]
    ROC = EvaluationMetrics_User.getROC()[0]
    FAR = EvaluationMetrics_User.getFAR()[0]
    FRR = EvaluationMetrics_User.getFRR()[0]
    FalseAccept = EvaluationMetrics_User.getFalseAccept()[0]
    FalseReject = EvaluationMetrics_User.getFalseReject()[0]
    TrueAccept = EvaluationMetrics_User.getTrueAccept()[0]
    TrueReject = EvaluationMetrics_User.getTrueReject()[0]
    TrnSize = EvaluationMetrics_User.getTrnSize()[0]
    TstSize = EvaluationMetrics_User.getTstSize()[0]
    
    EvaluationMetrics_All.setAccuracy(Accuracy)
    EvaluationMetrics_All.setF1Score(F1Score)
    EvaluationMetrics_All.setROC(ROC)
    EvaluationMetrics_All.setFAR(FAR)
    EvaluationMetrics_All.setFRR(FRR)
    EvaluationMetrics_All.setFalseAccept(FalseAccept)
    EvaluationMetrics_All.setFalseReject(FalseReject)
    EvaluationMetrics_All.setTrueAccept(TrueAccept)
    EvaluationMetrics_All.setTrueReject(TrueReject)
    EvaluationMetrics_All.setTrnSize(TrnSize)
    EvaluationMetrics_All.setTstSize(TstSize)
    
    return EvaluationMetrics_All


#--------------------------------------------------
# frange
#--------------------------------------------------
def frange(start, stop, step):
	
	i = start
	while(i<stop):
		yield i
		i += step
        
        
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
def RunML(OriginalUser, DFF_Swipes, DFF_Acc, DFF_Gyr, Final_Features_Swipes, Final_Features_Sensors, Split_Rate, Folds):
    
    PrintUserStats = False
       
    # Initializing FOLD Evaluation Metrics
    #--------------------------------------
    EvaluationMetrics_Swipes_Folds = EvaluationMetrics()
    EvaluationMetrics_Acc_Folds = EvaluationMetrics()
    EvaluationMetrics_Gyr_Folds = EvaluationMetrics()
    EvaluationMetrics_Sensors_Folds = EvaluationMetrics()
        
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
        TrnSet_Swipes_X = Set_Original[0][0].loc[:, Final_Features_Swipes]
        TrnSet_Swipes_Y = Set_Original[0][0].loc[:, ['Output']].values
        TrnSet_Acc_X = Set_Original[0][1].loc[:, Final_Features_Sensors]
        TrnSet_Acc_Y = Set_Original[0][1].loc[:, ['Output']].values
        TrnSet_Gyr_X = Set_Original[0][2].loc[:, Final_Features_Sensors]
        TrnSet_Gyr_Y = Set_Original[0][2].loc[:, ['Output']].values
        
        # Test Set
        TstSet_Swipes_X = pd.concat([Set_Attackers[0].loc[:, Final_Features_Swipes], Set_Original[1][0].loc[:, Final_Features_Swipes]], ignore_index=True, sort=False)
        TstSet_Swipes_Y = pd.concat([Set_Attackers[0].loc[:, ['Output']], Set_Original[1][0].loc[:, ['Output']]], ignore_index=True, sort=False).values 
        TstSet_Acc_X = pd.concat([Set_Attackers[1].loc[:, Final_Features_Sensors], Set_Original[1][1].loc[:, Final_Features_Sensors]], ignore_index=True, sort=False)
        TstSet_Acc_Y = pd.concat([Set_Attackers[1].loc[:, ['Output']], Set_Original[1][1].loc[:, ['Output']]], ignore_index=True, sort=False).values
        TstSet_Gyr_X = pd.concat([Set_Attackers[2].loc[:, Final_Features_Sensors], Set_Original[1][2].loc[:, Final_Features_Sensors]], ignore_index=True, sort=False)
        TstSet_Gyr_Y = pd.concat([Set_Attackers[2].loc[:, ['Output']], Set_Original[1][2].loc[:, ['Output']]], ignore_index=True, sort=False).values
  

        # Normilizing Sets (MinMaxScalar)
        #--------------------------------
        Scalar_Swipes = MinMaxScaler().fit(TrnSet_Swipes_X)
        TrnSet_Swipes_X_Norm = Scalar_Swipes.transform(TrnSet_Swipes_X)
        TstSet_Swipes_X_Norm = Scalar_Swipes.transform(TstSet_Swipes_X)
        Scalar_Acc = MinMaxScaler().fit(TrnSet_Acc_X)
        TrnSet_Acc_X_Norm = Scalar_Acc.transform(TrnSet_Acc_X)
        TstSet_Acc_X_Norm = Scalar_Acc.transform(TstSet_Acc_X)
        Scalar_Gyr = MinMaxScaler().fit(TrnSet_Gyr_X)
        TrnSet_Gyr_X_Norm = Scalar_Gyr.transform(TrnSet_Gyr_X)
        TstSet_Gyr_X_Norm = Scalar_Gyr.transform(TstSet_Gyr_X)
    
    
        # Training Classifiers
        #---------------------
        Classifier = 'OneClassSVM'
        nus = []
        gammas = []
        for nu in frange(0.01, 0.3, 0.01):
            nus.append(nu)
        for gamma in frange(0.00005, 0.001, 0.00005):
            gammas.append(gamma)
        Clfs_Swipes = []
        maxDistances_Swipes = []
        for nu in nus:
            for gamma in gammas:
                Parameters = [gamma, nu]
                Clf_Swipes, maxDistance_Swipes = Clf_Train(Classifier, Parameters, TrnSet_Swipes_X_Norm)
                Clfs_Swipes.append(Clf_Swipes)
                maxDistances_Swipes.append(maxDistance_Swipes)
            
        Classifier = 'LocalOutlierFactor'
        n_neighbors = 3
        Parameters = [n_neighbors]
        Clf_Acc, maxDistance_Acc = Clf_Train(Classifier, Parameters, TrnSet_Acc_X_Norm)
            
        Classifier = 'LocalOutlierFactor'
        n_neighbors = 5
        Parameters = [n_neighbors]
        Clf_Gyr, maxDistance_Gyr = Clf_Train(Classifier, Parameters, TrnSet_Gyr_X_Norm)

                    
        # Testing Classifiers
        #--------------------
        Decisions_Swipes = []
        for k in range(len(Clfs_Swipes)):
            Decision_Swipes, Prediction_Swipes = Clf_Predict(Clfs_Swipes[k], TstSet_Swipes_X_Norm, maxDistances_Swipes[k])
            Decisions_Swipes.append(Decision_Swipes)
            
        Predictions_Swipes = SwipesMultClassifier(Decisions_Swipes)
        Decisions_Acc, Predictions_Acc = Clf_Predict(Clf_Acc, TstSet_Acc_X_Norm, maxDistance_Acc)
        Decisions_Gyr, Predictions_Gyr = Clf_Predict(Clf_Gyr, TstSet_Gyr_X_Norm, maxDistance_Gyr)
        Predictions_Sensors = SensorsClassifier(Decisions_Acc, Decisions_Gyr)

    
        # Evaluating Classifiers
        #-----------------------
        EvaluationMetrics_Swipes_Folds = Clf_Evaluate(TrnSet_Swipes_Y, TstSet_Swipes_Y, Predictions_Swipes, EvaluationMetrics_Swipes_Folds)
        EvaluationMetrics_Acc_Folds = Clf_Evaluate(TrnSet_Acc_Y, TstSet_Acc_Y, Predictions_Acc, EvaluationMetrics_Acc_Folds)
        EvaluationMetrics_Gyr_Folds = Clf_Evaluate(TrnSet_Gyr_Y, TstSet_Gyr_Y, Predictions_Gyr, EvaluationMetrics_Gyr_Folds)
        EvaluationMetrics_Sensors_Folds = Clf_Evaluate(TrnSet_Acc_Y, TstSet_Acc_Y, Predictions_Sensors, EvaluationMetrics_Sensors_Folds)
        

    # Calculating Mean of Folds Metrics
    #----------------------------------
    EvaluationMetrics_Swipes = EvaluationMetrics()
    EvaluationMetrics_Swipes = CalculateMeanMetrics(EvaluationMetrics_Swipes_Folds, EvaluationMetrics_Swipes)
    EvaluationMetrics_Acc = EvaluationMetrics()
    EvaluationMetrics_Acc = CalculateMeanMetrics(EvaluationMetrics_Acc_Folds, EvaluationMetrics_Acc)
    EvaluationMetrics_Gyr = EvaluationMetrics()
    EvaluationMetrics_Gyr = CalculateMeanMetrics(EvaluationMetrics_Gyr_Folds, EvaluationMetrics_Gyr)   
    EvaluationMetrics_Sensors = EvaluationMetrics()
    EvaluationMetrics_Sensors = CalculateMeanMetrics(EvaluationMetrics_Sensors_Folds, EvaluationMetrics_Sensors)

    
    # Print User Stats
    #-----------------
    if PrintUserStats:
        SumaryTable = Texttable()
        SumaryTable.header(['User:\n' + OriginalUser, 'TrnSize', 'TstSize', 'Mean Accuracy', 'Mean F1Score', 'Mean FAR', 'Mean FRR'])
        SumaryTable.set_cols_align(['c','c', 'c', 'c', 'c', 'c', 'c'])
        SumaryTable.set_cols_valign(['m','m', 'm', 'm', 'm', 'm', 'm'])
        SumaryTable.add_row(['Swipes', EvaluationMetrics_Swipes.getTrnSize()[0], EvaluationMetrics_Swipes.getTstSize()[0], EvaluationMetrics_Swipes.getAccuracy()[0], EvaluationMetrics_Swipes.getF1Score()[0], EvaluationMetrics_Swipes.getFAR()[0], EvaluationMetrics_Swipes.getFRR()[0]])
        SumaryTable.add_row(['Acc', EvaluationMetrics_Acc.getTrnSize()[0], EvaluationMetrics_Acc.getTstSize()[0], EvaluationMetrics_Acc.getAccuracy()[0], EvaluationMetrics_Acc.getF1Score()[0], EvaluationMetrics_Acc.getFAR()[0], EvaluationMetrics_Acc.getFRR()[0]])
        SumaryTable.add_row(['Gyr', EvaluationMetrics_Gyr.getTrnSize()[0], EvaluationMetrics_Gyr.getTstSize()[0], EvaluationMetrics_Gyr.getAccuracy()[0], EvaluationMetrics_Gyr.getF1Score()[0], EvaluationMetrics_Gyr.getFAR()[0], EvaluationMetrics_Gyr.getFRR()[0]])
        SumaryTable.add_row(['Sensors', EvaluationMetrics_Sensors.getTrnSize()[0], EvaluationMetrics_Sensors.getTstSize()[0], EvaluationMetrics_Sensors.getAccuracy()[0], EvaluationMetrics_Sensors.getF1Score()[0], EvaluationMetrics_Sensors.getFAR()[0], EvaluationMetrics_Sensors.getFRR()[0]])
        print(SumaryTable.draw())    
        
    
    return EvaluationMetrics_Swipes, EvaluationMetrics_Acc, EvaluationMetrics_Gyr, EvaluationMetrics_Sensors