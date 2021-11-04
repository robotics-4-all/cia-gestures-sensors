"""
This script was created at 20-Sep-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os
import pandas as pd
from tqdm import tqdm

from _cases_dictionaries import dict_cases


#  ============== #
#    Functions    #
# =============== #
def get_results(case_name: str, screen_path: str, ftr_acc: pd.DataFrame, ftr_gyr: pd.DataFrame, ftr_swp: pd.DataFrame):

    path_results = os.path.join(screen_path, 'results.csv')
    results = pd.DataFrame()

    dict_obj = {
        'acc': dict_cases[case_name]['GetResults']['acc'],
        'gyr': dict_cases[case_name]['GetResults']['gyr'],
        'swp': dict_cases[case_name]['GetResults']['swp']
    }

    dict_ftr = {
        'acc': ftr_acc,
        'gyr': ftr_gyr,
        'swp': ftr_swp
    }

    # Select original user
    for original_user in tqdm(set(ftr_acc['User'])):

        dict_decisions = {'acc': None, 'gyr': None, 'swp': None}

        # Get level 1 decisions
        for data_type in dict_obj:
            obj = dict_obj[data_type](original_user, dict_ftr[data_type])
            obj.train_classifier()
            dict_decisions[data_type] = obj.get_decisions()
            metrics = obj.calculate_metrics()
            results = results.append(metrics, ignore_index=True)

        # Get final predictions

    # Save all results
    results.to_csv(path_results, index=False)
    print('     Results saved saved at:', path_results)

    # Save analytics
    for data_type in dict_obj:
        path_analytics = os.path.join(screen_path, 'results_analytics_' + data_type + '.csv')
        results.loc[results['Data_Type'] == data_type].describe().to_csv(path_analytics, index=True)
        print('     ' + data_type + ' analytics saved saved at:', path_analytics)
    print('')

    return
