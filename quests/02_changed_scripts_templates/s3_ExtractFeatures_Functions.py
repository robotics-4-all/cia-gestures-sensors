"""
This script was created at 09-Dec-21
author: eachrist
"""

"""

def extract_features_sns(case: str, screen_path: str, data: pd.DataFrame, module: str, window, overlap):

    print(' - Extracting ' + module + ' features.')
    path_df = os.path.join(screen_path, 'ftr_' + module[0:3] + '_' + str(window) + '_' + str(overlap) + '.csv')

    if not os.path.exists(path_df):

        features = dict_cases[case]['FeatureExtraction']['sns']['lvl0_ftr'][module[0:3]]
        sample_rate = dict_cases[case]['FeatureExtraction']['sns']['sample_rate']
        # window = dict_cases[case]['FeatureExtraction']['sns']['window']
        # overlap = dict_cases[case]['FeatureExtraction']['sns']['overlap']

        features_objects = {}
        for feature in features:
            features_objects[feature] = FeaturesSns()

        for user in tqdm(list(set(data['user']))):
            user_data = data.loc[data['user'] == user]
            timestamps = list(set(user_data['timestamp']))
            timestamps.sort()
            for idx, ts in enumerate(timestamps):
                for feature in features:
                    data_to_window = user_data.loc[data['timestamp'] == ts][feature].to_numpy()
                    features_objects[feature] = calculate_features_sns(user, module[0:3], data_to_window, idx, ts,
                                                                       features_objects[feature],
                                                                       window, overlap, sample_rate)

        df_features = features_objects[features[0]].create_dataframe(features[0], True)
        if len(features) > 1:
            for feature in features[1:]:
                df_temp = features_objects[feature].create_dataframe(feature, False)
                df_features = pd.concat([df_features, df_temp], axis=1)
        df_features.to_csv(path_df, index=False)
        print('     ' + module + ' features dataframe saved at: ', path_df)

    else:

        df_features = pd.read_csv(path_df)
        print('     ' + module + ' features dataframe loaded from: ', path_df)

    print('')

    return df_features

"""
