"""
This script was created at 20-Sep-21
author: eachrist

"""
# ============= #
#    Imports    #
# ============= #
from sklearn.preprocessing import StandardScaler

from s__Helpers_Functions import frange
from s4_GetResults_SimpleClassifier import SimpleClassifier


# ============= #
#    Classes    #
# ============= #
# Accelerometer Class
class AccClassifier(SimpleClassifier):

    def __init__(self):

        final_features = ['Window', 'Mean', 'STD', 'Max', 'Min', 'Range',
                          'Percentile25', 'Percentile50', 'Percentile75',
                          'Entropy', 'Kurtosis', 'Skewness',
                          'Amplitude1', 'Amplitude2', 'Frequency2', 'MeanFrequency']

        scalar = StandardScaler

        clf_name = 'OneClassSVM_rbf_dflt'
        parameters = [None]
        clfs_parameters = {clf_name: parameters}

        super(AccClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)


class GyrClassifier(SimpleClassifier):

    def __init__(self):

        final_features = ['Window', 'Mean', 'STD', 'Max', 'Min', 'Range',
                          'Percentile25', 'Percentile50', 'Percentile75',
                          'Entropy', 'Kurtosis', 'Skewness',
                          'Amplitude1', 'Amplitude2', 'Frequency2', 'MeanFrequency']

        scalar = StandardScaler

        clf_name = 'OneClassSVM_rbf_dflt'
        parameters = [None]
        clfs_parameters = {clf_name: parameters}

        super(GyrClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)


class SwpClassifier(SimpleClassifier):

    def __init__(self):

        final_features = ['Duration', 'MeanX', 'MeanY',
                          'TraceLength', 'StartStopLength', 'TraceProjection', 'ScreenPercentage',
                          'StartVelocity', 'StopVelocity', 'AccelerationHor', 'AccelerationVer',
                          'Slope', 'MeanSquareError', 'MeanAbsError', 'MedianAbsError', 'CoefDetermination']

        scalar = StandardScaler

        clf_name = 'OneClassSVM_rbf_dflt'
        parameters = [None]
        clfs_parameters = {clf_name: parameters}

        super(SwpClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)


class TapClassifier(SimpleClassifier):

    def __init__(self):
        final_features = ['Duration']

        scalar = StandardScaler

        clf_name = 'OneClassSVM_rbf_dflt'
        parameters = [None]
        clfs_parameters = {clf_name: parameters}

        super(TapClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)
