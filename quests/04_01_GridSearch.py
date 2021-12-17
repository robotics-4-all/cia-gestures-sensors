# Imports
import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn import svm
from statistics import mean
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler, StandardScaler

'''
Results:

case1 exp1:
nu [0.3, 0.5]
gamma [0.00005, 0.1]

case1 exp2:
nu [0.3, 0.5, 0.02]
gamma [0.0005, 0.1, 0.005]
'''

# Parameters
case = 'case11'
exp = '01'

final_features = {
    'acc': ['Mean', 'STD', 'Max', 'Min', 'Percentile25', 'Percentile50', 'Percentile75',
            'Kurtosis', 'Skewness', 'Amplitude2', 'Frequency2'],

    'gyr': ['Mean', 'STD', 'Max', 'Min', 'Percentile25', 'Percentile50', 'Percentile75',
            'Kurtosis', 'Skewness', 'Amplitude2', 'Frequency2'],

    # 'ges': ['Duration', 'MeanX', 'MeanY', 'StartStopLength', 'ScreenPercentage',
    #                       'TraceProjection', 'StartVelocity', 'StopVelocity',
    #                       'AccelerationHor', 'AccelerationVer', 'Slope', 'MeanSquareError', 'CoefDetermination'],

    'ges': ['Duration'],  # taps
}

folds = 5
scalar = StandardScaler

nus = [0.01, 0.1, 0.3, 0.5, 0.8]
gammas = [5e-05, 0.001, 0.01, 0.1, 1, 10]
# nus = [0.3, 0.35, 0.4, 0.45, 0.5]
# gammas = [0.00001, 0.0005, 0.001, 0.05, 0.1]

# Thread
results = {
    'nus': nus,
    'gammas': gammas
}

for screen in ['Reacton', 'Memoria', 'Speedy']:
    # for screen in ['Focus', 'Mathisis', 'Reacton']:
    results[screen] = {}

    for data_type in ['ges']:
        # for data_type in ['acc', 'gyr', 'ges']:
        grid_results_FRR = np.zeros((len(nus), len(gammas)))
        grid_results_FAR = np.zeros((len(nus), len(gammas)))

        # Load data
        data_path = os.path.join('cases', case, screen, 'features_' + data_type + '.csv')
        data = pd.read_csv(data_path)

        users = list(set(data['User']))
        for org_user in tqdm(users):
            grid_results_FRR_per_user = np.zeros((len(nus), len(gammas)))
            grid_results_FAR_per_user = np.zeros((len(nus), len(gammas)))

            x = data.loc[data['User'] == org_user][final_features[data_type]]
            x = x.reset_index(drop=True)

            kf = KFold(n_splits=folds, shuffle=True, random_state=2)
            for fold, [trn_indexes, tst_indexes] in enumerate(kf.split(x)):

                # Select train and test set for original user
                x_trn_org, x_tst_org = x.iloc[trn_indexes], x.iloc[tst_indexes]
                x_trn_org, x_tst_org = x_trn_org.to_numpy(), x_tst_org.to_numpy()

                # Scale data
                if scalar != None:
                    scalar_obj = scalar().fit(x_trn_org)
                    x_trn_org = scalar_obj.transform(x_trn_org)

                for row, nu in enumerate(nus):
                    for col, gamma in enumerate(gammas):

                        # Train model
                        clf = svm.OneClassSVM(gamma=gamma, kernel='rbf', nu=nu)
                        clf.fit(x_trn_org)
                        distances = clf.decision_function(x_trn_org)
                        max_distance = max(distances)

                        FAR_per_att = []
                        for user in users:

                            if user == org_user:
                                x_tst = x_tst_org
                            else:
                                x_tst = data.loc[data['User'] == user][final_features[data_type]]
                                x_tst = x_tst.reset_index(drop=True)

                            if scalar != None:
                                x_tst = scalar_obj.transform(x_tst)

                            # Get predictions
                            decisions = clf.decision_function(x_tst) / max_distance
                            predictions = np.empty(x_tst.shape[0])
                            for sample_idx in range(x_tst.shape[0]):
                                predictions[sample_idx] = 1 if decisions[sample_idx] > 0 else -1

                            # Calculate metrics
                            if user == org_user:
                                false_rejections = 0
                                for sample in predictions:
                                    if sample != 1:
                                        false_rejections += 1
                                grid_results_FRR_per_user[row, col] = false_rejections / predictions.shape[0]

                            else:
                                false_acceptances = 0
                                for sample in predictions:
                                    if sample == 1:
                                        false_acceptances += 1
                                FAR_per_att.append(false_acceptances / predictions.shape[0])

                        grid_results_FAR_per_user[row, col] = mean(FAR_per_att)

            grid_results_FRR_per_user /= folds
            grid_results_FAR_per_user /= folds

            grid_results_FRR += grid_results_FRR_per_user
            grid_results_FAR += grid_results_FAR_per_user

        grid_results_FRR /= len(users)
        grid_results_FAR /= len(users)

        results[screen][data_type] = {
            'FRR': grid_results_FRR.tolist(),
            'FAR': grid_results_FAR.tolist()
        }

path_save = os.path.join(os.path.dirname(__file__), '04_01_GridSearch_results_' + case + '_' + exp + '.json')

with open(path_save, 'w') as fp:
    json.dump(results, fp)
print(' results dict saved in: ', path_save)
