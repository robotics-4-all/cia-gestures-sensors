"""
This script was created at 17-Dec-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os
import pandas as pd
from s0_cases_dictionaries import dict_cases

#  =================== #
#    Case Selection    #
# ==================== #
from cases.case18.subclasses_classifiers import dict_nu, dict_gamma
case = 'case18'

#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    for screen in dict_cases[case]['screens']:

        results_path = os.path.join('cases', case, screen, 'results.csv')
        results = pd.read_csv(results_path)

        false_nus = dict_cases[case]['GetResults']['Classifiers']['nus']
        false_gammas = dict_cases[case]['GetResults']['Classifiers']['gammas']

        for mod in ['acc', 'gyr', 'swp', 'tap']:
            true_nus = dict_nu[mod]
            true_gammas = dict_gamma[mod]

            mod_df = results.loc[results['Module'] == mod]
            mod_df['Nu'] = mod_df['Nu'].replace(false_nus, true_nus)
            mod_df['Gamma'] = mod_df['Gamma'].replace(false_gammas, true_gammas)

            results.loc[mod_df.index, :] = mod_df[:]

        results_path = os.path.join('cases', case, screen, 'results.csv')
        results.to_csv(results_path, index=False)
