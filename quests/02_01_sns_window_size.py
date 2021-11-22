"""
This script was created at 14-Nov-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os
import pandas as pd
from tqdm import tqdm
from statistics import stdev

from s0_Helpers_Functions import check_paths, frange
from s3_ExtractFeatures_Functions import extract_features_df_sns

from _cases_dictionaries import dict_cases

'''
desc:
'extraction_type': 'User'

results:

aggelikihs = {
window = 500
overlap = 0.9 
} kai blepoume

'''


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    cases = {
        'case1': ['Mathisis', 'Focus', 'Reacton'],
        'case2': ['Reacton', 'Memoria', 'Speedy']
    }
    snss = ['acc', 'gyr']

    results = pd.DataFrame()

    for case in cases:
        case_path = check_paths(os.path.dirname(os.path.dirname(__file__)), os.path.join('cases', case))

        for screen in cases[case]:
            screen_path = check_paths(case_path, screen)

            for sns in snss:
                feature = dict_cases[case]['ExtractFeatures']['sns']['feature'][sns[0:3]]
                data_path = os.path.join('cases', case, screen, 'df_' + sns + '.csv')
                df_data = pd.read_csv(data_path)[['user', feature]]

                for window in [50, 200, 500, 1000, 1500]:
                    for overlap in [0, 0.3, 0.9]:
                        mean_std = 0

                        for user in tqdm(set(df_data['user'])):

                            overlap_rl_size = int(overlap * window)

                            means = []

                            data_length = df_data.shape[0]
                            if data_length >= window:
                                flag = True
                                start = 0

                                while data_length > 0:
                                    stop = start + window
                                    window_data = df_data[start:stop]
                                    means.append(window_data.mean().values[0])

                                    if flag:
                                        data_length += start - stop
                                        flag = False
                                    else:
                                        data_length += start - stop + overlap_rl_size

                                    if data_length + overlap_rl_size < window:
                                        if data_length < overlap_rl_size:
                                            break
                                        overlap_rl_size = window - data_length

                                    start = stop - overlap_rl_size

                            mean_std += stdev(means)

                        mean_std /= len(list(set(df_data['user'])))

                        df_row = {
                            'case': case,
                            'screen': screen,
                            'sensor': sns,
                            'window': window,
                            'overlap': overlap,
                            'mean_std': mean_std
                        }
                        results = results.append(df_row, ignore_index=True)

            print('...next screen\n')

    results.to_csv(os.path.join(os.path.dirname(__file__), '02_01_sns_window_size_results.csv'), index=False)
