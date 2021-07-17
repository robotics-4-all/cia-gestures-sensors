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
from texttable import Texttable

from sklearn import svm
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor

from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MinMaxScaler

from s0_Funcs_Util_v000 import frange
from s5_Class_EvaluationMetrics_v000 import EvaluationMetrics

##############################
#    INITIALIZE FUNCTIONS    #
##############################
# ===============================================
# Clf_Train : Split synced swipes, acc & gyr FDFs
# Classifier - 
# Parameters - 
# TrnSet_X - 
# ===============================================
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


# =================
# Clf_GetDecisions : 
# Model - 
# TstSet_X - 
# maxDistance - 
# =================
def Clf_GetDecisions(Clf, TstSet_X, maxDistance):
    
    Decisions = Clf.decision_function(TstSet_X)
    Decisions = Decisions / maxDistance

    return Decisions

# ===================
# Clf_GetPredictions :
# Decisions - 
# ===================
def Clf_GetPredictions(Clf, TstSet_X):
    
    Predictions = Clf.predict(TstSet_X)
            
    return Predictions

# ===================
# Clf_GetPredictions :
# Decisions - 
# ===================
def Clf_GetTotalPredictions(Predictions):
    
    Predictions_Total = []
    
    for j in range(len(Predictions[0])):
        Predictions_Sum = 0 
        for i in range(len(Predictions)):
            Predictions_Sum = Predictions_Sum + Predictions[i][j]
            
        if Predictions_Sum >= 0:
            Predictions_Total.append(1)
        else:
            Predictions_Total.append(-1)  
            
    return Predictions_Total


# ===================
# Clf_Evaluate : 
# TrnSet_Y - 
# TstSet_Y - 
# Prediction - 
# EvaluationMetrics - 
# ===================
def Clf_Evaluate(TrnSet_Y, TstSet_Y, Prediction, EvaluationMetrics):
    
    Accuracy = accuracy_score(TstSet_Y, Prediction)
    F1Score = f1_score(TstSet_Y, Prediction)
    ROC = roc_auc_score(TstSet_Y, Prediction)
    CunfusionMatrix = confusion_matrix(TstSet_Y, Prediction, labels = [-1, 1])
    FalseAccept = CunfusionMatrix[0, 1]
    FalseReject = CunfusionMatrix[1, 0]
    TrueAccept = CunfusionMatrix[1, 1]
    TrueReject = CunfusionMatrix[0, 0]
    FAR = FalseAccept / np.sum(TstSet_Y == -1)
    FRR = FalseReject / np.sum(TstSet_Y == 1)

    TrnOrgSize = len(TrnSet_Y)
    TstOrgSize = len(TstSet_Y[TstSet_Y == 1])
    TstAttSize = len(TstSet_Y[TstSet_Y == -1])
    
    EvaluationMetrics.setAccuracy(Accuracy)
    EvaluationMetrics.setF1Score(F1Score)
    EvaluationMetrics.setROC(ROC)
    EvaluationMetrics.setFAR(FAR)
    EvaluationMetrics.setFRR(FRR)
    EvaluationMetrics.setFalseAccept(FalseAccept)
    EvaluationMetrics.setFalseReject(FalseReject)
    EvaluationMetrics.setTrueAccept(TrueAccept)
    EvaluationMetrics.setTrueReject(TrueReject)
    EvaluationMetrics.setTrnOrgSize(TrnOrgSize)
    EvaluationMetrics.setTstOrgSize(TstOrgSize)
    EvaluationMetrics.setTstAttSize(TstAttSize)
    
    return EvaluationMetrics


# =========================
# CalculateMeanMetrics : 
# EvaluationMetrics_Folds - 
# EvaluationMetrics - 
# =========================
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
    TrnOrgSize = np.mean(EvaluationMetrics_Folds.getTrnOrgSize())
    TstOrgSize = np.mean(EvaluationMetrics_Folds.getTstOrgSize())
    TstAttSize = np.mean(EvaluationMetrics_Folds.getTstAttSize())
    
    EvaluationMetrics.setAccuracy(Accuracy)
    EvaluationMetrics.setF1Score(F1Score)
    EvaluationMetrics.setROC(ROC)
    EvaluationMetrics.setFAR(FAR)
    EvaluationMetrics.setFRR(FRR)
    EvaluationMetrics.setFalseAccept(FalseAccept)
    EvaluationMetrics.setFalseReject(FalseReject)
    EvaluationMetrics.setTrueAccept(TrueAccept)
    EvaluationMetrics.setTrueReject(TrueReject)
    EvaluationMetrics.setTrnOrgSize(TrnOrgSize)
    EvaluationMetrics.setTstOrgSize(TstOrgSize)
    EvaluationMetrics.setTstAttSize(TstAttSize)
    
    return EvaluationMetrics


# ========================
# AppendUserMetrics : 
# EvaluationMetrics_User - 
# EvaluationMetrics_All - 
# ========================
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
    TrnOrgSize = EvaluationMetrics_User.getTrnOrgSize()[0]
    TstOrgSize = EvaluationMetrics_User.getTstOrgSize()[0]
    TstAttSize = EvaluationMetrics_User.getTstAttSize()[0]
    
    EvaluationMetrics_All.setAccuracy(Accuracy)
    EvaluationMetrics_All.setF1Score(F1Score)
    EvaluationMetrics_All.setROC(ROC)
    EvaluationMetrics_All.setFAR(FAR)
    EvaluationMetrics_All.setFRR(FRR)
    EvaluationMetrics_All.setFalseAccept(FalseAccept)
    EvaluationMetrics_All.setFalseReject(FalseReject)
    EvaluationMetrics_All.setTrueAccept(TrueAccept)
    EvaluationMetrics_All.setTrueReject(TrueReject)
    EvaluationMetrics_All.setTrnOrgSize(TrnOrgSize)
    EvaluationMetrics_All.setTstOrgSize(TstOrgSize)
    EvaluationMetrics_All.setTstAttSize(TstAttSize)
    
    return EvaluationMetrics_All