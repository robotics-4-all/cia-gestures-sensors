"""
This script was created at 09-Dec-21
author: eachrist

"""
"""

def get_results(case: str, screen: str, screen_path: str,
                df_acc: pd.DataFrame, df_gyr: pd.DataFrame, df_ges: pd.DataFrame,
                num_of_clf_that_decide) -> pd.DataFrame:

    print(' - Getting results.')
    path_df = os.path.join(screen_path, 'results_' + str(num_of_clf_that_decide) + '.csv')

    # Define parameters
    split_rate = dict_cases[case]['GetResults']['split_rate']

    # Define evaluator
    eval_obj = dict_cases[case]['GetResults']['Evaluator']()

    # Select original user
    for original_user in tqdm(set(df_acc['User'])):

        # Split data to trn, tst, att
        acc_trn, acc_tst, acc_att = split_df_sns(original_user, df_acc, split_rate)
        gyr_trn, gyr_tst, gyr_att = split_df_sns(original_user, df_gyr, split_rate)
        ges_trn, ges_tst, ges_att = split_df_ges(original_user, df_ges, split_rate)

        # Separate swipes & taps
        swp_trn = ges_trn.loc[ges_trn['Module'] == 'swp'].reset_index(drop=True)
        tap_trn = ges_trn.loc[ges_trn['Module'] == 'tap'].reset_index(drop=True)
        swp_tst = ges_tst.loc[ges_tst['Module'] == 'swp'].reset_index(drop=True)
        tap_tst = ges_tst.loc[ges_tst['Module'] == 'tap'].reset_index(drop=True)
        swp_att = ges_att.loc[ges_att['Module'] == 'swp'].reset_index(drop=True)
        tap_att = ges_att.loc[ges_att['Module'] == 'tap'].reset_index(drop=True)

        # Concentrate data
        sets_dict = {
            'trn': [acc_trn, gyr_trn, swp_trn, tap_trn],
            'tst': [acc_tst, gyr_tst, swp_tst, tap_tst],
            'att': [acc_att, gyr_att, swp_att, tap_att]
        }

        # Define Classifiers
        classifiers = []
        for data_type in ['acc', 'gyr', 'swp', 'tap']:
            # lvl0_ftr = None
            # if data_type in ['acc', 'gyr']:
            #     lvl0_ftr = dict_cases[case]['FeatureExtraction']['sns']['lvl0_ftr'][data_type]
            # classifiers.append(dict_cases[case]['GetResults']['Classifiers'][data_type](lvl0_ftr))
            classifiers.append(dict_cases[case]['GetResults']['Classifiers'][data_type](num_of_clf_that_decide))

        # Train Classifiers
        for idx, clf in enumerate(classifiers):
            clf.train_classifiers(sets_dict['trn'][idx])

        # Get prediction for training, testing and attackers data
        for sett in sets_dict:
            for idx, clf in enumerate(classifiers):
                sets_dict[sett][idx]['Decision'] = clf.get_decisions(sets_dict[sett][idx])
                sets_dict[sett][idx]['Prediction'] = get_predictions(sets_dict[sett][idx]['Decision'])

        # Evaluate predictions of every module separately
        eval_obj.calculate_metrics(screen, original_user, sets_dict)

    # Create dataframe with the results of separated modules
    results = eval_obj.create_dataframe()

    # Save results
    # results.to_csv(path_df, index=False)
    print('     Results saved at: ', path_df)
    print('')

    return results
    
"""
