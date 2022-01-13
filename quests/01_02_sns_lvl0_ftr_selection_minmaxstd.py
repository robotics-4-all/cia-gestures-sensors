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

#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    c = 'case01'
    s = dict_cases[c]['screens']
    sensors = ['acc', 'gyr']

    for screen in s:
        for sns in sensors:
            data_path = os.path.join('cases', c, screen, 'df_' + sns + '.csv')
            df_data = pd.read_csv(data_path)
            users = list(set(df_data['user']))
            votes = {}
            for user in users:
                user_data = df_data.loc[df_data['user'] == user][['x', 'y', 'magnitude']]
                user_data = user_data.reset_index(drop=True)
                temp_std = user_data.std(axis=0, skipna=True)
                ftr_std = list(user_data)[temp_std.argmin()]  # argmin, argmax
                if ftr_std not in votes:
                    votes[ftr_std] = {'votes': 0, 'mean': 0}
                votes[ftr_std]['votes'] += 1
                votes[ftr_std]['mean'] += temp_std[ftr_std]
            for ftr in votes:
                votes[ftr]['mean'] /= len(users)
            print(c, screen, sns, votes)
