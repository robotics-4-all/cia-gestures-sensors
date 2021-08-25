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


def Clf_Evaluate(DFF_Org_Trn, Predictions_Org_Tst, Predictions_Atts, EvaluationMetrics):
    """
    Compute evaluation metrics.

    :param DFF_Org_Trn:
    :param Predictions_Org_Tst:
    :param Predictions_Atts:
    :param EvaluationMetrics: An object from EvaluationMetrics class in s5_Class_EvaluationMetrics_v001
    :return: The updated EvaluationMetrics
    """

    OrgTrnSize = len(DFF_Org_Trn)
    OrgTstSize = len(Predictions_Org_Tst)
    AttNum = len(Predictions_Atts)
    Att_TotalSize = 0
    for idx_Att in range(len(Predictions_Atts)):
        Att_TotalSize += len(Predictions_Atts[idx_Att])
    Att_AvgSize = Att_TotalSize / AttNum

    FalseRejections = 0
    for idx_Sample in range(len(Predictions_Org_Tst)):
        if Predictions_Org_Tst[idx_Sample] == -1:
            FalseRejections += 1
    FRR = FalseRejections / OrgTstSize

    TotalFalseAcceptance = 0
    Sum_FAR_Att = 0
    for idx_Att in range(len(Predictions_Atts)):
        FalseAcceptance = 0
        for idx_Sample in range(len(Predictions_Atts[idx_Att])):
            if Predictions_Atts[idx_Att][idx_Sample] == 1:
                FalseAcceptance += 1
        FAR_Att = FalseAcceptance / len(Predictions_Atts[idx_Att])
        Sum_FAR_Att += FAR_Att
        TotalFalseAcceptance = TotalFalseAcceptance + FalseAcceptance
    FAR_Total = TotalFalseAcceptance / Att_TotalSize
    FAR_Avg = Sum_FAR_Att / AttNum

    Num_Of_Unlocks = 0 # Number of unlocks an original user forced to do
    Threshold = 35
    Confidence = 60
    for idx_Sample in range(len(Predictions_Org_Tst)):
        if Confidence < Threshold:
            Confidence = 60
            Num_Of_Unlocks += 1
        Sample = Predictions_Org_Tst[idx_Sample]
        if Sample == 1:
            Confidence += 5
        else:
            Confidence -= 15
        if Confidence > 100:
            Confidence = 100
    FRR_Conf = Num_Of_Unlocks / OrgTstSize

    Sum_Num_Of_Accepted = 0
    for idx_Att in range(len(Predictions_Atts)):
        Num_Of_Accepted = 0 # Number of successful attempts made by the attacker until locked
        Threshold = 35
        Confidence = 60
        for idx_Sample in range(len(Predictions_Atts[idx_Att])):
            Sample = Predictions_Atts[idx_Att][idx_Sample]
            if Sample == 1:
                Confidence += 5
            else:
                Confidence -= 15
            if Confidence > 100:
                Confidence = 100
            if Confidence >= Threshold:
                Num_Of_Accepted += 1
            else:
                break
        Sum_Num_Of_Accepted += Num_Of_Accepted
    Num_Of_Accepted_Avg = Sum_Num_Of_Accepted / AttNum

    EvaluationMetrics.setOrgTrnSize(OrgTrnSize)
    EvaluationMetrics.setOrgTstSize(OrgTstSize)
    EvaluationMetrics.setAttNum(AttNum)
    EvaluationMetrics.setAtt_TotalSize(Att_TotalSize)
    EvaluationMetrics.setAtt_AvgSize(Att_AvgSize)
    EvaluationMetrics.setFRR(FRR)
    EvaluationMetrics.setFRR_Conf(FRR_Conf)
    EvaluationMetrics.setFAR_Total(FAR_Total)
    EvaluationMetrics.setFAR_Avg(FAR_Avg)
    EvaluationMetrics.setNum_Of_Unlocks(Num_Of_Unlocks)
    EvaluationMetrics.setNum_Of_Accepted_Avg(Num_Of_Accepted_Avg)

    return EvaluationMetrics


def CalculateMeanMetrics(EvaluationMetrics_Folds, EvaluationMetrics):
    """
    Use an EvaluationMetric object, to calculate the mean of metrics.
    Save them in a different EvaluationMetric object.

    :param EvaluationMetrics_Folds: The object with the metrics.
    :param EvaluationMetrics: The object in which the mean values will be stored.
    :return: The updated EvaluationMetrics
    """

    OrgTrnSize = np.mean(EvaluationMetrics_Folds.getOrgTrnSize())
    OrgTstSize = np.mean(EvaluationMetrics_Folds.getOrgTstSize())
    AttNum = np.mean(EvaluationMetrics_Folds.getAttNum())
    Att_TotalSize = np.mean(EvaluationMetrics_Folds.getAtt_TotalSize())
    Att_AvgSize = np.mean(EvaluationMetrics_Folds.getAtt_AvgSize())
    FRR = np.mean(EvaluationMetrics_Folds.getFRR())
    FRR_Conf = np.mean(EvaluationMetrics_Folds.getFRR_Conf())
    FAR_Total = np.mean(EvaluationMetrics_Folds.getFAR_Total())
    FAR_Avg = np.mean(EvaluationMetrics_Folds.getFAR_Avg())
    Num_Of_Unlocks = np.mean(EvaluationMetrics_Folds.getNum_Of_Unlocks())
    Num_Of_Accepted_Avg = np.mean(EvaluationMetrics_Folds.getNum_Of_Accepted_Avg())

    OrgTrnSize_Std = stdev(EvaluationMetrics_Folds.getOrgTrnSize())
    OrgTstSize_Std = stdev(EvaluationMetrics_Folds.getOrgTstSize())
    AttNum_Std = stdev(EvaluationMetrics_Folds.getAttNum())
    Att_TotalSize_Std = stdev(EvaluationMetrics_Folds.getAtt_TotalSize())
    Att_AvgSize_Std = stdev(EvaluationMetrics_Folds.getAtt_AvgSize())
    FRR_Std = stdev(EvaluationMetrics_Folds.getFRR())
    FRR_Conf_Std = stdev(EvaluationMetrics_Folds.getFRR_Conf())
    FAR_Total_Std = stdev(EvaluationMetrics_Folds.getFAR_Total())
    FAR_Avg_Std = stdev(EvaluationMetrics_Folds.getFAR_Avg())
    Num_Of_Unlocks_Std = stdev(EvaluationMetrics_Folds.getNum_Of_Unlocks())
    Num_Of_Accepted_Avg_Std = stdev(EvaluationMetrics_Folds.getNum_Of_Accepted_Avg())

    EvaluationMetrics.setOrgTrnSize(OrgTrnSize)
    EvaluationMetrics.setOrgTstSize(OrgTstSize)
    EvaluationMetrics.setAttNum(AttNum)
    EvaluationMetrics.setAtt_TotalSize(Att_TotalSize)
    EvaluationMetrics.setAtt_AvgSize(Att_AvgSize)
    EvaluationMetrics.setFRR(FRR)
    EvaluationMetrics.setFRR_Conf(FRR_Conf)
    EvaluationMetrics.setFAR_Total(FAR_Total)
    EvaluationMetrics.setFAR_Avg(FAR_Avg)
    EvaluationMetrics.setNum_Of_Unlocks(Num_Of_Unlocks)
    EvaluationMetrics.setNum_Of_Accepted_Avg(Num_Of_Accepted_Avg)

    EvaluationMetrics.setOrgTrnSize_Std(OrgTrnSize_Std)
    EvaluationMetrics.setOrgTstSize_Std(OrgTstSize_Std)
    EvaluationMetrics.setAttNum_Std(AttNum_Std)
    EvaluationMetrics.setAtt_TotalSize_Std(Att_TotalSize_Std)
    EvaluationMetrics.setAtt_AvgSize_Std(Att_AvgSize_Std)
    EvaluationMetrics.setFRR_Std(FRR_Std)
    EvaluationMetrics.setFRR_Conf_Std(FRR_Conf_Std)
    EvaluationMetrics.setFAR_Total_Std(FAR_Total_Std)
    EvaluationMetrics.setFAR_Avg_Std(FAR_Avg_Std)
    EvaluationMetrics.setNum_Of_Unlocks_Std(Num_Of_Unlocks_Std)
    EvaluationMetrics.setNum_Of_Accepted_Avg_Std(Num_Of_Accepted_Avg_Std)

    return EvaluationMetrics
