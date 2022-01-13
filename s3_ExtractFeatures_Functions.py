"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os
import ast
import numpy as np
import pandas as pd
from tqdm import tqdm
from math import sqrt
from statistics import mean
from scipy.fftpack import fft
from scipy.stats import entropy, kurtosis, skew
from s__Helpers_Functions import linear_regression
from s0_cases_dictionaries import dict_cases
from s3_ExtractFeatures_Classes import FeaturesSns, FeaturesGes


# =============== #
#    Functions    #
# =============== #
def calculate_features_sns(user: int, module: str, data: np.ndarray, group: int, timestamp: float,
                           features_object: FeaturesSns, window: int, overlap: float, sample_rate: float):

    overlap = int(overlap * window)
    data_length = data.shape[0]

    if data_length <= 1:
        return features_object

    if data_length < window:
        window = data_length

    flag = True
    start = 0
    start_time = timestamp

    while data_length > 0:

        stop = start + window
        stop_time = timestamp + (stop - 1) * sample_rate

        features_object.setUser(user)
        features_object.setType(module)
        features_object.setStartTime(start_time)
        features_object.setStopTime(stop_time)
        features_object.setGroup(group)
        features_object.setWindow(stop-start)

        # Time features
        window_data = data[start:stop]
        features_object.setMean(window_data.mean())
        features_object.setSTD(window_data.std())
        features_object.setMax(window_data.max())
        features_object.setMin(window_data.min())
        features_object.setRange(window_data.ptp())
        features_object.setPercentile25(np.percentile(window_data, 25))
        features_object.setPercentile50(np.percentile(window_data, 50))
        features_object.setPercentile75(np.percentile(window_data, 75))
        features_object.setEntropy(entropy(window_data, base=2))
        features_object.setKurtosis(kurtosis(window_data))
        features_object.setSkewness(skew(window_data))

        # Frequency features
        window_dft = fft(window_data)
        freq = np.fft.fftfreq(stop - start)
        idx = (np.absolute(window_dft)).argsort()[-2:][::-1]
        features_object.setAmplitude1(np.absolute(window_dft[idx[0]]))
        features_object.setAmplitude2(np.absolute(window_dft[idx[1]]))
        features_object.setFrequency2(freq[idx[1]])
        features_object.setMeanFrequency(np.mean(freq))

        if flag:
            data_length += start - stop
            flag = False
        else:
            data_length += start - stop + overlap

        # Dynamic overlap
        if data_length + overlap < window:
            if data_length < overlap:
                break
            overlap = window - data_length

        start = stop - overlap
        start_time = timestamp + start * sample_rate

    return features_object


def extract_features_sns(case: str, screen_path: str, data: pd.DataFrame, module: str):

    print(' - Extracting ' + module + ' features.')
    path_df = os.path.join(screen_path, 'ftr_' + module[0:3] + '.csv')

    if not os.path.exists(path_df):

        features = dict_cases[case]['FeatureExtraction']['sns']['lvl0_ftr'][module[0:3]]
        sample_rate = dict_cases[case]['FeatureExtraction']['sns']['sample_rate']
        window = dict_cases[case]['FeatureExtraction']['sns']['window'][module[0:3]]
        overlap = dict_cases[case]['FeatureExtraction']['sns']['overlap'][module[0:3]]

        features_objects = {}
        for feature in features:
            features_objects[feature] = FeaturesSns()

        for user in tqdm(list(set(data['user']))):
            user_data = data.loc[data['user'] == user]
            timestamps = list(set(user_data['timestamp']))
            timestamps.sort()
            for idx, ts in enumerate(timestamps):
                for feature in features:
                    data_to_window = user_data.loc[data['timestamp'] == ts][feature].to_numpy()
                    features_objects[feature] = calculate_features_sns(user, module, data_to_window, idx, ts,
                                                                       features_objects[feature],
                                                                       window, overlap, sample_rate)

        df_features = features_objects[features[0]].create_dataframe(features[0], True)
        if len(features) > 1:
            for feature in features[1:]:
                df_temp = features_objects[feature].create_dataframe(feature, False)
                df_features = pd.concat([df_features, df_temp], axis=1)
        df_features.to_csv(path_df, index=False)
        print('     ' + module + ' features dataframe saved at: ', path_df)

    else:

        df_features = pd.read_csv(path_df)
        print('     ' + module + ' features dataframe loaded from: ', path_df)

    print('')

    return df_features


def calculate_features_ges(gesture: pd.Series, features_object: FeaturesGes,
                           normalize: bool, default_width: float, default_height: float):

    features_object.setUser(gesture['user'])
    features_object.setType(gesture['type'])
    features_object.setStartTime(gesture['time_start'])
    features_object.setStopTime(gesture['time_stop'])
    features_object.setDuration(gesture['duration'])

    if gesture['type'] == 'swipe':

        if type(gesture['data']) == str:
            ges_data = ast.literal_eval(gesture['data'])
        else:
            ges_data = gesture['data']
        x_poss, y_poss = [ges_data[0]['x0']], [ges_data[0]['y0']]
        for data in ges_data:
            x_poss.append(data['moveX'])
            y_poss.append(data['moveY'])
        if normalize:
            x_poss = [x * default_width / gesture['device_width'] for x in x_poss]
            y_poss = [y * default_height / gesture['device_height'] for y in y_poss]
        features_object.setMeanX(mean(x_poss))
        features_object.setMeanY(mean(y_poss))
        trace_length = 0
        for idx in range(1, len(x_poss)):
            dx = x_poss[idx] - x_poss[idx - 1]
            dy = y_poss[idx] - y_poss[idx - 1]
            trace_length += sqrt(dx ** 2 + dy ** 2)
        features_object.setTraceLength(trace_length)
        dx = abs(x_poss[-1] - x_poss[0])
        dy = abs(y_poss[-1] - y_poss[0])
        start_stop_length = sqrt(dx ** 2 + dy ** 2)
        features_object.setStartStopLength(start_stop_length)
        temp_dict = {
            'hor': {
                'trace_projection': dx,
                'points': {},
                'norm': {
                    True: default_width,
                    False: gesture['device_width']
                }
            },
            'ver': {
                'trace_projection': dy,
                'points': {},
                'norm': {
                    True: default_height,
                    False: gesture['device_height']
                }
            }
        }
        direction = 'hor' if dx >= dy else 'ver'
        trace_projection = temp_dict[direction]['trace_projection']
        features_object.setTraceProjection(trace_projection)
        features_object.setScreenPercentage(trace_projection / temp_dict[direction]['norm'][normalize])
        start_velocity = sqrt(ges_data[0]['vx'] ** 2 + ges_data[0]['vy'] ** 2)
        features_object.setStartVelocity(start_velocity)
        stop_velocity = sqrt(ges_data[-1]['vx'] ** 2 + ges_data[-1]['vy'] ** 2)
        features_object.setStopVelocity(stop_velocity)
        acceleration_hor = (ges_data[-1]['vx'] - ges_data[0]['vx']) / (gesture['duration'] * 0.001)
        features_object.setAccelerationHor(acceleration_hor)
        acceleration_ver = (ges_data[-1]['vy'] - ges_data[0]['vy']) / (gesture['duration'] * 0.001)
        features_object.setAccelerationVer(acceleration_ver)
        trace_stats = linear_regression(x_poss, y_poss)
        features_object.setSlope(trace_stats['slope'])
        features_object.setMeanSquareError(trace_stats['mean_squared_error'])
        features_object.setMeanAbsError(trace_stats['mean_abs_error'])
        features_object.setMedianAbsError(trace_stats['median_abs_error'])
        features_object.setCoefDetermination(trace_stats['coef_determination'])

    else:

        features_object.setMeanX()
        features_object.setMeanY()
        features_object.setTraceLength()
        features_object.setStartStopLength()
        features_object.setScreenPercentage()
        features_object.setTraceProjection()
        features_object.setStartVelocity()
        features_object.setStopVelocity()
        features_object.setAccelerationHor()
        features_object.setAccelerationVer()
        features_object.setSlope()
        features_object.setMeanSquareError()
        features_object.setMeanAbsError()
        features_object.setMedianAbsError()
        features_object.setCoefDetermination()

    return features_object


def extract_features_ges(case: str, screen_path: str, data: pd.DataFrame):

    print(' - Extracting gestures features.')
    path_df = os.path.join(screen_path, 'ftr_ges.csv')

    if not os.path.exists(path_df):

        normalize = dict_cases[case]['FeatureExtraction']['ges']['normalize']
        default_width = dict_cases[case]['FeatureExtraction']['ges']['default_width']
        default_height = dict_cases[case]['FeatureExtraction']['ges']['default_height']

        features_object = FeaturesGes()
        for user in tqdm(list(set(data['user']))):
            user_data = data.loc[data['user'] == user]
            user_data = user_data.sort_values(by=['time_start'], ignore_index=True)
            for index, ges in user_data.iterrows():
                features_object = calculate_features_ges(ges, features_object, normalize, default_width, default_height)

        df_features = features_object.create_dataframe()
        df_features.to_csv(path_df, index=False)
        print('     gestures features dataframe saved at: ', path_df)

    else:

        df_features = pd.read_csv(path_df)
        print('     gestures features dataframe loaded from: ', path_df)

    print('')

    return df_features
