"""
This script was created at 07-Feb-22
author: eachrist

"""
import os
import pandas as pd

guide_dict = {
    'Mathisis': ['33a3a5u', '508rk86', 'ldg6zjk', 'ta0ko40', 'aqq25vq'],
    'Focus': ['508rk86', '68n9ll', '9gykp6g', 'ftk8v41', 'qa94pwy', 'ldg6zjk', '677l8bq'],
    'Reacton': ['1l967s6', '60u0i9n', '7stgp0r', '8uohdv4', 'sxvkh3b', 'w764hxe'],
    'Speedy': ['508rk86', '9gx7uks', 'gy48qmy', 'xfx1ung', '7stgp0r'],
    'Memoria': ['9gx7uks', 'xrm6gjj', 'cyr6jmc', '7f0qwx8', '06mdn3c', 'xfx1ung']
}

if __name__ == '__main__':

    cases = ['case29']
    screens = ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria']

    guide_case = 'case20'
    for screen in screens:

        # get list of users to remove
        results_g_path = os.path.join('cases', guide_case, screen, 'results.csv')
        results_g = pd.read_csv(results_g_path)
        users_to_drop = list(set(results_g['OriginalUser'].to_list())) + guide_dict[screen]

        for case in cases:
            for mod in ['acc', 'gyr', 'ges']:
                ftr_path = os.path.join('cases', case, screen, 'ftr_' + mod + '.csv')
                ftr_df = pd.read_csv(ftr_path)

                debug = True

                # remove users
                for index, row in ftr_df.iterrows():
                    if row['User'] in users_to_drop:
                        ftr_df = ftr_df.drop(index)
                ftr_df = ftr_df.reset_index(drop=True)

                # save
                ftr_df.to_csv(ftr_path, index=False)
