"""
This script was created at 20-Sep-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

from sklearn import svm
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor

from s4_GetResults_ClfSuperClass import ClfSuperClass


#  ============== #
#    Functions    #
# =============== #
def clf_train(clf_name, parameters, train_data):

    if clf_name == 'LocalOutlierFactor':
        clf = LocalOutlierFactor(n_neighbors=parameters[0], novelty=True)  # parameters = [3]

    elif clf_name == 'OneClassSVM':
        clf = svm.OneClassSVM(gamma=parameters[0], kernel='rbf', nu=parameters[1])  # parameters = [0.001, 01]

    else:
        raise ValueError('No such Algorithm found !!!')

    clf.fit(train_data)
    distances = clf.decision_function(train_data)
    max_distance = max(distances)

    return clf, max_distance


#  ============ #
#    Classes    #
# ============= #
class SimpleClf(ClfSuperClass):

    def __init__(self, original_user: str, data_type: str,
                 features_df: pd.DataFrame,
                 final_features: list,
                 scalar, clfs_parameters):

        self.scalar = scalar
        self.scalar_trained = {}

        self.orgu_x_trns = {}
        self.orgu_x_tsts = {}

        self.clfs_parameters = clfs_parameters
        self.clfs_trained = {}
        self.clfs_max_distance = {}

        users_data = {}
        for user in set(features_df['User']):
            users_data[user] = features_df.loc[features_df['User'] == user][final_features]
            users_data[user] = users_data[user].reset_index(drop=True)

        super(SimpleClf, self).__init__(original_user, data_type, users_data)

    def train_classifier(self) -> None:

        x = self.users_data[self.original_user]

        kf = KFold(n_splits=self.folds, shuffle=True, random_state=2)
        for fold, [trn_indexes, tst_indexes] in enumerate(kf.split(x)):

            # Select train and test set for original user
            x_trn, x_tst = x.iloc[trn_indexes], x.iloc[tst_indexes]
            x_trn, x_tst = x_trn.to_numpy(), x_tst.to_numpy()
            self.orgu_x_trns[fold], self.orgu_x_tsts[fold] = x_trn, x_tst

            # Scale data
            if self.scalar != None:
                scalar = self.scalar().fit(x_trn)
                x_trn, x_tst = scalar.transform(x_trn), scalar.transform(x_tst)
                self.scalar_trained[fold] = scalar

            # Train models
            self.clfs_trained[fold] = []
            self.clfs_max_distance[fold] = []
            for clf_name in self.clfs_parameters:
                for parameters in self.clfs_parameters[clf_name]:
                    clf, max_distance = clf_train(clf_name, parameters, x_trn)
                    self.clfs_trained[fold].append(clf)
                    self.clfs_max_distance[fold].append(max_distance)

        return

    def get_decisions(self):

        for fold in range(self.folds):
            for user in self.users_data:

                if user not in self.users_decisions:
                    self.users_decisions[user] = {}
                    self.users_predictions[user] = {}

                if user == self.original_user:
                    x_tst = self.orgu_x_tsts[fold]
                else:
                    x_tst = self.users_data[user]

                # Scale data
                if self.scalar != None:
                    scalar = self.scalar_trained[fold]
                    x_tst = scalar.transform(x_tst)

                decision_total = np.zeros(x_tst.shape[0])
                for idx, clf in enumerate(self.clfs_trained[fold]):
                    decision = clf.decision_function(x_tst) / self.clfs_max_distance[fold][idx]
                    decision_total += decision
                self.users_decisions[user][fold] = decision_total

                predictions = np.empty(x_tst.shape[0])
                for idx in range(x_tst.shape[0]):
                    predictions[idx] = 1 if decision_total[idx] > 0 else -1
                self.users_predictions[user][fold] = predictions

        return self.users_decisions
