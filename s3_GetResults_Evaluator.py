"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import pandas as pd
from statistics import mean

#  =============== #
#    Parameters    #
# ================ #
start_threshold = 35
start_confidence = 60
dict_conf = {
    'inlier': {
        'Mathisis': 40,
        'Focus': 40,
        'Speedy': 40,
        'Reacton': 10,
        'Memoria': 10
    },
    'outlier': {
        'Mathisis': -15,
        'Focus': -8,
        'Speedy': -15,
        'Reacton': -15,
        'Memoria': -15
    }
}


#  ============== #
#    Functions    #
# =============== #
def evaluate_original_user(predictions: list, screen: str):

    FRR = None
    Num_Of_Unlocks = None
    FRRConf = None

    if len(predictions) != 0:
        threshold = start_threshold
        confidence = start_confidence
        false_rejections = 0
        Num_Of_Unlocks = 0
        for sample in predictions:
            if confidence < threshold:
                confidence = start_confidence
                Num_Of_Unlocks += 1
            if sample != 1:
                confidence += dict_conf['inlier'][screen]
            else:
                confidence += dict_conf['outlier'][screen]
                false_rejections += 1
            if confidence > 100:
                confidence = 100
        FRR = false_rejections / len(predictions)
        FRRConf = Num_Of_Unlocks / len(predictions)

    return FRR, Num_Of_Unlocks, FRRConf


def evaluate_attackers(data: pd.DataFrame, screen: str):

    Mean_FAR = None
    Mean_Num_Of_Acceptances_Till_Lock = None
    if data.shape[0] != 0:
        Mean_FAR = 0
        Mean_Num_Of_Acceptances_Till_Lock = 0
        for user in set(data['User']):
            predictions = data.loc[data['User'] == user]['Prediction'].to_list()
            threshold = start_threshold
            confidence = start_confidence
            false_acceptances = 0
            Num_Of_Acceptances_Till_Lock = 0
            flag = True
            for sample in predictions:
                if confidence >= threshold:
                    Num_Of_Acceptances_Till_Lock += 1
                else:
                    flag = False
                if sample == 1:
                    if flag:
                        confidence += dict_conf['inlier'][screen]
                    false_acceptances += 1
                else:
                    if flag:
                        confidence += dict_conf['outlier'][screen]
                if confidence > 100:
                    confidence = 100
            FAR = false_acceptances / len(predictions)
            Mean_FAR += FAR
            Mean_Num_Of_Acceptances_Till_Lock += Num_Of_Acceptances_Till_Lock
        Mean_FAR /= len(set(data['User']))
        Mean_Num_Of_Acceptances_Till_Lock /= len(set(data['User']))

    return Mean_FAR, Mean_Num_Of_Acceptances_Till_Lock


def find_groups(data: pd.DataFrame):

    group = 0
    groups = [group]
    stop_time = data.iloc[0]['StopTime']
    temp_sns_sample = data.loc[data['Type'] == 'acc'].iloc[0]
    window_time = temp_sns_sample['StopTime'] - temp_sns_sample['StartTime']

    for index, sample in data[1:].iterrows():
        if sample['StartTime'] > stop_time:
            group += 1
            if sample['Type'] == 'swipe' or sample['Type'] == 'tap':
                stop_time = sample['StartTime'] + window_time
        groups.append(group)
        if sample['Type'] == 'acc' or sample['Type'] == 'gyr':
            stop_time = sample['StopTime']

    return groups


def groups_predictions(data: pd.DataFrame):

    predictions = []
    for group in set(data['Group']):
        group_data = data.loc[data['Group'] == group]['Decision'].to_list()
        group_decision = mean(group_data)
        group_prediction = 1 if group_decision > 0 else -1
        predictions.append(group_prediction)

    return predictions


def get_final_evaluation_metrics(list_of_data: list):

    # Append and sort all data
    all_data = pd.DataFrame()
    for data in list_of_data:
        data_to_append = data[['User', 'Type', 'StartTime', 'StopTime', 'Decision']]
        all_data = all_data.append(data_to_append, ignore_index=True)

    metrics = {
        'number_of_users': len(set(all_data['User'])),
        'number_of_data': 0,
        'pos_ones_percentage': 0,
        'neg_ones_percentage': 0
    }
    for user in set(all_data['User']):
        all_user_data = all_data.loc[all_data['User'] == user].sort_values(by=['StartTime']).reset_index(drop=True)
        all_user_data['Group'] = find_groups(all_user_data)
        predictions = groups_predictions(all_user_data)
        metrics['number_of_data'] += len(predictions)
        metrics['pos_ones_percentage'] += len([x for x in predictions if x == 1]) / len(predictions)
        metrics['neg_ones_percentage'] += len([x for x in predictions if x == -1]) / len(predictions)
    # metrics['number_of_data'] /= len(set(all_data['User']))
    metrics['pos_ones_percentage'] /= len(set(all_data['User']))
    metrics['neg_ones_percentage'] /= len(set(all_data['User']))

    return metrics


#  ============ #
#    Classes    #
# ============= #
class Evaluator:

    def __init__(self, screen: str):

        self.screen = screen
        self.OriginalUser = []
        self.Module = []
        self.NumOfTrnData = []
        self.NumOfTstData = []
        self.NumOfAttData = []
        self.NumOfAtt = []
        self.FRR_trn = []
        self.FRRConf_trn = []
        self.NumOfUnlocks_trn = []
        self.FRR_tst = []
        self.FRRConf_tst = []
        self.NumOfUnlocks_tst = []
        self.FAR = []
        self.NumOfAcceptTL = []

    def calculate_metrics(self, original_user: str, sets_dict: dict):

        # Its module separately
        for idx, data_type in enumerate(['acc', 'gyr', 'swp', 'tap']):
            trn = sets_dict['trn'][idx]['Prediction'].to_list()
            tst = sets_dict['tst'][idx]['Prediction'].to_list()
            att = sets_dict['att'][idx][['User', 'Prediction']]
            self.OriginalUser.append(original_user)
            self.Module.append(data_type)
            self.NumOfTrnData.append(len(trn))
            self.NumOfTstData.append(len(tst))
            self.NumOfAttData.append(att.shape[0])
            self.NumOfAtt.append(len(set(att['User'])))
            FRR, NumOfUnlocks, FRRConf = evaluate_original_user(trn, self.screen)
            self.FRR_trn.append(FRR)
            self.FRRConf_trn.append(FRRConf)
            self.NumOfUnlocks_trn.append(NumOfUnlocks)
            FRR, NumOfUnlocks, FRRConf = evaluate_original_user(tst, self.screen)
            self.FRR_tst.append(FRR)
            self.FRRConf_tst.append(FRRConf)
            self.NumOfUnlocks_tst.append(NumOfUnlocks)
            FAR, NumOfAcceptTL = evaluate_attackers(att, self.screen)
            self.FAR.append(FAR)
            self.NumOfAcceptTL.append(NumOfAcceptTL)

        # Combine Modules
        self.OriginalUser.append(original_user)
        self.Module.append('fnl')
        metrics = get_final_evaluation_metrics(sets_dict['trn'])
        self.NumOfTrnData.append(metrics['number_of_data'])
        self.FRR_trn.append(metrics['neg_ones_percentage'])
        self.FRRConf_trn.append(None)
        self.NumOfUnlocks_trn.append(None)
        metrics = get_final_evaluation_metrics(sets_dict['tst'])
        self.NumOfTstData.append(metrics['number_of_data'])
        self.FRR_tst.append(metrics['neg_ones_percentage'])
        self.FRRConf_tst.append(None)
        self.NumOfUnlocks_tst.append(None)
        metrics = get_final_evaluation_metrics(sets_dict['att'])
        self.NumOfAtt.append(metrics['number_of_users'])
        self.NumOfAttData.append(metrics['number_of_data'])
        self.FAR.append(metrics['pos_ones_percentage'])
        self.NumOfAcceptTL.append(None)

        return

    def create_dataframe(self):

        df = pd.DataFrame()
        df['OriginalUser'] = self.OriginalUser
        df['Module'] = self.Module
        df['NumOfTrnData'] = self.NumOfTrnData
        df['NumOfTstData'] = self.NumOfTstData
        df['NumOfAttData'] = self.NumOfAttData
        df['NumOfAtt'] = self.NumOfAtt
        df['FRR_trn'] = self.FRR_trn
        df['FRRConf_trn'] = self.FRRConf_trn
        df['NumOfUnlocks_trn'] = self.NumOfUnlocks_trn
        df['FRR_tst'] = self.FRR_tst
        df['FRRConf_tst'] = self.FRRConf_tst
        df['NumOfUnlocks_tst'] = self.NumOfUnlocks_tst
        df['FAR'] = self.FAR
        df['NumOfAcceptTL'] = self.NumOfAcceptTL

        return df
