"""
This script was created at 09-Dec-21
author: eachrist

"""
# Remove random shuffle from line 38.

# ============= #
#    Imports    #
# ============= #
import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from bson.objectid import ObjectId

from s0_cases_dictionaries import json_files_path, gestures_database_name, dict_cases
from s__Helpers_Functions import MongoDBHandler, DBDataHandler


# =============== #
#    Functions    #
# =============== #
def create_df_sns(case_name: str, screen_path: str, dict_sns: dict, sensor: str):

    print(' - Creating ' + sensor + ' dataframe.')
    path_df = os.path.join(screen_path, 'df_' + sensor[0:3] + '.csv')

    if not os.path.exists(path_df):

        df = pd.DataFrame()

        for user in tqdm(dict_sns['users']):
            flag = False
            user_data = 0

            timestamps = list(dict_sns['users'][user]['timestamps'])
            for timestamp in timestamps:
                dict_temp_screen = {}

                if flag:
                    break

                with open(os.path.join(json_files_path, user + '_' + timestamp + '.json')) as json_file:
                    json_text = json.load(json_file)

                    for j in json_text[sensor]:
                        if j['screen'] in dict_sns['users'][user]['timestamps'][timestamp]['screens']:

                            if j['screen'] not in dict_temp_screen:
                                dict_temp_screen[j['screen']] = {'nod': 0}

                            if dict_temp_screen[j['screen']]['nod'] == \
                                    dict_sns['users'][user]['timestamps'][timestamp]['screens'][j['screen']]['nod']:
                                continue

                            # if j['x'] == 0 and j['y'] == 0:
                            #     continue

                            df_row = {
                                'user': user,
                                'timestamp': int(timestamp),
                                'screen': j['screen'],
                                'x': j['x'],
                                'y': j['y'],
                                'z': j['z'],
                                'magnitude': np.sqrt(j['x']**2 + j['y']**2 + j['z']**2),
                                'combine_angle': np.sqrt(j['y']**2 + j['z']**2)
                            }
                            df = df.append(df_row, ignore_index=True)
                            dict_temp_screen[j['screen']]['nod'] += 1

                            user_data += 1
                            if user_data == dict_cases[case_name]['CreateDataframes']['sns']['max_user_data']:
                                flag = True
                                break

        df.to_csv(path_df, index=False)
        print('     ' + sensor + ' dataframe saved at: ', path_df)

    else:

        df = pd.read_csv(path_df)
        print('     ' + sensor + ' dataframe loaded from: ', path_df)

    print('     ' + sensor + ' dataframe size: ', df.shape[0])
    print('')

    return df


def create_df_ges(case_name: str, screen_path: str, dict_ges: dict) -> pd.DataFrame:

    print(' - Creating gestures dataframe.')
    path_df = os.path.join(screen_path, 'df_ges.csv')

    if not os.path.exists(path_df):

        m = MongoDBHandler('mongodb://localhost:27017/', gestures_database_name)
        d = DBDataHandler(m)

        df = pd.DataFrame()

        for user in tqdm(dict_ges['users']):
            flag = False
            user_data = 0

            if flag:
                break

            for ges_id in dict_ges['users'][user]['gestures']:

                ges = d.get_gestures({'_id': ObjectId(ges_id)})[0]
                device = d.get_devices({'device_id': ges['device_id']})[0]

                df_row = {
                    'user': user,
                    'screen': ges['screen'],
                    'id': ObjectId(ges_id),
                    'type': ges['type'],
                    'time_start': ges['t_start'],
                    'time_stop': ges['t_stop'],
                    'duration': ges['t_stop'] - ges['t_start'],
                    'data': ges['data'],
                    'device_height': device['height'],
                    'device_width': device['width']
                }
                df = df.append(df_row, ignore_index=True)

                user_data += 1
                if user_data == dict_cases[case_name]['CreateDataframes']['ges']['max_user_data']:
                    flag = True
                    break

        df.to_csv(path_df, index=False)
        print('     Gestures dataframe saved at: ', path_df)

    else:

        df = pd.read_csv(path_df)
        print('     Gestures dataframe loaded from: ', path_df)

    print('     Gestures dataframe size: ', df.shape[0])
    print('')

    return df
