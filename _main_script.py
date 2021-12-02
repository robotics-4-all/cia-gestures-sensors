"""
This script was created at 13-Sep-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os

from _cases_dictionaries import dict_cases
from s0_Helpers_Functions import check_paths
from s1_ExploreData_Functions import explore_sns_data, explore_ges_data, select_users
from s2_CreateDataframes_Functions import create_df_sns, create_df_ges
from s3_ExtractFeatures_Functions import extract_features_df_sns, extract_features_df_ges
from s4_GetResults_Functions import get_results
from s5_VisualizeResults_Functions import visualize_results


# =============== #
#    Functions    #
# =============== #
def main_thread(case_name: str, screen_name: str):

    print('---', screen_name, '---\n')
    screen_path = check_paths(case_path, screen_name)

    # Explore data
    print('-> ExploreData\n')
    dict_acc = explore_sns_data(case_name, screen_path, screen_name, 'accelerometer')
    dict_gyr = explore_sns_data(case_name, screen_path, screen_name, 'gyroscope')
    dict_ges = explore_ges_data(case_name, screen_path, screen_name)
    dict_acc_fnl, dict_gyr_fnl, dict_ges_fnl = select_users(case_name, screen_path, dict_acc, dict_gyr, dict_ges)
    print('  ---\n')

    # Create dataframes
    print('-> CreateDataframes\n')
    df_acc = create_df_sns(case_name, screen_path, dict_acc_fnl, 'accelerometer')
    df_gyr = create_df_sns(case_name, screen_path, dict_gyr_fnl, 'gyroscope')
    df_ges = create_df_ges(case_name, screen_path, dict_ges_fnl)
    print('  ---\n')

    # Extract features
    print('-> ExtractFeatures\n')
    ftr_acc = extract_features_df_sns(case_name, screen_path, df_acc, 'accelerometer')
    ftr_gyr = extract_features_df_sns(case_name, screen_path, df_gyr, 'gyroscope')
    ftr_ges = extract_features_df_ges(case_name, screen_path, df_ges)
    print('  ---\n')

    print('-> GettingResults\n')
    results = get_results(case_name, screen_name, screen_path, ftr_acc, ftr_gyr, ftr_ges)
    print('  ---\n')

    print('-> VisualizeResults\n')
    visualize_results(screen_path, results)
    print('  ---\n')

    return


# ========== #
#    main    #
# ========== #
if __name__ == "__main__":

    # Select case
    case_name = 'case7'
    case_path = check_paths(os.path.dirname(__file__), os.path.join('cases', case_name))

    print('=====')
    print(case_name)
    print('=====')

    # Select screen
    for screen_name in dict_cases[case_name]['screens']:
        main_thread(case_name, screen_name)
        input('Press Enter to continue...\n')
