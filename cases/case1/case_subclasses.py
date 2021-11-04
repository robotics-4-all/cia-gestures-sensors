"""
This script was created at 20-Sep-21
author: eachrist

"""
# ============= #
#    Imports    #
# ============= #
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from s0_Helpers_Functions import frange
from s4_GetResults_ClfSimple import SimpleClf


# ============= #
#    Classes    #
# ============= #
class AccClf(SimpleClf):

    def __init__(self, original_user: str, features_df: pd.DataFrame):

        data_type = 'acc'

        final_features = ['Mean', 'STD', 'Max', 'Min', 'Range',
                          'Percentile25', 'Percentile50', 'Percentile75',
                          'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2']

        scalar = MinMaxScaler

        clf_name = 'LocalOutlierFactor'
        parameters = [[3], [5], [7]]

        clfs_parameters = {clf_name: parameters}

        super(AccClf, self).__init__(original_user, data_type,
                                     features_df, final_features,
                                     scalar, clfs_parameters)


class GyrClf(SimpleClf):

    def __init__(self, original_user: str, features_df: pd.DataFrame):

        data_type = 'gyr'

        final_features = ['Mean', 'STD', 'Max', 'Min', 'Range',
                          'Percentile25', 'Percentile50', 'Percentile75',
                          'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2']

        scalar = MinMaxScaler

        clf_name = 'LocalOutlierFactor'
        parameters = [[3], [5], [7]]

        clfs_parameters = {clf_name: parameters}

        super(GyrClf, self).__init__(original_user, data_type,
                                     features_df, final_features,
                                     scalar, clfs_parameters)


class SwpClf(SimpleClf):

    def __init__(self, original_user: str, features_df: pd.DataFrame):

        data_type = 'swp'

        final_features = ['TraceLengthHorizontal', 'TraceLengthVertical',
                          'Slope', 'MeanSquareError', 'MeanAbsError', 'MedianAbsError', 'CoefDetermination',
                          'AccelerationHorizontal', 'AccelerationVertical',
                          'MeanY']

        scalar = MinMaxScaler

        clf_name = 'OneClassSVM'
        parameters = []

        for nu in frange(0.01, 0.3, 0.1):
            for gamma in frange(5.00, 10.00, 0.5):
                parameters.append([gamma, nu])

        clfs_parameters = {clf_name: parameters}

        super(SwpClf, self).__init__(original_user, data_type,
                                     features_df, final_features,
                                     scalar, clfs_parameters)
