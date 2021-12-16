"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os
import pandas as pd
from tqdm import tqdm

from s0_cases_dictionaries import dict_cases
from s3_ExtractFeatures_Functions import extract_features_sns, extract_features_ges
from s3_GetResults_SimpleClassifier import get_predictions
from s3_GetResults_Evaluator import Evaluator


#  ============== #
#    Functions    #
# =============== #
def split_df_sns(original_user: str, df: pd.DataFrame, split_rate: float):

    data = df.loc[df['user'] == original_user].reset_index(drop=True)
    timestamps = list(set(data['timestamp']))
    timestamps.sort()

    nod_trn = 0
    idx_ts = 0
    while nod_trn < round(data.shape[0] * (1 - split_rate)):
        nod_trn += data.loc[data['timestamp'] == timestamps[idx_ts]].shape[0]
        idx_ts += 1
    ts_trn_stop = timestamps[idx_ts - 1]
    ts_tst_start = timestamps[idx_ts]

    df_trn = data.loc[data['timestamp'] <= ts_trn_stop].reset_index(drop=True)
    df_tst = data.loc[data['timestamp'] >= ts_tst_start].reset_index(drop=True)
    df_att = df.loc[df['user'] != original_user].reset_index(drop=True)

    return df_trn, df_tst, df_att


def split_df_ges(original_user: str, df: pd.DataFrame, split_rate: float):

    data = df.loc[df['user'] == original_user].reset_index(drop=True)
    nog_trn = round(data.shape[0] * (1 - split_rate)) + 1

    df_trn = data[:nog_trn].reset_index(drop=True)
    df_tst = data[nog_trn:].reset_index(drop=True)
    df_att = df.loc[df['user'] != original_user].reset_index(drop=True)

    return df_trn, df_tst, df_att


def get_results(case_name: str, screen_name: str, screen_path: str,
                df_acc: pd.DataFrame, df_gyr: pd.DataFrame, df_ges: pd.DataFrame) -> pd.DataFrame:

    print(' - Getting results.')
    path_df = os.path.join(screen_path, 'results.csv')

    # Define parameters
    split_rate = dict_cases[case_name]['GetResults']['split_rate']
    sns_lvl0_ftr = dict_cases[case_name]['GetResults']['FeatureExtraction']['sns']['lvl0_ftr']
    sample_rate = dict_cases[case_name]['GetResults']['FeatureExtraction']['sns']['sample_rate']
    window = dict_cases[case_name]['GetResults']['FeatureExtraction']['sns']['window']
    overlap = dict_cases[case_name]['GetResults']['FeatureExtraction']['sns']['overlap']
    normalize = dict_cases[case_name]['GetResults']['FeatureExtraction']['ges']['normalize']
    default_width = dict_cases[case_name]['GetResults']['FeatureExtraction']['ges']['default_width']
    default_height = dict_cases[case_name]['GetResults']['FeatureExtraction']['ges']['default_height']
    time_window = dict_cases[case_name]['GetResults']['Evaluator']['time_window']

    # Define evaluator
    eval_obj = Evaluator(screen_name, time_window)

    # Select original user
    for original_user in tqdm(set(df_acc['user'])):

        # Split data to trn, tst
        acc_trn, acc_tst, acc_att = split_df_sns(original_user, df_acc, split_rate)
        gyr_trn, gyr_tst, gyr_att = split_df_sns(original_user, df_gyr, split_rate)
        ges_trn, ges_tst, ges_att = split_df_ges(original_user, df_ges, split_rate)

        # Extract features for training data
        ftr_acc_trn = extract_features_sns(acc_trn, 'acc', sns_lvl0_ftr, window, overlap, sample_rate)
        ftr_gyr_trn = extract_features_sns(gyr_trn, 'gyr', sns_lvl0_ftr, window, overlap, sample_rate)
        ftr_ges_trn = extract_features_ges(ges_trn, normalize, default_width, default_height)
        ftr_swp_trn = ftr_ges_trn.loc[ftr_ges_trn['Type'] == 'swipe'].reset_index(drop=True)
        ftr_tap_trn = ftr_ges_trn.loc[ftr_ges_trn['Type'] == 'tap'].reset_index(drop=True)

        # Extract features for testing data
        ftr_acc_tst = extract_features_sns(acc_tst, 'acc', sns_lvl0_ftr, window, 0, sample_rate)
        ftr_gyr_tst = extract_features_sns(gyr_tst, 'gyr', sns_lvl0_ftr, window, 0, sample_rate)
        ftr_ges_tst = extract_features_ges(ges_tst, normalize, default_width, default_height)
        ftr_swp_tst = ftr_ges_tst.loc[ftr_ges_tst['Type'] == 'swipe'].reset_index(drop=True)
        ftr_tap_tst = ftr_ges_tst.loc[ftr_ges_tst['Type'] == 'tap'].reset_index(drop=True)

        # Extract features for attackers data
        ftr_acc_att = extract_features_sns(acc_att, 'acc', sns_lvl0_ftr, window, 0, sample_rate)
        ftr_gyr_att = extract_features_sns(gyr_att, 'gyr', sns_lvl0_ftr, window, 0, sample_rate)
        ftr_ges_att = extract_features_ges(ges_att, normalize, default_width, default_height)
        ftr_swp_att = ftr_ges_att.loc[ftr_ges_att['Type'] == 'swipe'].reset_index(drop=True)
        ftr_tap_att = ftr_ges_att.loc[ftr_ges_att['Type'] == 'tap'].reset_index(drop=True)

        # Concentrate data
        sets_dict = {
            'trn': [ftr_acc_trn, ftr_gyr_trn, ftr_swp_trn, ftr_tap_trn],
            'tst': [ftr_acc_tst, ftr_gyr_tst, ftr_swp_tst, ftr_tap_tst],
            'att': [ftr_acc_att, ftr_gyr_att, ftr_swp_att, ftr_tap_att]
        }

        # Define Classifiers
        classifiers = []
        for data_type in ['acc', 'gyr', 'swp', 'tap']:
            classifiers.append(dict_cases[case_name]['GetResults']['Classifiers'][data_type]())

        # Train Classifiers
        for idx, clf in enumerate(classifiers):
            clf.train_classifiers(sets_dict['trn'][idx])

        # Get prediction for training, testing and attackers data
        for sett in sets_dict:
            for idx, clf in enumerate(classifiers):
                sets_dict[sett][idx]['Decision'] = clf.get_decisions(sets_dict[sett][idx])
                sets_dict[sett][idx]['Prediction'] = get_predictions(sets_dict[sett][idx]['Decision'])

        # Evaluate predictions of every module separately
        eval_obj.calculate_metrics(original_user, sets_dict)

    # Create dataframe with the results of separated modules
    results = eval_obj.create_dataframe()

    # Save results
    results.to_csv(path_df, index=False)
    print('     Results saved at: ', path_df)
    print('')

    return results
