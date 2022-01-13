"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import pandas as pd

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
def evaluate_original_user(data: pd.DataFrame, screen: str):

    FRR = None
    Num_Of_Unlocks = None
    FRRConf = None

    predictions = data['Prediction'].to_list()
    if len(predictions) != 0:
        threshold = start_threshold
        confidence = start_confidence
        false_rejections = 0
        Num_Of_Unlocks = 0
        for sample in predictions:
            if confidence < threshold:
                confidence = start_confidence
                Num_Of_Unlocks += 1
            tp = 'inlier'
            if sample != 1:
                tp = 'outlier'
                false_rejections += 1
            confidence += dict_conf[tp][screen]
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
                tp = 'outlier'
                if sample == 1:
                    tp = 'inlier'
                    false_acceptances += 1
                if flag:
                    confidence += dict_conf[tp][screen]
                if confidence > 100:
                    confidence = 100
            FAR = false_acceptances / len(predictions)
            Mean_FAR += FAR
            Mean_Num_Of_Acceptances_Till_Lock += Num_Of_Acceptances_Till_Lock
        Mean_FAR /= len(set(data['User']))
        Mean_Num_Of_Acceptances_Till_Lock /= len(set(data['User']))

    return Mean_FAR, Mean_Num_Of_Acceptances_Till_Lock


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

        # Define dataframe with all data types shorted by user and stop time
        for sett in ['trn', 'tst', 'att']:
            all_data = pd.DataFrame()
            for data in sets_dict[sett]:
                # Short every data type by user and stop time
                data = data.sort_values(by=['User', 'StopTime']).reset_index(drop=True)
                data_to_append = data[['User', 'Type', 'StartTime', 'StopTime', 'Decision', 'Prediction']]
                all_data = all_data.append(data_to_append, ignore_index=True)
            # Short final dataframe
            all_data = all_data.sort_values(by=['User', 'StopTime']).reset_index(drop=True)
            sets_dict[sett].append(all_data)

        # Evaluate its module
        for idx, data_type in enumerate(['acc', 'gyr', 'swp', 'tap', 'all']):
            trn = sets_dict['trn'][idx][['Decision', 'Prediction']]
            tst = sets_dict['tst'][idx][['Decision', 'Prediction']]
            att = sets_dict['att'][idx][['User', 'Decision', 'Prediction']]
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
