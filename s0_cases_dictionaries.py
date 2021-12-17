"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ================= #
#    Dictionaries    #
# ================== #
import cases.case1.case_subclasses

json_files_path = 'D:\_Projects_\Thesis_ContinuousImplicitAuthentication\Datasets\BrainRun\sensors_data'
gestures_database_name = 'BrainRun_GestureDevicesUsersGames'

dict_cases = {

    # After meeting 30/11/2021
    'case1': {
        'comments': '',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 5,
            'sns': {
                'min_nod_per_screen': 1,
                'min_nod_per_timestamp': 2,
                'min_nod_per_user': 3000,
                'max_nod_per_user': float('inf')
            },
            'ges': {
                'device_max_width': 600,
                'device_max_height': 1000,
                'fake_swp_limit': 30,
                'swp_min_data_points': 4,
                'swp_max_data_points': 10,
                'min_nog_per_user': 300,
                'max_nog_per_user': float('inf')
            }
        },
        'CreateDataframes': {
            'sns': {'max_user_data': 20000},
            'ges': {'max_user_data': 2000}
        },
        'GetResults': {
            'split_rate': 0.3,
            'FeatureExtraction': {
                'sns': {
                    'lvl0_ftr': 'magnitude',
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': 500,  # 500 samples in 10 sec
                    'overlap': 0.9
                },
                'ges': {
                    'normalize': True,
                    'default_width': 400,
                    'default_height': 700
                }
            },
            'Classifiers': {
                'acc': cases.case1.case_subclasses.AccClassifier,
                'gyr': cases.case1.case_subclasses.GyrClassifier,
                'swp': cases.case1.case_subclasses.SwpClassifier,
                'tap': cases.case1.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    }
}
