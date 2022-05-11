"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ================ #
#    Classifiers    #
# ================= #
import cases.case01.subclasses_classifiers  # single 0 lvl feature classifiers
import cases.case05.subclasses_classifiers  # multiple 0 lvl feature classifiers
import cases.case06.subclasses_classifiers  # classifier with final features
import cases.case08.subclasses_classifiers  # like case06 but modified for quest04
import cases.case09.subclasses_classifiers  # like case06 but modified for quest04
import cases.case10.subclasses_classifiers  # like case06 but modified for quest05
import cases.case11.subclasses_classifiers  # like case06 but specified FRR~FAR regions according to case09
import cases.case17.subclasses_classifiers  # like case08 but design for case16 (case15 eval + LOF) grid search
import cases.case18.subclasses_classifiers  # like case17 but zoom in specific regions
import cases.case19.subclasses_classifiers  # use case18 regions, find optimal num of classifiers
import cases.case20.subclasses_classifiers  # use case18 regions and final num of optimal classifiers, FAR~FRR
import cases.case21.subclasses_classifiers  # case20 but FRR < FAR
import cases.case22.subclasses_classifiers  # case20 but FRR > FAR


#  =============== #
#    Evaluators    #
# ================ #
import cases.case01.subclasses_evaluator  # starting evaluator
import cases.case04.subclasses_evaluator  # like case01 but for quest02
import cases.case08.subclasses_evaluator  # like case01 but for quest04, quest05
import cases.case12.subclasses_evaluator  # case01 but confidence_step *= sample_decision
import cases.case13.subclasses_evaluator  # case01 but confidence_step *= FRR_trn
import cases.case14.subclasses_evaluator  # case01 but combine case12 & case13
import cases.case15.subclasses_evaluator  # case14 but change confidence_step & add 2 new metrics
import cases.case26.subclasses_evaluator
import cases.case27.subclasses_evaluator

#  =============== #
#    Dictionary    #
# ================ #
json_files_path = 'D:\_Projects_\Thesis_ContinuousImplicitAuthentication\Datasets\BrainRun\sensors_data'
gestures_database_name = 'BrainRun_GestureDevicesUsersGames'

dict_cases = {

    # quest 01: Find acc, gyr lvl0 features
    # 20211227: y biggest variation among users not in acc & gyr
    # 20211227: a user data min/max variation in acc magnitude/y, in gyr x/magnitude
    # 20220106: case05 use x, y, magnitude together and update scripts
    'case01': {
        'comments': 'y is the 0 lvl feature for sensors',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['y'], 'gyr': ['y']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 500, 'gyr': 500},  # 500 samples in 10 sec
                    'overlap': {'acc': 0.9, 'gyr': 0.9}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case01.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case01.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case01.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case01.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case01.subclasses_evaluator.CaseEvaluator}},
    'case02': {
        'comments': 'magnitude is the 0 lvl feature for sensors',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['magnitude'], 'gyr': ['magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 500, 'gyr': 500},  # 500 samples in 10 sec
                    'overlap': {'acc': 0.9, 'gyr': 0.9}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case01.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case01.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case01.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case01.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case01.subclasses_evaluator.CaseEvaluator}},
    'case03': {
        'comments': 'x is the 0 lvl feature for sensors',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x'], 'gyr': ['x']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 500, 'gyr': 500},  # 500 samples in 10 sec
                    'overlap': {'acc': 0.9, 'gyr': 0.9}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case01.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case01.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case01.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case01.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case01.subclasses_evaluator.CaseEvaluator}},
    'case05': {
        'comments': 'more than one lvl0 features, scripts changed.',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case05.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case05.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case05.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case05.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case01.subclasses_evaluator.CaseEvaluator}},

    # quest 02: Select sensors window and overlap (Scripts modification needed!)
    # 20211229: case04, FAR good for window >= 50 and bigger overlaps both for acc & gyr
    # 20211229: case04, FRR_tst good for window <= 100, for some bigger overlaps not so good both for acc & gyr
    # 20211229: case04, lets try window = 50 and overlap = 0.6 both in acc & gyr
    # 20220107: case07, lets maintain previous choices
    'case04': {
        'comments': 'Grid search',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['magnitude'], 'gyr': ['magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': [25, 50, 100, 200, 400, 500, 800, 1600],  # 500 samples in 10 sec
                    'overlap': [0.0, 0.1, 0.2, 0.4, 0.8, 0.9]},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case01.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case01.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case01.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case01.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case04.subclasses_evaluator.CaseEvaluator}},
    'case07': {
        'comments': 'Grid search with case06 features',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': [25, 50, 100, 200, 400, 500, 800, 1600],  # 8 sec
                    'overlap': [0.0, 0.1, 0.2, 0.4, 0.8, 0.9]},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case06.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case06.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case06.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case06.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case04.subclasses_evaluator.CaseEvaluator}},

    # quest 03: Find sensors and gestures lvl1 features
    # 20220106: case06, select final features for acc, gyr and ges, final features at case06 subclasses_evaluator.py
    'case06': {
        'comments': 'Case with final features selected',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case06.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case06.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case06.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case06.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case01.subclasses_evaluator.CaseEvaluator}},

    # quest 04: Find SVMs optimal parameters (Scripts modification needed!)
    # 20220111: case08, grid search nu, gamma both in (0, 1) for all data, case08 evaluator
    # 20220113: case09, case08 but search in FRR~FAR regions for all modules
    # 20220131: case17, grid search nu, gamma both in (0, 1) for all data, like case16 (case15 evaluator + LOF)
    # 20220201: case18, case17 but search in FRR~FAR regions for all modules
    'case08': {
        'comments': 'Grid search',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'nus': list(range(22)),
                            'gammas': list(range(27)),
                            'acc': cases.case08.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case08.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case08.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case08.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case08.subclasses_evaluator.CaseEvaluator}},
    'case09': {
        'comments': 'Grid search in region where FRR~FAR',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'nus': list(range(15)),
                            'gammas': list(range(20)),
                            'acc': cases.case09.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case09.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case09.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case09.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case08.subclasses_evaluator.CaseEvaluator}},
    'case17': {
        'comments': 'grid search for case16',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case17.subclasses_classifiers.features,
            'Classifiers': {'nus': list(range(22)),
                            'gammas': list(range(27)),
                            'acc': cases.case17.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case17.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case17.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case17.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},
    'case18': {
        'comments': 'grid search for case16 but in spesific regions',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case18.subclasses_classifiers.features,
            'Classifiers': {'nus': list(range(20)),
                            'gammas': list(range(20)),
                            'acc': cases.case18.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case18.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case18.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case18.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},

    # quest 05: Optimal number of classifiers that decide (Scripts modification needed!)
    # 20220117: case10, case09 evaluator & case08 evaluator => 50 classifiers to decide
    # 20220204: case19, case15 evaluator + LOF (case16) & case21 regions
    'case10': {
        'comments': 'Search for optimal number of classifiers.',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'num_of_clf_that_decide': [1, 5, 15, 50, 100, 200, 300],
                            'acc': cases.case10.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case10.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case10.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case10.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case08.subclasses_evaluator.CaseEvaluator}},
    'case19': {
        'comments': 'Search for optimal number of classifiers.',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case19.subclasses_classifiers.features,
            'Classifiers': {'num_of_clf_that_decide': [1, 5, 15, 30, 60, 100, 200, 300],
                            'acc': cases.case19.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case19.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case19.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case19.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},

    # quest 06: Evaluator optimization methods
    # 20220117: case11, use case10 results, case01 evaluator & case09 regions
    # 20220118: case12, case11 classifier, in evaluator confidence_step *= sample_decision => better FRR worse FAR
    # 20220118: case13, case11 classifier, in evaluator confidence_step *= FRR_trn => better FRR worse FAR
    # 20220118: case14, case11 classifier, in evaluator combine case12 and case13 => best FRR worst FAR
    # 20220131: case15, case11 classifier, in evaluator combine case14, new confidence_steps & add 2 new metrics
    # 20220131: case16, case11 classifier & case15 evaluator but run LOF before training
    'case11': {
        'comments': '',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case11.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case11.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case11.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case11.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case01.subclasses_evaluator.CaseEvaluator}},
    'case12': {
        'comments': 'case11 but evaluator confidence step is multiplied with sample decision',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case11.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case11.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case11.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case11.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case12.subclasses_evaluator.CaseEvaluator}},
    'case13': {
        'comments': 'case11 but evaluator confidence step is multiplied by its module FRR_trn',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case11.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case11.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case11.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case11.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case13.subclasses_evaluator.CaseEvaluator}},
    'case14': {
        'comments': 'combine case12 and case13',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case11.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case11.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case11.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case11.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case14.subclasses_evaluator.CaseEvaluator}},
    'case15': {
        'comments': 'combine case14 with new conf steps',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case11.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case11.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case11.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case11.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},
    'case15.2': {
        'comments': 'combine case14 with new conf steps',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'Classifiers': {'acc': cases.case11.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case11.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case11.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case11.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},
    'case16': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case11.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case11.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case11.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case11.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case11.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},

    # 15 users
    # 20220205: case20, final FRR~FAR
    # 20220205: case21, final FRR < FAR
    # 20220205: case22, final FRR > FAR
    'case20': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case20.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case20.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case20.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case20.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case20.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},
    'case21': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case21.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case21.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case21.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case21.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case21.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},
    'case22': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case22.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case22.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case22.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case22.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case22.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},

    # MORE users
    # 20220205: case23, final FRR~FAR
    # 20220205: case24, final FRR < FAR
    # 20220205: case25, final FRR > FAR
    'case23': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 60,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case20.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case20.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case20.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case20.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case20.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},
    'case23.2': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 60,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': False,
            'features': cases.case20.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case20.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case20.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case20.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case20.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},
    'case24': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 60,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case21.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case21.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case21.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case21.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case21.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},
    'case25': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 60,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case20.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case22.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case22.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case22.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case22.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}},

    # 20220308: case26, MORE users, final FRR~FAR, no gyr (temp edit case15 evaluator)
    'case26': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 60,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case20.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case20.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case20.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case20.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case20.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case26.subclasses_evaluator.CaseEvaluator}},

    # 20220308: case27, MORE users, final FRR~FAR, no acc (temp edit case15 evaluator)
    'case27': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 60,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case20.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case20.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case20.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case20.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case20.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case27.subclasses_evaluator.CaseEvaluator}},

    # 20220308: case28, MORE users, final FRR~FAR, no swp (temp edit case15 evaluator)
    'case28': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 60,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case20.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case20.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case20.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case20.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case20.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case27.subclasses_evaluator.CaseEvaluator}},

    # 20220308: case29, remove users used in training from features df
    'case29': {
        'comments': 'combine case14 and LOF before training',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 60,
            'sns': {'min_nod_per_screen': 1,
                    'min_nod_per_timestamp': 2,
                    'min_nod_per_user': 3000,
                    'max_nod_per_user': float('inf')},
            'ges': {'device_max_width': 600,
                    'device_max_height': 1000,
                    'fake_swp_limit': 30,
                    'swp_min_data_points': 4,
                    'swp_max_data_points': 10,
                    'min_nog_per_user': 300,
                    'max_nog_per_user': float('inf')}},
        'CreateDataframes': {'sns': {'max_user_data': 20000},
                             'ges': {'max_user_data': 2000}},
        'FeatureExtraction': {
            'sns': {'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': {'acc': 50, 'gyr': 50},  # 1 sec
                    'overlap': {'acc': 0.6, 'gyr': 0.6}},
            'ges': {'normalize': True,
                    'default_width': 400,
                    'default_height': 700}},
        'GetResults': {
            'split_rate': 0.3,
            'preprocess': True,
            'features': cases.case20.subclasses_classifiers.features,
            'Classifiers': {'acc': cases.case20.subclasses_classifiers.AccClassifier,
                            'gyr': cases.case20.subclasses_classifiers.GyrClassifier,
                            'swp': cases.case20.subclasses_classifiers.SwpClassifier,
                            'tap': cases.case20.subclasses_classifiers.TapClassifier},
            'Evaluator': cases.case15.subclasses_evaluator.CaseEvaluator}}

}
