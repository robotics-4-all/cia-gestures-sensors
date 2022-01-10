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
from s4_GetResults_SimpleClassifier import get_predictions
from s4_GetResults_Evaluator import Evaluator


#  ============== #
#    Functions    #
# =============== #
def split_df_sns(original_user: str, df: pd.DataFrame, split_rate: float):

    data = df.loc[df['User'] == original_user].reset_index(drop=True)
    groups = list(set(data['Group']))
    groups.sort()

    nod_trn = 0
    idx_ts = 0
    while nod_trn < round(data.shape[0] * (1 - split_rate)):
        nod_trn += data.loc[data['Group'] == groups[idx_ts]].shape[0]
        idx_ts += 1
        if idx_ts >= len(groups):
            idx_ts -= 1
            break
    ts_trn_stop = groups[idx_ts - 1]
    ts_tst_start = groups[idx_ts]

    df_trn = data.loc[data['Group'] <= ts_trn_stop].reset_index(drop=True)
    df_tst = data.loc[data['Group'] >= ts_tst_start].reset_index(drop=True)
    df_att = df.loc[df['User'] != original_user].reset_index(drop=True)

    return df_trn, df_tst, df_att


def split_df_ges(original_user: str, df: pd.DataFrame, split_rate: float):

    data = df.loc[df['User'] == original_user].reset_index(drop=True)
    nog_trn = round(data.shape[0] * (1 - split_rate)) + 1

    df_trn = data[:nog_trn].reset_index(drop=True)
    df_tst = data[nog_trn:].reset_index(drop=True)
    df_att = df.loc[df['User'] != original_user].reset_index(drop=True)

    return df_trn, df_tst, df_att


def get_results(case: str, screen: str, screen_path: str,
                df_acc: pd.DataFrame, df_gyr: pd.DataFrame, df_ges: pd.DataFrame) -> pd.DataFrame:

    print(' - Getting results.')
    path_df = os.path.join(screen_path, 'results.csv')

    # Define parameters
    split_rate = dict_cases[case]['GetResults']['split_rate']

    # Define evaluator
    eval_obj = Evaluator(screen)

    # Select original user
    for original_user in tqdm(set(df_acc['User'])):

        # Split data to trn, tst, att
        acc_trn, acc_tst, acc_att = split_df_sns(original_user, df_acc, split_rate)
        gyr_trn, gyr_tst, gyr_att = split_df_sns(original_user, df_gyr, split_rate)
        ges_trn, ges_tst, ges_att = split_df_ges(original_user, df_ges, split_rate)

        # Separate swipes & taps
        swp_trn = ges_trn.loc[ges_trn['Type'] == 'swipe'].reset_index(drop=True)
        tap_trn = ges_trn.loc[ges_trn['Type'] == 'tap'].reset_index(drop=True)
        swp_tst = ges_tst.loc[ges_tst['Type'] == 'swipe'].reset_index(drop=True)
        tap_tst = ges_tst.loc[ges_tst['Type'] == 'tap'].reset_index(drop=True)
        swp_att = ges_att.loc[ges_att['Type'] == 'swipe'].reset_index(drop=True)
        tap_att = ges_att.loc[ges_att['Type'] == 'tap'].reset_index(drop=True)

        # Concentrate data
        sets_dict = {
            'trn': [acc_trn, gyr_trn, swp_trn, tap_trn],
            'tst': [acc_tst, gyr_tst, swp_trn, tap_trn],
            'att': [acc_att, gyr_att, swp_trn, tap_trn]
        }

        # Define Classifiers
        classifiers = []
        for data_type in ['acc', 'gyr', 'swp', 'tap']:
            lvl0_ftr = None
            if data_type in ['acc', 'gyr']:
                lvl0_ftr = dict_cases[case]['FeatureExtraction']['sns']['lvl0_ftr'][data_type]
            classifiers.append(dict_cases[case]['GetResults']['Classifiers'][data_type](lvl0_ftr))

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
