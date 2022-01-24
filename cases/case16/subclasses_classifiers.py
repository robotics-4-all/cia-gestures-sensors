"""
This script was created at 20-Sep-21
author: eachrist

"""
# ============= #
#    Imports    #
# ============= #
import numpy as np
from sklearn.preprocessing import StandardScaler
from s4_GetResults_ClassClassifier import Classifier


# ============= #
#    Classes    #
# ============= #
# Accelerometer Class
class AccClassifier(Classifier):

    def __init__(self, param):

        final_features = ['Mean_x', 'Mean_y', 'Mean_magnitude',
                          'STD_x', 'STD_y', 'STD_magnitude',
                          'Max_x', 'Max_y', 'Max_magnitude',
                          'Min_x', 'Min_y', 'Min_magnitude',
                          'Percentile25_x', 'Percentile25_y', 'Percentile25_magnitude',
                          'Percentile50_x', 'Percentile50_y', 'Percentile50_magnitude',
                          'Percentile75_x', 'Percentile75_y', 'Percentile75_magnitude',
                          'Kurtosis_x', 'Kurtosis_y', 'Kurtosis_magnitude',
                          'Skewness_x', 'Skewness_y', 'Skewness_magnitude',
                          'Amplitude1_x', 'Amplitude1_y', 'Amplitude1_magnitude',
                          'Amplitude2_x',
                          'Frequency2_x', 'Frequency2_y', 'Frequency2_magnitude',
                          'MeanFrequency_x']

        scalar = StandardScaler
        clf_name = 'OneClassSVM'
        parameters = []
        for nu in np.arange(0.13, 0.16, 0.01).round(2).tolist():
            for gamma in np.arange(0.0010, 0.0020, 0.00005).round(5).tolist():
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}
        super(AccClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=50)


class GyrClassifier(Classifier):

    def __init__(self, param):

        final_features = ['Mean_x', 'Mean_y', 'Mean_magnitude',
                          'STD_y',
                          'Max_x',
                          'Min_x', 'Min_y', 'Min_magnitude',
                          'Percentile75_x',
                          'Kurtosis_x', 'Kurtosis_y', 'Kurtosis_magnitude',
                          'Skewness_x', 'Skewness_y', 'Skewness_magnitude',
                          'Amplitude1_x',
                          'Frequency2_x', 'Frequency2_y', 'Frequency2_magnitude',
                          'MeanFrequency_x']

        scalar = StandardScaler
        clf_name = 'OneClassSVM'
        parameters = []
        for nu in np.arange(0.37, 0.40, 0.01).round(2).tolist():
            for gamma in np.arange(0.06, 0.07, 0.0005).round(5).tolist():
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}
        super(GyrClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=50)


class SwpClassifier(Classifier):

    def __init__(self, param):

        final_features = ['Duration', 'MeanX', 'MeanY',
                          'TraceLength', 'TraceProjection',
                          'StartVelocity', 'StopVelocity', 'AccelerationHor', 'AccelerationVer',
                          'Slope', 'MeanSquareError', 'CoefDetermination']

        scalar = StandardScaler
        clf_name = 'OneClassSVM'
        parameters = []
        for nu in np.arange(0.22, 0.24, 0.01).round(2).tolist():
            for gamma in np.arange(0.06, 0.07, 0.0005).round(5).tolist():
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}
        super(SwpClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=30)


class TapClassifier(Classifier):

    def __init__(self, param):

        final_features = ['Duration']

        scalar = StandardScaler
        clf_name = 'OneClassSVM'
        parameters = []
        for nu in np.arange(0.51, 0.54, 0.01).round(2).tolist():
            for gamma in np.arange(0.700, 0.900, 0.025).round(3).tolist():
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}
        super(TapClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=30)
