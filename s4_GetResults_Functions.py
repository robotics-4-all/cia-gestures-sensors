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
def get_results(case_name: str, screen_path: str, ftr_acc: pd.DataFrame, ftr_gyr: pd.DataFrame, ftr_swp: pd.DataFrame) -> pd.DataFrame:

    path_results = os.path.join(screen_path, 'results.csv')

    if not os.path.exists(path_results):
        results = pd.DataFrame()

        dict_obj = {
            'acc': dict_cases[case_name]['GetResults']['acc'],
            'gyr': dict_cases[case_name]['GetResults']['gyr'],
            'swp': dict_cases[case_name]['GetResults']['swp'],
            'ags': dict_cases[case_name]['GetResults']['ags']
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
            for module in dict_obj:

                if module != 'ags':
                    obj = dict_obj[module](original_user, dict_ftr[module])
                    obj.train_classifier()
                    dict_decisions[module] = obj.get_decisions()
                else:
                    obj = dict_obj[module](original_user, dict_decisions)
                    final_predictions = obj.get_final_predictions()

                metrics = obj.calculate_metrics()
                results = results.append(metrics, ignore_index=True)

        # Save all results
        results.to_csv(path_results, index=False)
        print('     Results saved at:', path_results)

        # Save analytics
        for module in dict_obj:
            path_analytics = os.path.join(screen_path, 'results_analytics_' + module + '.csv')
            results.loc[results['Module'] == module].describe().to_csv(path_analytics, index=True)
            print('     ' + module + ' analytics saved saved at:', path_analytics)

    else:

        results = pd.read_csv(path_results)
        print('     Results loaded from:', path_results)

    print('')

    return results
