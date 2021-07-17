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
from s5_Class_EvaluationMetrics_v001 import EvaluationMetrics

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
def Clf_Evaluate(TrnSet_Y, Predictions_Swipes_Org_Tst, Predictions_Swipes_Att, EvaluationMetrics):
    
    TrnOrgSize = len(TrnSet_Y)
    TstOrgSize = len(Predictions_Swipes_Org_Tst)
    TstAttSize = len(Predictions_Swipes_Att)
    
    Num_Of_Unlocks = 0
    Num_Of_Accepted = 0
    
    Threshold = 35
    Confidence = 60
    for sample_idx in range(len(Predictions_Swipes_Org_Tst)):
        sample = Predictions_Swipes_Org_Tst[sample_idx]
        if sample == 1:
            Confidence += 5
        else:
            Confidence -= 15
        if Confidence > 100:
            Confidence = 100
        if Confidence < Threshold:
            Confidence = 60
            Num_Of_Unlocks += 1
            
    Threshold = 35
    Confidence = 60
    for sample_idx in range(len(Predictions_Swipes_Att)):
        sample = Predictions_Swipes_Att[sample_idx]
        if sample == 1:
            Confidence += 5
        else:
            Confidence -= 15
        if Confidence > 100:
            Confidence = 100
        if Confidence >= Threshold:
            Num_Of_Accepted += 1
        if Confidence <= 0:
            Confidence = 0
    
    EvaluationMetrics.setTrnOrgSize(TrnOrgSize)
    EvaluationMetrics.setTstOrgSize(TstOrgSize)
    EvaluationMetrics.setTstAttSize(TstAttSize)
    EvaluationMetrics.setNum_Of_Unlocks(Num_Of_Unlocks)
    EvaluationMetrics.setNum_Of_Accepted(Num_Of_Accepted)
    
    return EvaluationMetrics


# =========================
# CalculateMeanMetrics : 
# EvaluationMetrics_Folds - 
# EvaluationMetrics - 
# =========================
def CalculateMeanMetrics(EvaluationMetrics_Folds, EvaluationMetrics):
    
    TrnOrgSize = np.mean(EvaluationMetrics_Folds.getTrnOrgSize())
    TstOrgSize = np.mean(EvaluationMetrics_Folds.getTstOrgSize())
    TstAttSize = np.mean(EvaluationMetrics_Folds.getTstAttSize())
    Num_Of_Unlocks = np.mean(EvaluationMetrics_Folds.getNum_Of_Unlocks())
    Num_Of_Accepted = np.mean(EvaluationMetrics_Folds.getNum_Of_Accepted())
    
    EvaluationMetrics.setTrnOrgSize(TrnOrgSize)
    EvaluationMetrics.setTstOrgSize(TstOrgSize)
    EvaluationMetrics.setTstAttSize(TstAttSize)
    EvaluationMetrics.setNum_Of_Unlocks(Num_Of_Unlocks)
    EvaluationMetrics.setNum_Of_Accepted(Num_Of_Accepted)
    
    return EvaluationMetrics


# ========================
# AppendUserMetrics : 
# EvaluationMetrics_User - 
# EvaluationMetrics_All - 
# ========================
def AppendUserMetrics(EvaluationMetrics_User, EvaluationMetrics_All):
    
    TrnOrgSize = EvaluationMetrics_User.getTrnOrgSize()[0]
    TstOrgSize = EvaluationMetrics_User.getTstOrgSize()[0]
    TstAttSize = EvaluationMetrics_User.getTstAttSize()[0]
    Num_Of_Unlocks = EvaluationMetrics_User.getNum_Of_Unlocks()[0]
    Num_Of_Accepted = EvaluationMetrics_User.getNum_Of_Accepted()[0]
    
    EvaluationMetrics_All.setTrnOrgSize(TrnOrgSize)
    EvaluationMetrics_All.setTstOrgSize(TstOrgSize)
    EvaluationMetrics_All.setTstAttSize(TstAttSize)
    EvaluationMetrics_All.setNum_Of_Unlocks(Num_Of_Unlocks)
    EvaluationMetrics_All.setNum_Of_Accepted(Num_Of_Accepted)
    
    return EvaluationMetrics_All