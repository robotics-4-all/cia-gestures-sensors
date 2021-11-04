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
from scipy.fftpack import fft
from scipy.stats import entropy, kurtosis, skew

from _cases_dictionaries import dict_cases
from s0_Helpers_Functions import *
from s3_ExtractFeatures_Classes import *


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

        extraction_type = dict_cases[case_name]['ExtractFeatures']['sns']['extraction_type']
        feature = dict_cases[case_name]['ExtractFeatures']['sns']['feature']

        features_object = FeaturesSns()

        for user in tqdm(set(df['user'])):

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


def extract_features_swp(case_name: str, swipe, features_object):

    normalize = dict_cases[case_name]['ExtractFeatures']['swp']['normalize']

    scalar_width = 400
    scalar_height = 700

    features_object.setUser(swipe['user'])
    features_object.setTimeStart(swipe['time_start'])
    features_object.setTimeStop(swipe['time_stop'])
    features_object.setScreen(swipe['screen'])
    features_object.setDuration(swipe['duration'])

    if type(swipe['data']) == str:
        swipe_data = ast.literal_eval(swipe['data'])
    else:
        swipe_data = swipe['data']

    x_positions = []
    y_positions = []
    x_positions.append(swipe_data[0]['x0'])
    y_positions.append(swipe_data[0]['y0'])
    for data in swipe_data:
        x_positions.append(data['moveX'])
        y_positions.append(data['moveY'])

    length_horizontal = x_positions[-1] - x_positions[0]
    length_vertical = y_positions[-1] - y_positions[0]
    if normalize:
        length_horizontal = scalar_width * length_horizontal / swipe['device_width']
        length_vertical = scalar_height * length_vertical / swipe['device_height']
    features_object.setTraceLengthHorizontal(np.abs(length_horizontal))
    features_object.setTraceLengthVertical(np.abs(length_vertical))

    if np.abs(length_horizontal) > np.abs(length_vertical):
        if length_horizontal > 0:
            direction = 'right'
        else:
            direction = 'left'
    else:
        if length_vertical > 0:
            direction = 'up'
        else:
            direction = 'down'
    features_object.setDirection(direction)

    trace_stats = linear_regression(x_positions, y_positions)
    features_object.setSlope(trace_stats['slope'])
    features_object.setMeanSquareError(trace_stats['mean_squared_error'])
    features_object.setMeanAbsError(trace_stats['mean_abs_error'])
    features_object.setMedianAbsError(trace_stats['median_abs_error'])
    features_object.setCoefDetermination(trace_stats['coef_determination'])

    acceleration_horizontal = (swipe_data[-1]['vx'] - swipe_data[0]['vx']) / (swipe['duration'] * 0.001)
    acceleration_vertical = (swipe_data[-1]['vy'] - swipe_data[0]['vy']) / (swipe['duration'] * 0.001)
    features_object.setAccelerationHorizontal(acceleration_horizontal)
    features_object.setAccelerationVertical(acceleration_vertical)

    mean_x = 0
    mean_y = 0
    for x in x_positions:
        mean_x += x
    for y in y_positions:
        mean_y += y
    mean_x /= len(x_positions)
    mean_y /= len(y_positions)
    if normalize:
        mean_x = scalar_width * mean_x / swipe['device_width']
        mean_y = scalar_height * mean_y / swipe['device_height']
    features_object.setMeanX(mean_x)
    features_object.setMeanY(mean_y)

    return features_object


def extract_features_df_swp(case_name: str, screen_path: str, df: pd.DataFrame) -> pd.DataFrame:

    print(' - Extract features swipes.')
    path_features_df_swp = os.path.join(screen_path, 'features_swipes.csv')

    if not os.path.exists(path_features_df_swp):

        features_object = FeaturesSwp()

        for index, swipe in tqdm(df.iterrows()):
            features_object = extract_features_swp(case_name, swipe, features_object)

        features_df_swp = features_object.create_dataframe()
        features_df_swp.to_csv(path_features_df_swp, index=False)
        print('     Swipes features saved at: ', path_features_df_swp)

    else:

        features_df_swp = pd.read_csv(path_features_df_swp)
        print('     Swipes features loaded from: ', path_features_df_swp)

    print('     swipes_feature size: ', features_df_swp.shape[0])
    print('')

    return features_df_swp
