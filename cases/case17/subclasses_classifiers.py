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

# ================ #
#    Parameters    #
# ================ #
dict_nu = {
    'acc': np.arange(0.01, 0.36, 0.02).round(2).tolist(),
    'gyr': np.arange(0.01, 0.70, 0.04).round(2).tolist(),
    'swp': np.arange(0.01, 0.53, 0.03).round(2).tolist(),
    'tap': np.arange(0.24, 0.76, 0.03).round(2).tolist(),
}

dict_gamma = {
    'acc': np.arange(0.001, 0.050, 0.002).round(3).tolist(),
    'gyr': np.arange(0.01, 0.26, 0.01).round(2).tolist(),
    'swp': np.arange(0.01, 0.26, 0.01).round(2).tolist(),
    'tap': np.arange(0.01, 1, 0.04).round(2).tolist(),
}


# ============= #
#    Classes    #
# ============= #
# Accelerometer Class
class AccClassifier(Classifier):

    def __init__(self, nu_idx, gamma_idx):

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
        parameters = [[dict_gamma['acc'][gamma_idx], dict_nu['acc'][nu_idx]]]
        clfs_parameters = {clf_name: parameters}
        super(AccClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)


class GyrClassifier(Classifier):

    def __init__(self, nu_idx, gamma_idx):

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
        parameters = [[dict_gamma['gyr'][gamma_idx], dict_nu['gyr'][nu_idx]]]
        clfs_parameters = {clf_name: parameters}
        super(GyrClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)


class SwpClassifier(Classifier):

    def __init__(self, nu_idx, gamma_idx):

        final_features = ['Duration', 'MeanX', 'MeanY',
                          'TraceLength', 'TraceProjection',
                          'StartVelocity', 'StopVelocity', 'AccelerationHor', 'AccelerationVer',
                          'Slope', 'MeanSquareError', 'CoefDetermination']

        scalar = StandardScaler
        clf_name = 'OneClassSVM'
        parameters = [[dict_gamma['swp'][gamma_idx], dict_nu['swp'][nu_idx]]]
        clfs_parameters = {clf_name: parameters}
        super(SwpClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)


class TapClassifier(Classifier):

    def __init__(self, nu_idx, gamma_idx):

        final_features = ['Duration']

        scalar = StandardScaler
        clf_name = 'OneClassSVM'
        parameters = [[dict_gamma['tap'][gamma_idx], dict_nu['tap'][nu_idx]]]
        clfs_parameters = {clf_name: parameters}
        super(TapClassifier, self).__init__(final_features, scalar, clfs_parameters, num_of_clf_that_decide=1)
