"""
This script was created at 05-Sep-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os
import json
from tqdm import tqdm
from bson.objectid import ObjectId

from _cases_dictionaries import json_files_path, gestures_database_name, dict_cases
from s0_Helpers_Functions import *


# =============== #
#    Functions    #
# =============== #
def explore_sns_data(case_name: str, screen_path: str, screen_name: str, sensor: str) -> dict:

    print(' - Exploring', sensor, 'data.')
    path_save = os.path.join(screen_path, 'users_dict_' + sensor[0:3] + '.json')

    if not os.path.exists(path_save):

        output_dict = {

            'json_files_path': json_files_path,
            'data_type': sensor,
            'screen_name': screen_name,
            'synced_screen': dict_cases[case_name]['ExploreData']['sns']['synced_screen'],
            'min_nod_per_screen': dict_cases[case_name]['ExploreData']['sns']['min_nod_per_screen'],
            'min_nod_per_timestamp': dict_cases[case_name]['ExploreData']['sns']['min_nod_per_timestamp'],
            'num_of_users_found': 0,
            'users': {}
        }

        # List *.json files
        json_files = [pos_json for pos_json in os.listdir(json_files_path) if pos_json.endswith('.json')]

        for json_file in tqdm(json_files):

            user = json_file.replace('.json', '').split('_')[0]
            timestamp_str = json_file.replace('.json', '').split('_')[1]

            if user not in output_dict['users']:
                output_dict['users'][user] = {'nod': 0, 'timestamps': {}}

            timestamp = {'nod': 0, 'screens': {}}
            screens = {}

            with open(os.path.join(json_files_path, json_file)) as js:
                json_text = json.load(js)

                # Find number of acc and gyr data in valid screens
                for i in json_text[sensor]:
                    if screen_name in i['screen']:

                        if i['screen'] not in screens:
                            screens[i['screen']] = {'nod': 0}

                        if i['x'] != 0 and i['y'] != 0:
                            screens[i['screen']]['nod'] += 1

            # If a screen pass the min data limitation put it in the timestamps dict
            for screen in screens:
                if screens[screen]['nod'] >= output_dict['min_nod_per_screen']:
                    timestamp['screens'][screen] = screens[screen]
                    timestamp['nod'] += screens[screen]['nod']

            # If a timestamp pass the min data limitation put it in the users dict
            if timestamp['nod'] >= output_dict['min_nod_per_timestamp']:
                output_dict['users'][user]['timestamps'][timestamp_str] = timestamp
                output_dict['users'][user]['nod'] += timestamp['nod']

        # Remove users without data
        initial_users_list = list(output_dict['users'])
        for user in initial_users_list:
            if output_dict['users'][user]['nod'] == 0:
                output_dict['users'].pop(user)

        # Find final number of users
        output_dict['num_of_users_found'] = len(output_dict['users'])

        # Save dict in a .json file
        with open(path_save, 'w') as fp:
            json.dump(output_dict, fp)
        print('     ' + sensor + ' dict saved in: ', path_save)

    else:

        f = open(path_save, )
        output_dict = json.load(f)
        print('     ' + sensor + ' dict loaded from: ', path_save)
        f.close()

    print('     ' + str(output_dict['num_of_users_found']), 'Users with valid ' + sensor + ' data found.')
    print('')

    return output_dict


def explore_swp_data(case_name: str, screen_path: str, screen_name: str) -> dict:

    print(' - Exploring swipes data.')
    path_save = os.path.join(screen_path, 'users_dict_swp.json')

    if not os.path.exists(path_save):

        output_dict = {
            'gestures_database_name': gestures_database_name,
            'data_type': 'Swipes',
            'screen_name': screen_name,
            'device_max_width': dict_cases[case_name]['ExploreData']['swp']['device_max_width'],
            'device_max_height': dict_cases[case_name]['ExploreData']['swp']['device_max_height'],
            'fake_swp_limit': dict_cases[case_name]['ExploreData']['swp']['fake_swp_limit'],
            'swp_min_data_points': dict_cases[case_name]['ExploreData']['swp']['swp_min_data_points'],
            'swp_max_data_points': dict_cases[case_name]['ExploreData']['swp']['swp_max_data_points'],
            'num_of_users_found': 0,
            'users': {}
        }

        # Get data
        m = MongoDBHandler('mongodb://localhost:27017/', gestures_database_name)
        d = DBDataHandler(m)

        users = d.get_users()
        for user in tqdm(users):
            if 'xp' in user:

                # Remove usernames with problems
                if ((user['xp'] > 1) and ('deth' not in user['username']) and ('Marpap' not in user['username']) and
                        ('Johnys' not in user['username']) and ('Tenebrific' not in user['username']) and
                        ('Sherlocked' not in user['username']) and ('kavouras' not in user['username'])):

                    output_dict['users'][user['player_id']] = {'nos': 0, 'swipes': {}}

                    devices = d.get_devices({'user_id': ObjectId(user['_id'])})
                    for device in devices:

                        # Remove kiosk device and devices with big dimensions (not mobile phones)
                        if 'TouchScreen' not in device['device_id'] and \
                                device['width'] < output_dict['device_max_width'] and \
                                device['height'] < output_dict['device_max_height']:

                            gestures = d.get_gestures_from_device(device['device_id'])
                            for gesture in gestures:
                                if gesture['type'] == 'swipe':
                                    if output_dict['screen_name'] in gesture['screen']:
                                        if gesture['t_start'] == -1 or gesture['t_stop'] == -1:
                                            continue

                                        # Fake swipes limit
                                        if gesture['t_stop'] - gesture['t_start'] < output_dict['fake_swp_limit']:
                                            continue

                                        # Data length limitations
                                        if output_dict['swp_min_data_points'] <= len(gesture['data']) \
                                                <= output_dict['swp_max_data_points']:
                                            output_dict['users'][user['player_id']]['swipes'][str(gesture['_id'])] = {
                                                'swipe_screen': gesture['screen'],
                                                'swipe_time_start': gesture['t_start'],
                                                'swipe_time_stop': gesture['t_stop']
                                            }
                                            output_dict['users'][user['player_id']]['nos'] += 1

        # Remove users without data
        initial_users_list = list(output_dict['users'])
        for user in initial_users_list:
            if output_dict['users'][user]['nos'] == 0:
                output_dict['users'].pop(user)

        output_dict['num_of_users_found'] = len(output_dict['users'])

        # Save dict in a .json file
        with open(path_save, 'w') as fp:
            json.dump(output_dict, fp)
        print('     Swipes dict saved in: ', path_save)

    else:

        f = open(path_save, )
        output_dict = json.load(f)
        print('     Swipes dict loaded from: ', path_save)
        f.close()

    print('     ' + str(output_dict['num_of_users_found']), 'Users with valid swipes data found.')
    print('')

    return output_dict


def select_users(case_name: str, screen_path: str, dict_acc: dict, dict_gyr: dict, dict_swp: dict):

    print(' - Selecting common users with specific data limits.')
    path_fnl_acc = os.path.join(screen_path, 'users_dict_acc_fnl.json')
    path_fnl_gyr = os.path.join(screen_path, 'users_dict_gyr_fnl.json')
    path_fnl_swp = os.path.join(screen_path, 'users_dict_swp_fnl.json')

    if not (os.path.exists(path_fnl_acc) or os.path.exists(path_fnl_gyr) or os.path.exists(path_fnl_swp)):

        # Synced sensor data -> TO DO!!!
        # Synced sensor with swipes data -> From previous experiments are not enough.

        # Define users data limits
        dict_acc['min_nod_per_user'] = dict_cases[case_name]['ExploreData']['sns']['min_nod_per_user']
        dict_acc['max_nod_per_user'] = dict_cases[case_name]['ExploreData']['sns']['max_nod_per_user']
        dict_gyr['min_nod_per_user'] = dict_cases[case_name]['ExploreData']['sns']['min_nod_per_user']
        dict_gyr['max_nod_per_user'] = dict_cases[case_name]['ExploreData']['sns']['max_nod_per_user']
        dict_swp['min_nos_per_user'] = dict_cases[case_name]['ExploreData']['swp']['min_nos_per_user']
        dict_swp['max_nos_per_user'] = dict_cases[case_name]['ExploreData']['swp']['max_nos_per_user']

        # If a user do not pass the min, max data limitation delete it
        for sensor_dict in [dict_acc, dict_gyr]:
            initial_users_list = list(sensor_dict['users'])
            for user in initial_users_list:
                if sensor_dict['users'][user]['nod'] < sensor_dict['min_nod_per_user'] or \
                        sensor_dict['users'][user]['nod'] > sensor_dict['max_nod_per_user']:
                    sensor_dict['users'].pop(user)
            sensor_dict['num_of_users_found'] = len(sensor_dict['users'])

        initial_users_list = list(dict_swp['users'])
        for user in initial_users_list:
            if dict_swp['users'][user]['nos'] < dict_swp['min_nos_per_user'] or \
                    dict_swp['users'][user]['nos'] > dict_swp['max_nos_per_user']:
                dict_swp['users'].pop(user)
        dict_swp['num_of_users_found'] = len(dict_swp['users'])

        # Select common users among three dicts.
        common_users = list(set(list(set(list(dict_acc['users'])).intersection(list(dict_gyr['users']))))
                            .intersection(list(dict_swp['users'])))

        for data_dict in [dict_acc, dict_gyr, dict_swp]:
            initial_users_list = list(data_dict['users'])
            for user in initial_users_list:
                if user not in common_users:
                    data_dict['users'].pop(user)
            data_dict['num_of_users_found'] = len(data_dict['users'])

        # Save dicts
        dict_fnl_acc = dict_acc
        with open(path_fnl_acc, 'w') as dict_temp:
            json.dump(dict_fnl_acc, dict_temp)
        print('     Accelerometer final dict saved in: ', path_fnl_acc)

        dict_fnl_gyr = dict_gyr
        with open(path_fnl_gyr, 'w') as dict_temp:
            json.dump(dict_fnl_gyr, dict_temp)
        print('     Gyroscope final dict saved in: ', path_fnl_gyr)

        dict_fnl_swp = dict_swp
        with open(path_fnl_swp, 'w') as dict_temp:
            json.dump(dict_fnl_swp, dict_temp)
        print('     Swipes final dict saved in: ', path_fnl_swp)

    else:

        f = open(path_fnl_acc, )
        dict_fnl_acc = json.load(f)
        print('     Accelerometer final dict loaded from: ', path_fnl_acc)
        f.close()

        f = open(path_fnl_gyr, )
        dict_fnl_gyr = json.load(f)
        print('     Gyroscope final dict loaded from: ', path_fnl_gyr)
        f.close()

        f = open(path_fnl_swp, )
        dict_fnl_swp = json.load(f)
        print('     Swipes final dict loaded from: ', path_fnl_swp)
        f.close()

    print('     ' + str(dict_fnl_acc['num_of_users_found']), 'Final users selected.')
    print('')

    return dict_fnl_acc, dict_fnl_gyr, dict_fnl_swp
