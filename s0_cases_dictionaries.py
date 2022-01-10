"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ================= #
#    Dictionaries    #
# ================== #
import cases.case1.case_subclasses
import cases.case6.case_subclasses
import cases.case7.case_subclasses

json_files_path = 'D:\_Projects_\Thesis_ContinuousImplicitAuthentication\Datasets\BrainRun\sensors_data'
gestures_database_name = 'BrainRun_GestureDevicesUsersGames'

dict_cases = {

    # quest 01: Find acc, gyr lvl0 features
    # 20211227: y biggest variation among users not in acc & gyr
    # 20211227: a user data min/max variation in acc magnitude/y, in gyr x/magnitude
    # 20220106: case6 use x, y, magnitude together and update scripts
    # 20220106: case6 best performance in average (screens, FRR, FAR)
    'case1': {
        'comments': 'y is the 0 lvl feature for sensors',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
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
        'FeatureExtraction': {
            'sns': {
                'lvl0_ftr': {'acc': ['y'], 'gyr': ['y']},
                'sample_rate': 20,  # 20ms, 50Hz
                'window': {'acc': 500, 'gyr': 500},  # 500 samples in 10 sec
                'overlap': {'acc': 0.9, 'gyr': 0.9}
            },
            'ges': {
                'normalize': True,
                'default_width': 400,
                'default_height': 700
            }
        },
        'GetResults': {
            'split_rate': 0.3,
            'Classifiers': {
                'acc': cases.case1.case_subclasses.AccClassifier,
                'gyr': cases.case1.case_subclasses.GyrClassifier,
                'swp': cases.case1.case_subclasses.SwpClassifier,
                'tap': cases.case1.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },
    'case2': {
        'comments': 'magnitude is the 0 lvl feature for sensors',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
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
        'FeatureExtraction': {
            'sns': {
                'lvl0_ftr': {'acc': ['magnitude'], 'gyr': ['magnitude']},
                'sample_rate': 20,  # 20ms, 50Hz
                'window': {'acc': 500, 'gyr': 500},  # 500 samples in 10 sec
                'overlap': {'acc': 0.9, 'gyr': 0.9}
            },
            'ges': {
                'normalize': True,
                'default_width': 400,
                'default_height': 700
            }
        },
        'GetResults': {
            'split_rate': 0.3,
            'Classifiers': {
                'acc': cases.case1.case_subclasses.AccClassifier,
                'gyr': cases.case1.case_subclasses.GyrClassifier,
                'swp': cases.case1.case_subclasses.SwpClassifier,
                'tap': cases.case1.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },
    'case3': {
        'comments': 'x is the 0 lvl feature for sensors',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
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
        'FeatureExtraction': {
            'sns': {
                'lvl0_ftr': {'acc': ['x'], 'gyr': ['x']},
                'sample_rate': 20,  # 20ms, 50Hz
                'window': {'acc': 500, 'gyr': 500},  # 500 samples in 10 sec
                'overlap': {'acc': 0.9, 'gyr': 0.9}
            },
            'ges': {
                'normalize': True,
                'default_width': 400,
                'default_height': 700
            }
        },
        'GetResults': {
            'split_rate': 0.3,
            'Classifiers': {
                'acc': cases.case1.case_subclasses.AccClassifier,
                'gyr': cases.case1.case_subclasses.GyrClassifier,
                'swp': cases.case1.case_subclasses.SwpClassifier,
                'tap': cases.case1.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },
    'case6': {
        'comments': 'more than one lvl0 features, scripts changed.',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
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
        'FeatureExtraction': {
            'sns': {
                'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                'sample_rate': 20,  # 20ms, 50Hz
                'window': {'acc': 400, 'gyr': 400},  # 8 sec
                'overlap': {'acc': 0.9, 'gyr': 0.9}
            },
            'ges': {
                'normalize': True,
                'default_width': 400,
                'default_height': 700
            }
        },
        'GetResults': {
            'split_rate': 0.3,
            'Classifiers': {
                'acc': cases.case6.case_subclasses.AccClassifier,
                'gyr': cases.case6.case_subclasses.GyrClassifier,
                'swp': cases.case6.case_subclasses.SwpClassifier,
                'tap': cases.case6.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },

    # quest 02: Select sensors window and overlap (Scripts modification needed!)
    # 20211229: Dynamic overlap (case5) is better, best performance in acc and gyr window = 400, overlap = 0.9
    # 20220107: case8 Dynamic overlap but with case6 sns lvl0 features
    # 20220110: from case8 best dynamic overlap, for acc 200 0.9 & for gyr 400 0.9
    'case4': {
        'comments': 'In the sensors feature extraction OVERLAP is static.',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
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
        'FeatureExtraction': {
            'sns': {
                'lvl0_ftr': {'acc': ['magnitude'], 'gyr': ['magnitude']},
                'sample_rate': 20,  # 20ms, 50Hz
                'window': [25, 50, 100, 200, 400, 500, 800, 1600],  # 500 samples in 10 sec
                'overlap': [0.0, 0.1, 0.2, 0.4, 0.8, 0.9]
            },
            'ges': {
                'normalize': True,
                'default_width': 400,
                'default_height': 700
            }
        },
        'GetResults': {
            'split_rate': 0.3,
            'Classifiers': {
                'acc': cases.case1.case_subclasses.AccClassifier,
                'gyr': cases.case1.case_subclasses.GyrClassifier,
                'swp': cases.case1.case_subclasses.SwpClassifier,
                'tap': cases.case1.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },
    'case5': {
        'comments': 'In the sensors feature extraction OVERLAP is dynamic.',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
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
        'FeatureExtraction': {
            'sns': {
                'lvl0_ftr': {'acc': ['magnitude'], 'gyr': ['magnitude']},
                'sample_rate': 20,  # 20ms, 50Hz
                'window': [25, 50, 100, 200, 400, 500, 800, 1600],  # 500 samples in 10 sec
                'overlap': [0.0, 0.1, 0.2, 0.4, 0.8, 0.9]
            },
            'ges': {
                'normalize': True,
                'default_width': 400,
                'default_height': 700
            }
        },
        'GetResults': {
            'split_rate': 0.3,
            'Classifiers': {
                'acc': cases.case1.case_subclasses.AccClassifier,
                'gyr': cases.case1.case_subclasses.GyrClassifier,
                'swp': cases.case1.case_subclasses.SwpClassifier,
                'tap': cases.case1.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },
    'case8': {
        'comments': 'more than one lvl0 features, scripts changed.',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
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
        'FeatureExtraction': {
            'sns': {
                'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                'sample_rate': 20,  # 20ms, 50Hz
                'window': [25, 50, 100, 200, 400, 500, 800, 1600],  # 8 sec
                'overlap': [0.0, 0.1, 0.2, 0.4, 0.8, 0.9]
            },
            'ges': {
                'normalize': True,
                'default_width': 400,
                'default_height': 700
            }
        },
        'GetResults': {
            'split_rate': 0.3,
            'Classifiers': {
                'acc': cases.case7.case_subclasses.AccClassifier,
                'gyr': cases.case7.case_subclasses.GyrClassifier,
                'swp': cases.case7.case_subclasses.SwpClassifier,
                'tap': cases.case7.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },

    # quest 03: Find sensors and gestures lvl1 features
    # 20220106: case7 select final features for acc, gyr and ges
    # 20220110: case9 use case8 results
    # 20220110: final features at case7 case_subclasses.py
    'case7': {
        'comments': 'more than one lvl0 features, scripts changed.',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
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
        'FeatureExtraction': {
            'sns': {
                'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                'sample_rate': 20,  # 20ms, 50Hz
                'window': {'acc': 400, 'gyr': 400},  # 8 sec
                'overlap': {'acc': 0.9, 'gyr': 0.9}
            },
            'ges': {
                'normalize': True,
                'default_width': 400,
                'default_height': 700
            }
        },
        'GetResults': {
            'split_rate': 0.3,
            'Classifiers': {
                'acc': cases.case7.case_subclasses.AccClassifier,
                'gyr': cases.case7.case_subclasses.GyrClassifier,
                'swp': cases.case7.case_subclasses.SwpClassifier,
                'tap': cases.case7.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },
    'case9': {
        'comments': 'more than one lvl0 features, scripts changed.',
        'screens': ['Mathisis', 'Focus', 'Reacton', 'Speedy', 'Memoria'],
        'ExploreData': {
            'max_users': 15,
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
        'FeatureExtraction': {
            'sns': {
                'lvl0_ftr': {'acc': ['x', 'y', 'magnitude'], 'gyr': ['x', 'y', 'magnitude']},
                'sample_rate': 20,  # 20ms, 50Hz
                'window': {'acc': 200, 'gyr': 200},  # 4 sec
                'overlap': {'acc': 0.9, 'gyr': 0.9}
            },
            'ges': {
                'normalize': True,
                'default_width': 400,
                'default_height': 700
            }
        },
        'GetResults': {
            'split_rate': 0.3,
            'Classifiers': {
                'acc': cases.case7.case_subclasses.AccClassifier,
                'gyr': cases.case7.case_subclasses.GyrClassifier,
                'swp': cases.case7.case_subclasses.SwpClassifier,
                'tap': cases.case7.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    }
}
