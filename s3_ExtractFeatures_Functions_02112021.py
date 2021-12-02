"""
This script was created at 14-Sep-21
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

from _cases_dictionaries import dict_cases
from s0_Helpers_Functions import linear_regression
from s3_ExtractFeatures_Classes import FeaturesSns, FeaturesSwp, FeaturesTap


# =============== #
#    Functions    #
# =============== #
def extract_features_sns(case_name: str, data: np.array, features_object, user, timestamp, screen):

    window = dict_cases[case_name]['ExtractFeatures']['sns']['window']
    overlap = dict_cases[case_name]['ExtractFeatures']['sns']['overlap']

    overlap = int(overlap * window)
    data_length = data.shape[0]

    if data_length >= window:
        flag = True
        start = 0

        while data_length > 0:
            features_object.setUser(user)
            features_object.setTimestamp(timestamp)
            features_object.setScreen(screen)

            stop = start + window

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

            if data_length + overlap < window:
                if data_length < overlap:
                    break
                overlap = window - data_length

            start = stop - overlap

    return features_object


def extract_features_df_sns(case_name: str, screen_path: str, df: pd.DataFrame, sensor: str):

    print(' - Extract features ' + sensor + '.')
    path_features_df_sns = os.path.join(screen_path, 'features_' + sensor[0:3] + '.csv')

    if not os.path.exists(path_features_df_sns):

        features_object = FeaturesSns()

        feature = dict_cases[case_name]['ExtractFeatures']['sns']['feature'][sensor[0:3]]
        for user in tqdm(set(df['user'])):
            data = df.loc[df['user'] == user]
            data = data.sort_values(by=[''])



            if extraction_type == 'User':
                data = np.array(df.loc[df['user'] == user][feature])
                features_object = extract_features_sns(case_name, data, features_object, user, None, None)

            elif extraction_type == 'Timestamp' or extraction_type == 'TimestampScreen':
                timestamps = set(df.loc[df['user'] == user]['timestamp'])
                for timestamp in timestamps:
                    if extraction_type == 'Timestamp':
                        data = np.array(df.loc[(df['user'] == user) &
                                               (df['timestamp'] == timestamp)][feature])
                        features_object = extract_features_sns(case_name, data, features_object, user, timestamp, None)

                    elif extraction_type == 'TimestampScreen':
                        screens = set(df.loc[(df['user'] == user) &
                                             (df['timestamp'] == timestamp)]['screen'])
                        for screen in screens:
                            data = np.array(
                                df.loc[(df['user'] == user) &
                                       (df['timestamp'] == timestamp) &
                                       (df['screen'] == screen)][feature])
                            features_object = extract_features_sns(case_name, data, features_object, user, timestamp, screen)

            elif extraction_type == 'Screen':

                screens = set(df.loc[df['user'] == user]['screen'])
                for screen in screens:
                    data = np.array(df.loc[(df['user'] == user) & (df['screen'] == screen)][feature])
                    features_object = extract_features_sns(case_name, data, features_object, user, None, screen)

        features_df_sns = features_object.create_dataframe()
        features_df_sns.to_csv(path_features_df_sns, index=False)
        print('     ' + sensor + ' features saved at: ', path_features_df_sns)

    else:

        features_df_sns = pd.read_csv(path_features_df_sns)
        print('     ' + sensor + ' features loaded from: ', path_features_df_sns)

    print('     ' + sensor + '_feature size: ', features_df_sns.shape[0])
    print('')

    return features_df_sns


def extract_features_ges(case_name: str, ges, features_object):

    features_object.setUser(ges['user'])
    features_object.setTimeStart(ges['time_start'])
    features_object.setTimeStop(ges['time_stop'])
    features_object.setScreen(ges['screen'])
    features_object.setDuration(ges['duration'])

    if dict_cases[case_name]['gesture_type'] == 'swipe':

        normalize = dict_cases[case_name]['ExtractFeatures']['ges']['normalize']
        scalar_width = 400
        scalar_height = 700

        if type(ges['data']) == str:
            swp_data = ast.literal_eval(ges['data'])
        else:
            swp_data = ges['data']

        x_poss, y_poss = [swp_data[0]['x0']], [swp_data[0]['y0']]
        for data in swp_data:
            x_poss.append(data['moveX'])
            y_poss.append(data['moveY'])
        if normalize:
            x_poss = [x * scalar_width / ges['device_width'] for x in x_poss]
            y_poss = [y * scalar_height / ges['device_height'] for y in y_poss]

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
                    True: scalar_width,
                    False: ges['device_width']
                }
            },
            'ver': {
                'trace_projection': dy,
                'points': {},
                'norm': {
                    True: scalar_height,
                    False: ges['device_height']
                }
            }
        }

        direction = 'hor' if dx >= dy else 'ver'

        trace_projection = temp_dict[direction]['trace_projection']
        features_object.setTraceProjection(trace_projection)

        features_object.setScreenPercentage(trace_projection / temp_dict[direction]['norm'][normalize])

        features_object.setRatio(None)  # (trace_projection / start_stop_length)
        features_object.setDeviation(None)  # define
        features_object.setLeaning(None)  # define

        start_velocity = sqrt(swp_data[0]['vx'] ** 2 + swp_data[0]['vy'] ** 2)
        features_object.setStartVelocity(start_velocity)

        stop_velocity = sqrt(swp_data[-1]['vx'] ** 2 + swp_data[-1]['vy'] ** 2)
        features_object.setStopVelocity(stop_velocity)

        acceleration_hor = (swp_data[-1]['vx'] - swp_data[0]['vx']) / (ges['duration'] * 0.001)
        features_object.setAccelerationHor(acceleration_hor)

        acceleration_ver = (swp_data[-1]['vy'] - swp_data[0]['vy']) / (ges['duration'] * 0.001)
        features_object.setAccelerationVer(acceleration_ver)

        trace_stats = linear_regression(x_poss, y_poss)
        features_object.setSlope(trace_stats['slope'])
        features_object.setMeanSquareError(trace_stats['mean_squared_error'])
        features_object.setMeanAbsError(trace_stats['mean_abs_error'])
        features_object.setMedianAbsError(trace_stats['median_abs_error'])
        features_object.setCoefDetermination(trace_stats['coef_determination'])

    return features_object


def extract_features_df_ges(case_name: str, screen_path: str, df: pd.DataFrame) -> pd.DataFrame:

    print(' - Extract features gestures.')
    path_features_df_ges = os.path.join(screen_path, 'features_ges.csv')

    if not os.path.exists(path_features_df_ges):

        if dict_cases[case_name]['gesture_type'] == 'swipe':
            features_object = FeaturesSwp()
        elif dict_cases[case_name]['gesture_type'] == 'tap':
            features_object = FeaturesTap()

        for index, ges in tqdm(df.iterrows()):
            features_object = extract_features_ges(case_name, ges, features_object)

        features_df_ges = features_object.create_dataframe()
        features_df_ges.to_csv(path_features_df_ges, index=False)
        print('     Gestures features saved at: ', path_features_df_ges)

    else:

        features_df_ges = pd.read_csv(path_features_df_ges)
        print('     Gestures features loaded from: ', path_features_df_ges)

    print('     gestures_feature size: ', features_df_ges.shape[0])
    print('')

    return features_df_ges
