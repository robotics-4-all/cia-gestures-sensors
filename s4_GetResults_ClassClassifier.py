"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import numpy as np
import pandas as pd
from statistics import median
from sklearn import svm
from sklearn.neighbors import LocalOutlierFactor


#  ============== #
#    Functions    #
# =============== #
def define_classifiers(clf_name, parameters):

    if clf_name == 'LocalOutlierFactor':
        clf = LocalOutlierFactor(n_neighbors=parameters[0], novelty=True)  # parameters = [3]
    elif clf_name == 'OneClassSVM':
        clf = svm.OneClassSVM(gamma=parameters[0], kernel='rbf', nu=parameters[1])  # parameters = [0.001, 01]
    elif clf_name == 'OneClassSVM_rbf_dflt':
        clf = svm.OneClassSVM(kernel='rbf')
    elif clf_name == 'LocalOutlierFactor_dflt':
        clf = LocalOutlierFactor(novelty=True)
    else:
        raise ValueError('No such Algorithm found !!!')

    return clf


def get_predictions(probabilities: np.ndarray):

    predictions = np.empty(probabilities.shape[0])
    for sample_idx in range(probabilities.shape[0]):
        predictions[sample_idx] = 1 if probabilities[sample_idx] > 0 else -1

    return predictions


#  ============ #
#    Classes    #
# ============= #
class Classifier:

    def __init__(self, final_features: list, scalar, clfs_parameters: dict, num_of_clf_that_decide: int):

        self.final_features = final_features
        self.scalar = scalar
        self.classifiers = []
        for clf_name in clfs_parameters:
            for parameters in clfs_parameters[clf_name]:
                self.classifiers.append(define_classifiers(clf_name, parameters))
        self.classifiers_max_distances = []
        self.classifiers_median_distances = []
        self.clfs_dec = num_of_clf_that_decide

    def train_classifiers(self, data: pd.DataFrame):

        if data.shape[0] != 0:
            data = data[self.final_features].to_numpy()
            if self.scalar != None:
                self.scalar = self.scalar().fit(data)
                data = self.scalar.transform(data)
            # Train models
            for clf in self.classifiers:
                clf.fit(data)
                distances = clf.decision_function(data)
                self.classifiers_max_distances.append(max(distances))
                self.classifiers_median_distances.append(median(distances))

        return

    def get_probabilities(self, data: pd.DataFrame):

        probabilities_avg = np.zeros(data.shape[0])
        if data.shape[0] != 0:
            data = data[self.final_features].to_numpy()
            if self.scalar != None:
                data = self.scalar.transform(data)
            for idx in np.argpartition(self.classifiers_median_distances, self.clfs_dec - 1)[:self.clfs_dec]:
                clf = self.classifiers[idx]
                probabilities = clf.decision_function(data) / self.classifiers_max_distances[idx]
                for sample_idx in range(data.shape[0]):
                    if probabilities[sample_idx] > 1:
                        probabilities[sample_idx] = 1
                    if probabilities[sample_idx] < -1:
                        probabilities[sample_idx] = -1
                probabilities_avg += probabilities
            probabilities_avg /= self.clfs_dec

        return probabilities_avg
