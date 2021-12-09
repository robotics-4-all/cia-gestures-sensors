"""
This script was created at 20-Sep-21
author: eachrist

"""
# ============= #
#    Imports    #
# ============= #
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from s4_GetResults_ClfSimple import SimpleClf
from s4_GetResults_ClfSuperClass import ClfSuperClass


# ================ #
#    Parameters    #
# ================ #
folds = 10


# ============= #
#    Classes    #
# ============= #
# Accelerometer Class
class AccClf(SimpleClf):

    def __init__(self, original_user: str, features_df: pd.DataFrame):

        data_type = 'acc'

        final_features = ['Mean', 'STD', 'Max', 'Min', 'Percentile25', 'Percentile50', 'Percentile75',
                          'Kurtosis', 'Skewness', 'Amplitude2', 'Frequency2']

        scalar = MinMaxScaler

        clf_name = 'OneClassSVM_rbf_dflt'
        parameters = [[None]]

        clfs_parameters = {clf_name: parameters}

        super(AccClf, self).__init__(folds, original_user, data_type,
                                     features_df, final_features,
                                     scalar, clfs_parameters, clfs_num=1)


# Gyroscope Class
class GyrClf(SimpleClf):

    def __init__(self, original_user: str, features_df: pd.DataFrame):

        data_type = 'gyr'

        final_features = ['Mean', 'STD', 'Max', 'Min', 'Percentile25', 'Percentile50', 'Percentile75',
                          'Kurtosis', 'Skewness', 'Amplitude2', 'Frequency2']

        scalar = MinMaxScaler

        clf_name = 'OneClassSVM_rbf_dflt'
        parameters = [[None]]

        clfs_parameters = {clf_name: parameters}

        super(GyrClf, self).__init__(folds, original_user, data_type,
                                     features_df, final_features,
                                     scalar, clfs_parameters, clfs_num=1)


# Swipes Class
class GesClf(SimpleClf):

    def __init__(self, original_user: str, features_df: pd.DataFrame):

        data_type = 'ges'

        final_features = ['Duration', 'MeanX', 'MeanY', 'StartStopLength', 'ScreenPercentage',
                          'TraceProjection', 'StartVelocity', 'StopVelocity',
                          'AccelerationHor', 'AccelerationVer', 'Slope', 'MeanSquareError', 'CoefDetermination']

        scalar = MinMaxScaler

        clf_name = 'OneClassSVM_rbf_dflt'
        parameters = [[None]]

        clfs_parameters = {clf_name: parameters}

        super(GesClf, self).__init__(folds, original_user, data_type,
                                     features_df, final_features,
                                     scalar, clfs_parameters, clfs_num=1)


# Ensemble Class
def get_final_decisions(dec_acc: np.ndarray, dec_gyr: np.ndarray, dec_swp: np.ndarray) -> np.ndarray:

    min_size = min(dec_acc.shape[0], dec_gyr.shape[0], dec_swp.shape[0])
    final_decision = dec_acc[:min_size] + dec_gyr[:min_size] + dec_swp[:min_size]

    return final_decision


class Ensemble(ClfSuperClass):

    def __init__(self, original_user: str, initial_decisions: dict):

        data_type = 'ttl'
        self.initial_decisions = initial_decisions

        super(Ensemble, self).__init__(folds, original_user, data_type)

    def get_final_predictions(self) -> dict:

        for fold in range(self.folds):
            for user in self.initial_decisions['acc']:

                if user not in self.users_decisions:
                    self.users_decisions[user] = {}
                    self.users_predictions[user] = {}

                dec_acc = self.initial_decisions['acc'][user][fold]
                dec_gyr = self.initial_decisions['gyr'][user][fold]
                dec_ges = self.initial_decisions['ges'][user][fold]

                self.users_decisions[user][fold] = get_final_decisions(dec_acc, dec_gyr, dec_ges)

                predictions = np.empty(self.users_decisions[user][fold].shape[0])
                for idx in range(self.users_decisions[user][fold].shape[0]):
                    predictions[idx] = 1 if self.users_decisions[user][fold][idx] > 0 else -1
                self.users_predictions[user][fold] = predictions

        return self.users_predictions
