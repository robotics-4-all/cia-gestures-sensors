"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ================= #
#    Dictionaries    #
# ================== #
import cases.case01.case_subclasses
import cases.case05.case_subclasses
import cases.case06.case_subclasses
import cases.case08.case_subclasses
import cases.case09.case_subclasses

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
                'acc': cases.case01.case_subclasses.AccClassifier,
                'gyr': cases.case01.case_subclasses.GyrClassifier,
                'swp': cases.case01.case_subclasses.SwpClassifier,
                'tap': cases.case01.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },
    'case02': {
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
                'acc': cases.case01.case_subclasses.AccClassifier,
                'gyr': cases.case01.case_subclasses.GyrClassifier,
                'swp': cases.case01.case_subclasses.SwpClassifier,
                'tap': cases.case01.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },
    'case03': {
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
                'acc': cases.case01.case_subclasses.AccClassifier,
                'gyr': cases.case01.case_subclasses.GyrClassifier,
                'swp': cases.case01.case_subclasses.SwpClassifier,
                'tap': cases.case01.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },
    'case05': {
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
                'window': {'acc': 50, 'gyr': 50},  # 1 sec
                'overlap': {'acc': 0.6, 'gyr': 0.6}
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
                'acc': cases.case05.case_subclasses.AccClassifier,
                'gyr': cases.case05.case_subclasses.GyrClassifier,
                'swp': cases.case05.case_subclasses.SwpClassifier,
                'tap': cases.case05.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },

    # quest 02: Select sensors window and overlap (Scripts modification needed!)
    # 20211229: from case04, FAR good for window >= 50 and bigger overlaps both for acc & gyr
    # 20211229: from case04, FRR_tst good for window <= 100, for some bigger overlaps not so good both for acc & gyr
    # 20211229: from case04, lets try window = 50 and overlap = 0.6 both in acc & gyr
    # 20220107: from case07, lets maintain previous choices
    'case04': {
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
                'acc': cases.case01.case_subclasses.AccClassifier,
                'gyr': cases.case01.case_subclasses.GyrClassifier,
                'swp': cases.case01.case_subclasses.SwpClassifier,
                'tap': cases.case01.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },
    'case07': {
        'comments': 'dynamic overlap, more than one lvl0 features, scripts changed.',
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
                'acc': cases.case06.case_subclasses.AccClassifier,
                'gyr': cases.case06.case_subclasses.GyrClassifier,
                'swp': cases.case06.case_subclasses.SwpClassifier,
                'tap': cases.case06.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },

    # quest 03: Find sensors and gestures lvl1 features
    # 20220106: case06 select final features for acc, gyr and ges, final features at case06 case_subclasses.py
    # 20220110: case08 use case07 results
    'case06': {
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
                'window': {'acc': 50, 'gyr': 50},  # 1 sec
                'overlap': {'acc': 0.6, 'gyr': 0.6}
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
                'acc': cases.case06.case_subclasses.AccClassifier,
                'gyr': cases.case06.case_subclasses.GyrClassifier,
                'swp': cases.case06.case_subclasses.SwpClassifier,
                'tap': cases.case06.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },

    # quest 04: Find SVMs optimal parameters (Scripts modification needed!)
    # 20220111: case08 grid search nu, gamma both in (0, 1) for all data
    # 20220113: case09 grid search nu, gamma  with different values for avery data type according to case08 results
    'case08': {
        'comments': '',
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
                'window': {'acc': 50, 'gyr': 50},  # 1 sec
                'overlap': {'acc': 0.6, 'gyr': 0.6}
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
                'nus': list(range(22)),
                'gammas': list(range(27)),
                'acc': cases.case08.case_subclasses.AccClassifier,
                'gyr': cases.case08.case_subclasses.GyrClassifier,
                'swp': cases.case08.case_subclasses.SwpClassifier,
                'tap': cases.case08.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },
    'case09': {
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
                'window': {'acc': 50, 'gyr': 50},  # 1 sec
                'overlap': {'acc': 0.6, 'gyr': 0.6}
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
                'nus': list(range(15)),
                'gammas': list(range(20)),
                'acc': cases.case09.case_subclasses.AccClassifier,
                'gyr': cases.case09.case_subclasses.GyrClassifier,
                'swp': cases.case09.case_subclasses.SwpClassifier,
                'tap': cases.case09.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    }
}
