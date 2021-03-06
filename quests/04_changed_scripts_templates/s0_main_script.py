"""
This script was created at 09-Dec-21
author: eachrist

"""
"""

def main_thread(case: str, screen: str):

    print('---', screen, '---\n')
    screen_path = check_paths(case_path, screen)

    # Explore data
    print('-> ExploreData\n')
    dict_acc = explore_sns_data(case, screen, screen_path, 'accelerometer')
    dict_gyr = explore_sns_data(case, screen, screen_path, 'gyroscope')
    dict_ges = explore_ges_data(case, screen, screen_path)
    dict_acc_fnl, dict_gyr_fnl, dict_ges_fnl = select_users(case, screen_path, dict_acc, dict_gyr, dict_ges)
    print('  ---\n')

    # Create dataframes
    print('-> CreateDataframes\n')
    df_acc = create_df_sns(case, screen_path, dict_acc_fnl, 'accelerometer')
    df_gyr = create_df_sns(case, screen_path, dict_gyr_fnl, 'gyroscope')
    df_ges = create_df_ges(case, screen_path, dict_ges_fnl)
    print('  ---\n')

    # Extract Features
    print('-> ExtractingFeatures\n')
    ftr_acc = extract_features_sns(case, screen_path, df_acc, 'accelerometer')
    ftr_gyr = extract_features_sns(case, screen_path, df_gyr, 'gyroscope')
    ftr_ges = extract_features_ges(case, screen_path, df_ges)
    print('  ---\n')

    all_results = pd.DataFrame()
    for nu in dict_cases[case]['GetResults']['Classifiers']['nus']:
        for gamma in dict_cases[case]['GetResults']['Classifiers']['gammas']:

            # Get Results
            print('-> GettingResults\n')
            results = get_results(case, screen, screen_path, ftr_acc, ftr_gyr, ftr_ges, nu, gamma)
            print('  ---\n')

            results['Nu'] = nu
            results['Gamma'] = gamma
            all_results = all_results.append(results, ignore_index=True)

    all_results.to_csv(os.path.join(screen_path, 'results.csv'), index=False)

    return

"""
