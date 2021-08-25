"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Lab Group

Author : Christos Emmanouil
"""
# ============= #
#    Imports    #
# ============= #
import numpy as np
from sklearn import svm
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score, confusion_matrix


# =============== #
#    Functions    #
# =============== #
def Clf_Train(Classifier, Parameters, TrnSet_X):
    """
    Select, initialize and fit a classifier.

    :param Classifier: Classifier name
    :param Parameters: Parameters its classifiers must have
    :param TrnSet_X: The train set, in order to fit the classifier
    :return: The classifier and the maximum distance of the train set.
    """

    if Classifier == 'LocalOutlierFactor':
        # Parameters = [3]
        Clf = LocalOutlierFactor(n_neighbors=Parameters[0], novelty=True)
        Clf.fit(TrnSet_X)
    elif Classifier == 'EllipticEnvelope':
        # parameters = [0]
        Clf = EllipticEnvelope(contamination=Parameters[0]).fit(TrnSet_X)
    elif Classifier == 'IsolationForest':
        # Parameters = [100, 0]
        Clf = IsolationForest(n_jobs=-1, n_estimators=Parameters[0],
                              contamination=Parameters[1], bootstrap=False).fit(TrnSet_X)
    elif Classifier == 'OneClassSVM':
        # parameters = [0.001, 01]
        Clf = svm.OneClassSVM(gamma=Parameters[0], kernel='rbf', nu=Parameters[1])
        Clf.fit(TrnSet_X)
    else:
        raise ValueError('No such Algorithm found !!!')

    Decision = Clf.decision_function(TrnSet_X)
    maxDistance = max(Decision)

    return Clf, maxDistance


def Clf_GetDecisions(Clf, TstSet_X, maxDistance):
    """
    Get the decisions of a classifier for the test set.
    If an observation's decision > 1, it's an outlier.

    :param Clf: The classifier
    :param TstSet_X: The test set
    :param maxDistance: The maximum distance of the train set
    :return: The decision for the test observations
    """

    Decisions = Clf.decision_function(TstSet_X)
    Decisions = Decisions / maxDistance

    return Decisions


def Clf_GetPredictions(Clf, TstSet_X):
    """
    Get predictions from aclassifier.

    :param Clf: The classifier
    :param TstSet_X: The test samples
    :return: The predictions of the samples
    """

    Predictions = Clf.predict(TstSet_X)

    return Predictions


def Clf_GetTotalPredictions(Predictions):
    """
    Use the predictions of samples to get their total predictions.

    :param Predictions: The predictions of samples
    :return: The total predictions
    """

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


def Clf_Evaluate(TrnSet_Y, TstSet_Y, Prediction, EvaluationMetrics):
    """
    Compute evaluation metrics.

    :param TrnSet_Y: Train samples
    :param TstSet_Y: Test samples
    :param Prediction: Predictions
    :param EvaluationMetrics: An object from EvaluationMetrics class in s5_Class_EvaluationMetrics_v000
    :return: The updated EvaluationMetrics
    """

    Accuracy = accuracy_score(TstSet_Y, Prediction)
    F1Score = f1_score(TstSet_Y, Prediction)
    ROC = roc_auc_score(TstSet_Y, Prediction)
    CunfusionMatrix = confusion_matrix(TstSet_Y, Prediction, labels=[-1, 1])
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


def CalculateMeanMetrics(EvaluationMetrics_Folds, EvaluationMetrics):
    """
    Use an EvaluationMetric object, to calculate the mean of metrics.
    Save them in a different EvaluationMetric object.

    :param EvaluationMetrics_Folds: The object with the metrics.
    :param EvaluationMetrics: The object in which the mean values will be stored.
    :return: The updated EvaluationMetrics
    """

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


def AppendUserMetrics(EvaluationMetrics_User, EvaluationMetrics_All):
    """

    :param EvaluationMetrics_User:
    :param EvaluationMetrics_All:
    :return:
    """

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
