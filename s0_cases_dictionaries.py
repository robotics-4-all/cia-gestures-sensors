"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ================= #
#    Dictionaries    #
# ================== #
import cases.case1.case_subclasses
import cases.case7.case_subclasses

json_files_path = 'D:\_Projects_\Thesis_ContinuousImplicitAuthentication\Datasets\BrainRun\sensors_data'
gestures_database_name = 'BrainRun_GestureDevicesUsersGames'

dict_cases = {

    # quest 01: Find acc, gyr lvl0 features
    # 20211217: why aggelikh magnitude?
    # 20211217: from quests best y for both but divide0 error
    # 20211227: from cases y-magnitude similar, maybe acc-magnitude & gyr-y, so magnitude for both due to y error
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
        'GetResults': {
            'split_rate': 0.3,
            'FeatureExtraction': {
                'sns': {
                    'lvl0_ftr': {'acc': 'y', 'gyr': 'y'},
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
        'GetResults': {
            'split_rate': 0.3,
            'FeatureExtraction': {
                'sns': {
                    'lvl0_ftr': {'acc': 'magnitude', 'gyr': 'magnitude'},
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
        'GetResults': {
            'split_rate': 0.3,
            'FeatureExtraction': {
                'sns': {
                    'lvl0_ftr': {'acc': 'x', 'gyr': 'x'},
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
    },


    # quest 02: Select sensors window and overlap
    # 20211227: To run this cases, scripts need to be modified for grid search.
    # 20211229: Dynamic overlap (case5), best performance in acc and gyr window = 400, overlap = 0.9
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
        'GetResults': {
            'split_rate': 0.3,
            'FeatureExtraction': {
                'sns': {
                    'lvl0_ftr': {'acc': 'magnitude', 'gyr': 'magnitude'},
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
        'GetResults': {
            'split_rate': 0.3,
            'FeatureExtraction': {
                'sns': {
                    'lvl0_ftr': {'acc': 'magnitude', 'gyr': 'magnitude'},
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
            'Classifiers': {
                'acc': cases.case1.case_subclasses.AccClassifier,
                'gyr': cases.case1.case_subclasses.GyrClassifier,
                'swp': cases.case1.case_subclasses.SwpClassifier,
                'tap': cases.case1.case_subclasses.TapClassifier
            },
            'Evaluator': {}
        }
    },

    # quest 03: Find sensors and gestures lvl1 features
    'case6': {
        'comments': 'Some features as previous cases.',
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
        'GetResults': {
            'split_rate': 0.3,
            'FeatureExtraction': {
                'sns': {
                    'lvl0_ftr': {'acc': 'magnitude', 'gyr': 'magnitude'},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': 400,  # 8 sec
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
    },
    'case7': {
        'comments': 'All features.',
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
        'GetResults': {
            'split_rate': 0.3,
            'FeatureExtraction': {
                'sns': {
                    'lvl0_ftr': {'acc': 'magnitude', 'gyr': 'magnitude'},
                    'sample_rate': 20,  # 20ms, 50Hz
                    'window': 400,  # 8 sec
                    'overlap': 0.9
                },
                'ges': {
                    'normalize': True,
                    'default_width': 400,
                    'default_height': 700
                }
            },
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
