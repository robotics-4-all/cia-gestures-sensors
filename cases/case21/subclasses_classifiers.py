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

# ==================== #
#    Final Features    #
# ==================== #
features = {
    'acc': ['Mean_x', 'Mean_y', 'Mean_magnitude',
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
            'MeanFrequency_x'],

    'gyr': ['Mean_x', 'Mean_y', 'Mean_magnitude',
            'STD_y',
            'Max_x',
            'Min_x', 'Min_y', 'Min_magnitude',
            'Percentile75_x',
            'Kurtosis_x', 'Kurtosis_y', 'Kurtosis_magnitude',
            'Skewness_x', 'Skewness_y', 'Skewness_magnitude',
            'Amplitude1_x',
            'Frequency2_x', 'Frequency2_y', 'Frequency2_magnitude',
            'MeanFrequency_x'],

    'swp': ['Duration', 'MeanX', 'MeanY',
            'TraceLength', 'TraceProjection',
            'StartVelocity', 'StopVelocity', 'AccelerationHor', 'AccelerationVer',
            'Slope', 'MeanSquareError', 'CoefDetermination'],

    'tap': ['Duration']
}

# ================ #
#    Parameters    #
# ================ #
dict_nu = {
    'acc': np.arange(0.001, 0.1, 0.005).round(3).tolist(),
    'gyr': np.arange(0.001, 0.1, 0.005).round(3).tolist(),
    'swp': np.arange(0.001, 0.021, 0.001).round(3).tolist(),
    'tap': np.arange(0.001, 0.021, 0.001).round(3).tolist()
}

dict_gamma = {
    'acc': np.arange(0.00001, 0.00021, 0.00001).round(5).tolist(),
    'gyr': np.arange(0.0001, 0.0021, 0.0001).round(4).tolist(),
    'swp': np.arange(0.0001, 0.0021, 0.0001).round(4).tolist(),
    'tap': np.arange(0.7, 0.795, 0.005).round(3).tolist()
}


# ============= #
#    Classes    #
# ============= #
# Accelerometer Class
class AccClassifier(Classifier):

    def __init__(self, param):

        final_features = features['acc']
        scalar = StandardScaler
        clf_name = 'OneClassSVM'
        parameters = []
        for nu in dict_nu['acc']:
            for gamma in dict_gamma['acc']:
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}
        super(AccClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=30)


class GyrClassifier(Classifier):

    def __init__(self, param):

        final_features = features['gyr']
        scalar = StandardScaler
        clf_name = 'OneClassSVM'
        parameters = []
        for nu in dict_nu['gyr']:
            for gamma in dict_gamma['gyr']:
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}
        super(GyrClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=60)


class SwpClassifier(Classifier):

    def __init__(self, param):

        final_features = features['swp']
        scalar = StandardScaler
        clf_name = 'OneClassSVM'
        parameters = []
        for nu in dict_nu['swp']:
            for gamma in dict_gamma['swp']:
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}
        super(SwpClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=60)


class TapClassifier(Classifier):

    def __init__(self, param):

        final_features = features['tap']
        scalar = StandardScaler
        clf_name = 'OneClassSVM'
        parameters = []
        for nu in dict_nu['tap']:
            for gamma in dict_gamma['tap']:
                parameters.append([gamma, nu])
        clfs_parameters = {clf_name: parameters}
        super(TapClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=60)
