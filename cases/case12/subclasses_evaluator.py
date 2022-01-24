"""
This script was created at 18-Jan-22
author: eachrist

"""
# ============= #
#    Imports    #
# ============= #
import pandas as pd
from s4_GetResults_ClassEvaluator import Evaluator


# ============= #
#    Classes    #
# ============= #
class CaseEvaluator(Evaluator):

    def __init__(self):

        self.start_confidence = 60
        self.threshold = 35

        self.dict_conf = {

            'inlier': {'Mathisis': 40,
                       'Focus': 40,
                       'Speedy': 40,
                       'Reacton': 10,
                       'Memoria': 10},

            'outlier': {'Mathisis': -15,
                        'Focus': -8,
                        'Speedy': -15,
                        'Reacton': -15,
                        'Memoria': -15}
        }

        super(CaseEvaluator, self).__init__()

    def evaluate_original_user(self, screen: str, data: pd.DataFrame):

        FRR = None
        Num_Of_Unlocks = None
        FRRConf = None
        predictions = data['Prediction'].to_list()
        decisions = data['Decision'].to_list()
        if len(predictions) != 0:
            confidence = self.start_confidence
            false_rejections = 0
            Num_Of_Unlocks = 0
            for idx, sample in enumerate(predictions):
                if confidence < self.threshold:
                    confidence = self.start_confidence
                    Num_Of_Unlocks += 1
                tp = 'inlier'
                if sample != 1:
                    tp = 'outlier'
                    false_rejections += 1
                confidence += self.dict_conf[tp][screen] * abs(decisions[idx])
                if confidence > 100:
                    confidence = 100
            FRR = false_rejections / len(predictions)
            FRRConf = Num_Of_Unlocks / len(predictions)

        return FRR, Num_Of_Unlocks, FRRConf

    def evaluate_attackers(self, screen: str, data: pd.DataFrame):

        Mean_FAR = None
        Mean_Num_Of_Acceptances_Till_Lock = None
        if data.shape[0] != 0:
            Mean_FAR = 0
            Mean_Num_Of_Acceptances_Till_Lock = 0
            for user in set(data['User']):
                decisions = data.loc[data['User'] == user]['Decision'].to_list()
                predictions = data.loc[data['User'] == user]['Prediction'].to_list()
                confidence = self.start_confidence
                false_acceptances = 0
                Num_Of_Acceptances_Till_Lock = 0
                flag = True
                for idx, sample in enumerate(predictions):
                    if confidence >= self.threshold:
                        Num_Of_Acceptances_Till_Lock += 1
                    else:
                        flag = False
                    tp = 'outlier'
                    if sample == 1:
                        tp = 'inlier'
                        false_acceptances += 1
                    if flag:
                        confidence += self.dict_conf[tp][screen] * abs(decisions[idx])
                    if confidence > 100:
                        confidence = 100
                FAR = false_acceptances / len(predictions)
                Mean_FAR += FAR
                Mean_Num_Of_Acceptances_Till_Lock += Num_Of_Acceptances_Till_Lock
            Mean_FAR /= len(set(data['User']))
            Mean_Num_Of_Acceptances_Till_Lock /= len(set(data['User']))

        return Mean_FAR, Mean_Num_Of_Acceptances_Till_Lock

    def calculate_metrics(self, screen: str, original_user: str, sets_dict: dict):

        # Define dataframe with all data types shorted by user and stop time
        for sett in ['trn', 'tst', 'att']:
            all_data = pd.DataFrame()
            for data in sets_dict[sett]:
                # Short every data type by user and stop time
                data = data.sort_values(by=['User', 'StopTime']).reset_index(drop=True)
                data_to_append = data[['User', 'Module', 'StartTime', 'StopTime', 'Decision', 'Prediction']]
                all_data = all_data.append(data_to_append, ignore_index=True)
            # Short final dataframe
            all_data = all_data.sort_values(by=['User', 'StopTime']).reset_index(drop=True)
            sets_dict[sett].append(all_data)

        # Evaluate its module
        for idx, module in enumerate(['acc', 'gyr', 'swp', 'tap', 'all']):
            trn = sets_dict['trn'][idx][['Decision', 'Prediction']]
            tst = sets_dict['tst'][idx][['Decision', 'Prediction']]
            att = sets_dict['att'][idx][['User', 'Decision', 'Prediction']]
            self.OriginalUser.append(original_user)
            self.Module.append(module)
            self.NumOfTrnData.append(len(trn))
            self.NumOfTstData.append(len(tst))
            self.NumOfAttData.append(att.shape[0])
            self.NumOfAtt.append(len(set(att['User'])))
            FRR, NumOfUnlocks, FRRConf = self.evaluate_original_user(screen, trn)
            self.FRR_trn.append(FRR)
            self.FRRConf_trn.append(FRRConf)
            self.NumOfUnlocks_trn.append(NumOfUnlocks)
            FRR, NumOfUnlocks, FRRConf = self.evaluate_original_user(screen, tst)
            self.FRR_tst.append(FRR)
            self.FRRConf_tst.append(FRRConf)
            self.NumOfUnlocks_tst.append(NumOfUnlocks)
            FAR, NumOfAcceptTL = self.evaluate_attackers(screen, att)
            self.FAR.append(FAR)
            self.NumOfAcceptTL.append(NumOfAcceptTL)

        return
