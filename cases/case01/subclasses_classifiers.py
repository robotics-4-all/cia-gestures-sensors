"""
This script was created at 20-Sep-21
author: eachrist

"""
# ============= #
#    Imports    #
# ============= #
import itertools
from sklearn.preprocessing import StandardScaler
from s4_GetResults_ClassClassifier import Classifier


# ============= #
#    Classes    #
# ============= #
# Accelerometer Class
class AccClassifier(Classifier):

    def __init__(self, lvl0_features: list):

        lvl1_features = {
            'unique': [],
            'lvl0_depended': ['Mean', 'STD', 'Max', 'Min',
                              'Percentile25', 'Percentile50', 'Percentile75',
                              'Kurtosis', 'Skewness', 'Amplitude2', 'Frequency2']}

        final_features = lvl1_features['unique'] + \
                         ['_'.join(ftr) for ftr in itertools.product(lvl1_features['lvl0_depended'], lvl0_features)]

        scalar = StandardScaler
        clf_name = 'OneClassSVM_rbf_dflt'
        parameters = [None]
        clfs_parameters = {clf_name: parameters}
        super(AccClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)


class GyrClassifier(Classifier):

    def __init__(self, lvl0_features: list):
        lvl1_features = {
            'unique': [],
            'lvl0_depended': ['Mean', 'STD', 'Max', 'Min',
                              'Percentile25', 'Percentile50', 'Percentile75',
                              'Kurtosis', 'Skewness', 'Amplitude2', 'Frequency2']}

        final_features = lvl1_features['unique'] + \
                         ['_'.join(ftr) for ftr in itertools.product(lvl1_features['lvl0_depended'], lvl0_features)]

        scalar = StandardScaler
        clf_name = 'OneClassSVM_rbf_dflt'
        parameters = [None]
        clfs_parameters = {clf_name: parameters}
        super(GyrClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)


class SwpClassifier(Classifier):

    def __init__(self, param):

        final_features = ['Duration', 'MeanX', 'MeanY', 'StartStopLength', 'ScreenPercentage',
                          'TraceProjection', 'StartVelocity', 'StopVelocity',
                          'AccelerationHor', 'AccelerationVer', 'Slope', 'MeanSquareError', 'CoefDetermination']

        scalar = StandardScaler
        clf_name = 'OneClassSVM_rbf_dflt'
        parameters = [None]
        clfs_parameters = {clf_name: parameters}
        super(SwpClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)


class TapClassifier(Classifier):

    def __init__(self, param):

        final_features = ['Duration']

        scalar = StandardScaler
        clf_name = 'OneClassSVM_rbf_dflt'
        parameters = [None]
        clfs_parameters = {clf_name: parameters}
        super(TapClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)
