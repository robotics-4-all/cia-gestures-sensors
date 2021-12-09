"""
This script was created at 20-Sep-21
author: eachrist

"""
# ============= #
#    Imports    #
# ============= #
from sklearn.preprocessing import StandardScaler

from s__Helpers_Functions import frange
from s3_GetResults_SimpleClassifier_20211130 import SimpleClassifier


# ============= #
#    Classes    #
# ============= #
# Accelerometer Class
class AccClassifier(SimpleClassifier):

    def __init__(self):

        final_features = ['Mean', 'STD', 'Max', 'Min', 'Percentile25', 'Percentile50', 'Percentile75',
                          'Kurtosis', 'Skewness', 'Amplitude2', 'Frequency2']

        scalar = StandardScaler

        clf_name = 'OneClassSVM'
        parameters = []
        for nu in frange(0.3, 0.5, 0.02):
            for gamma in frange(0.0005, 0.1, 0.005):
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}

        super(AccClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=50)


class GyrClassifier(SimpleClassifier):

    def __init__(self):

        final_features = ['Mean', 'STD', 'Max', 'Min', 'Percentile25', 'Percentile50', 'Percentile75',
                          'Kurtosis', 'Skewness', 'Amplitude2', 'Frequency2']

        scalar = StandardScaler

        clf_name = 'OneClassSVM'
        parameters = []
        for nu in frange(0.3, 0.5, 0.02):
            for gamma in frange(0.0005, 0.1, 0.005):
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}

        super(GyrClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=50)


class SwpClassifier(SimpleClassifier):

    def __init__(self):

        final_features = ['Duration', 'MeanX', 'MeanY', 'StartStopLength', 'ScreenPercentage',
                          'TraceProjection', 'StartVelocity', 'StopVelocity',
                          'AccelerationHor', 'AccelerationVer', 'Slope', 'MeanSquareError', 'CoefDetermination']

        scalar = StandardScaler

        clf_name = 'OneClassSVM'
        parameters = []
        for nu in frange(0.3, 0.5, 0.02):
            for gamma in frange(0.0005, 0.1, 0.005):
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}

        super(SwpClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=50)


class TapClassifier(SimpleClassifier):

    def __init__(self):

        final_features = ['Duration']

        scalar = StandardScaler

        clf_name = 'OneClassSVM'
        parameters = []
        for nu in frange(0.3, 0.5, 0.01):
            for gamma in frange(0.0005, 0.1, 0.005):
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}

        super(TapClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=50)
