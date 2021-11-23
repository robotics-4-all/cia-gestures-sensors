"""
This script was created at 13-Sep-21
author: eachrist

"""
#  ================= #
#    Dictionaries    #
# ================== #
import cases.case1.case_subclasses
import cases.case2.case_subclasses
import cases.case3.case_subclasses
import cases.case4.case_subclasses
import cases.case5.case_subclasses
import cases.case6.case_subclasses

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
    'case1': {
        'comments': 'Test acc, gyr, swp with complex models [LOFs, LOFs, SVMs].',

        'screens': ['Mathisis', 'Focus', 'Reacton'],

        'gesture_type': 'swipe',

        'ExploreData': {
            'sns': {
                'min_nod_per_screen': 1,
                'min_nod_per_timestamp': 1,

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
            },
        },

        'CreateDataframes': {
            'sns': {
                'max_user_data': 15000
            }
        },

        'ExtractFeatures': {
            'sns': {
                'extraction_type': 'User',  # User, Timestamp, TimestampScreen, Screen
                'feature': {'acc': 'magnitude', 'gyr': 'x'},
                'window': 500,
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
    },

    'case2': {
        'comments': 'Test acc, gyr, tps with complex models [LOFs, LOFs, SVMs].',

        'screens': ['Reacton', 'Memoria', 'Speedy'],

        'gesture_type': 'tap',

        'ExploreData': {
            'sns': {
                'min_nod_per_screen': 1,
                'min_nod_per_timestamp': 1,

                'min_nod_per_user': 3000,
                'max_nod_per_user': float('inf')

            },

            'ges': {
                'device_max_width': 600,
                'device_max_height': 1000,

                'min_nog_per_user': 300,
                'max_nog_per_user': float('inf')
            },
        },

        'CreateDataframes': {
            'sns': {
                'max_user_data': 15000
            }
        },

        'ExtractFeatures': {
            'sns': {
                'extraction_type': 'User',  # User, Timestamp, TimestampScreen, Screen
                'feature': {'acc': 'magnitude', 'gyr': 'x'},
                'window': 500,
                'overlap': 0.9
            },

            'ges': {
                'normalize': True
            }
        },

        'GetResults': {
            'acc': cases.case2.case_subclasses.AccClf,
            'gyr': cases.case2.case_subclasses.GyrClf,
            'ges': cases.case2.case_subclasses.GesClf,
            'ttl': cases.case2.case_subclasses.Ensemble,
        }
    },

    'case3': {
        'comments': 'Case 1 but with simple models [LOF, LOF, SVM].',

        'screens': ['Mathisis', 'Focus', 'Reacton'],

        'gesture_type': 'swipe',

        'ExploreData': {
            'sns': {
                'min_nod_per_screen': 1,
                'min_nod_per_timestamp': 1,

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
            },
        },

        'CreateDataframes': {
            'sns': {
                'max_user_data': 15000
            }
        },

        'ExtractFeatures': {
            'sns': {
                'extraction_type': 'User',  # User, Timestamp, TimestampScreen, Screen
                'feature': {'acc': 'magnitude', 'gyr': 'x'},
                'window': 500,
                'overlap': 0.9
            },

            'ges': {
                'normalize': True
            }
        },

        'GetResults': {
            'acc': cases.case3.case_subclasses.AccClf,
            'gyr': cases.case3.case_subclasses.GyrClf,
            'ges': cases.case3.case_subclasses.GesClf,
            'ttl': cases.case3.case_subclasses.Ensemble,
        }
    },

    'case4': {
        'comments': 'Case 1 but with simple models [SVM, SVM, SVM].',

        'screens': ['Mathisis', 'Focus', 'Reacton'],

        'gesture_type': 'swipe',

        'ExploreData': {
            'sns': {
                'min_nod_per_screen': 1,
                'min_nod_per_timestamp': 1,

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
            },
        },

        'CreateDataframes': {
            'sns': {
                'max_user_data': 15000
            }
        },

        'ExtractFeatures': {
            'sns': {
                'extraction_type': 'User',  # User, Timestamp, TimestampScreen, Screen
                'feature': {'acc': 'magnitude', 'gyr': 'x'},
                'window': 500,
                'overlap': 0.9
            },

            'ges': {
                'normalize': True
            }
        },

        'GetResults': {
            'acc': cases.case4.case_subclasses.AccClf,
            'gyr': cases.case4.case_subclasses.GyrClf,
            'ges': cases.case4.case_subclasses.GesClf,
            'ttl': cases.case4.case_subclasses.Ensemble,
        }
    },

    'case5': {
        'comments': 'Case 4 but window is 200.',

        'screens': ['Mathisis', 'Focus', 'Reacton'],

        'gesture_type': 'swipe',

        'ExploreData': {
            'sns': {
                'min_nod_per_screen': 1,
                'min_nod_per_timestamp': 1,

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
            },
        },

        'CreateDataframes': {
            'sns': {
                'max_user_data': 15000
            }
        },

        'ExtractFeatures': {
            'sns': {
                'extraction_type': 'User',  # User, Timestamp, TimestampScreen, Screen
                'feature': {'acc': 'magnitude', 'gyr': 'x'},
                'window': 200,
                'overlap': 0.9
            },

            'ges': {
                'normalize': True
            }
        },

        'GetResults': {
            'acc': cases.case5.case_subclasses.AccClf,
            'gyr': cases.case5.case_subclasses.GyrClf,
            'ges': cases.case5.case_subclasses.GesClf,
            'ttl': cases.case5.case_subclasses.Ensemble,
        }
    },

    'case6': {
        'comments': 'Case 5 but gyr uses magnitude.',
        'screens': ['Mathisis', 'Focus', 'Reacton'],

        'gesture_type': 'swipe',

        'ExploreData': {
            'sns': {
                'min_nod_per_screen': 1,
                'min_nod_per_timestamp': 1,

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
            },
        },

        'CreateDataframes': {
            'sns': {
                'max_user_data': 15000
            }
        },

        'ExtractFeatures': {
            'sns': {
                'extraction_type': 'User',  # User, Timestamp, TimestampScreen, Screen
                'feature': {'acc': 'magnitude', 'gyr': 'magnitude'},
                'window': 200,
                'overlap': 0.9
            },

            'ges': {
                'normalize': True
            }
        },

        'GetResults': {
            'acc': cases.case6.case_subclasses.AccClf,
            'gyr': cases.case6.case_subclasses.GyrClf,
            'ges': cases.case6.case_subclasses.GesClf,
            'ttl': cases.case6.case_subclasses.Ensemble,
        }
    }
}
