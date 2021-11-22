"""
This script was created at 14-Nov-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os
import pandas as pd

'''
results:

case1 Mathisis acc {'magnitude': 43, 'x': 1}
case1 Mathisis gyr {'x': 33, 'y': 11}
case1 Focus acc {'magnitude': 47, 'x': 4}
case1 Focus gyr {'y': 17, 'x': 34}
case1 Reacton acc {'magnitude': 10, 'x': 1}
case1 Reacton gyr {'x': 11}

case2 Reacton acc {'magnitude': 65, 'x': 4, 'y': 1}
case2 Reacton gyr {'x': 60, 'y': 10}
case2 Memoria acc {'magnitude': 106, 'x': 10}
case2 Memoria gyr {'x': 84, 'y': 32}
case2 Speedy acc {'magnitude': 92, 'x': 14, 'y': 1}
case2 Speedy gyr {'magnitude': 2, 'x': 78, 'y': 27}

conclusion:
acc -> magnitude
gyr -> x
'''


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    case = 'case1'
    screens = ['Mathisis', 'Focus', 'Reacton']  # case1
    # screens = ['Reacton', 'Memoria', 'Speedy']  # case2
    snss = ['acc', 'gyr']

    for screen in screens:
        for sns in snss:

            data_path = os.path.join('cases', case, screen, 'df_' + sns + '.csv')
            df_data = pd.read_csv(data_path)

            users = list(set(df_data['user']))

            votes = {}
            for user in users:
                user_data = df_data.loc[df_data['user'] == user][['x', 'y', 'magnitude']]
                user_data = user_data.reset_index()
                temp_std = user_data.std(axis=0, skipna=True)
                ftr_min_std = list(user_data)[temp_std.argmin()]
                if ftr_min_std not in votes:
                    votes[ftr_min_std] = {'votes': 0, 'mean': 0}
                votes[ftr_min_std]['votes'] += 1
                votes[ftr_min_std]['mean'] += temp_std[ftr_min_std]
            for ftr in votes:
                votes[ftr]['mean'] /= len(users)

            print(case, screen, sns, votes)
