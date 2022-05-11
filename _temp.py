"""
This script was created at 07-Feb-22
author: eachrist

"""
import os
import pandas as pd

if __name__ == '__main__':

    cases = ['case23.2']
    screens = ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria']
    what_to_remove = 2
    # 1 for 'remove users used in training'
    # 2 for 'remove extra users with bad results in guide_case'

    guide_case = 'case20'
    guide_dict = {
        'Mathisis': ['33a3a5u', '508rk86', 'ldg6zjk', 'ta0ko40', 'aqq25vq'],
        'Focus': ['508rk86', '68n9ll', '9gykp6g', 'ftk8v41', 'qa94pwy', 'ldg6zjk', '677l8bq'],
        'Reacton': ['1l967s6', '60u0i9n', '7stgp0r', '8uohdv4', 'sxvkh3b', 'w764hxe'],
        'Speedy': ['508rk86', '9gx7uks', 'gy48qmy', 'xfx1ung', '7stgp0r'],
        'Memoria': ['9gx7uks', 'xrm6gjj', 'cyr6jmc', '7f0qwx8', '06mdn3c', 'xfx1ung']
    }

    # for every screen
    for screen in screens:

        if what_to_remove == 1:
            results_g_path = os.path.join('cases', guide_case, screen, 'results.csv')
            results_g = pd.read_csv(results_g_path)
            users_to_drop = list(set(results_g['OriginalUser'].to_list()))

        if what_to_remove == 2:
            users_to_drop = guide_dict[screen]

        # for every case
        for case in cases:
            if what_to_remove == 1:
                results_path = os.path.join('cases', case, screen, 'results.csv')

            if what_to_remove == 2:
                results_path = os.path.join('cases', case, screen, 'results_1.csv')
            results = pd.read_csv(results_path)

            # modify results
            for index, row in results.iterrows():
                if row['OriginalUser'] in users_to_drop:
                    results = results.drop(index)
            results = results.reset_index(drop=True)

            # save results
            results_path = os.path.join('cases', case, screen, 'results_1.csv')
            results.to_csv(results_path, index=False)

        debug = True
