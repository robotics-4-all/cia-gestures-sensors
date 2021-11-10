"""
This script was created at 13-Sep-21
author: eachrist

"""
#  ================= #
#    Dictionaries    #
# ================== #
import cases.case1.case_subclasses

'''
Mathisis -> swipe
Focus -> swipe
Reacton -> swipe, tap
Memoria -> tap
Speedy -> tap
'''

json_files_path = 'D:\_Projects_\Thesis_ContinuousImplicitAuthentication\Datasets\BrainRun\sensors_data'
gestures_database_name = 'BrainRun_GestureDevicesUsersGames'

dict_cases = {
    'case2': {
        'comments': '',
        'screens': ['Reacton'],

        'gesture_type': 'tap',

        'ExploreData': {
            'sns': {
                'synced_screen': False,
                'min_nod_per_screen': 1,
                'min_nod_per_timestamp': 1,

                'min_nod_per_user': 4000,
                'max_nod_per_user': 16000

            },

            'ges': {
                'device_max_width': 600,
                'device_max_height': 1000,

                'fake_swp_limit': 30,
                'swp_min_data_points': 4,
                'swp_max_data_points': 10,

                'min_nog_per_user': 50,
                'max_nog_per_user': 300
            },
        },

        'ExtractFeatures': {
            'sns': {
                'extraction_type': 'User',  # User, Timestamp, TimestampScreen, Screen
                'feature': 'magnitude',  # magnitude, combine_angle, x, y, z
                'window': 200,
                'overlap': 0.9
            },

            'ges': {
                'normalize': True
            }
        },

        'GetResults': {
            'acc': cases.case1.case_subclasses.AccClf,
            'gyr': cases.case1.case_subclasses.GyrClf,
            'ges': cases.case1.case_subclasses.GesClf,
            'ttl': cases.case1.case_subclasses.Ensemble,
        }
    }
}
