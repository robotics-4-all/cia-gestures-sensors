"""
This script was created at 20-Sep-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import pandas as pd


#  ================= #
#    Dictionaries    #
# ================== #
dict_conf = {
    'inlier': {
        'Mathisis': 40,
        'Focus': 40,
        'Speedy': 40,
        'Reaction': 10,
        'Memoria': 10
    },
    'outlier': {
        'Mathisis': -15,
        'Focus': -8,
        'Speedy': -15,
        'Reaction': -15,
        'Memoria': -15
    }
}


#  ============ #
#    Classes    #
# ============= #
class ClfSuperClass:

    def __init__(self, folds: int, original_user: str, module: str):

        self.original_user = original_user
        self.module = module

        self.folds = folds

        self.users_decisions = {}
        self.users_predictions = {}

    def calculate_metrics(self, screen: str) -> pd.DataFrame:

        metrics = pd.DataFrame()

        for fold in range(self.folds):

            Mean_Num_Of_Att_Data = 0

            for user in self.users_decisions:

                predictions = self.users_predictions[user][fold]
                threshold = 35
                confidence = 60

                if user == self.original_user:

                    false_rejections = 0
                    Num_Of_Unlocks = 0
                    for sample in predictions:

                        if confidence < threshold:
                            confidence = 60
                            Num_Of_Unlocks += 1

                        if sample != 1:
                            confidence += dict_conf['inlier'][screen]
                        else:
                            confidence += dict_conf['outlier'][screen]
                            false_rejections += 1

                        if confidence > 100:
                            confidence = 100

                    Num_Of_OrgUser_Data = predictions.shape[0]
                    FRR = false_rejections / Num_Of_OrgUser_Data
                    FRR_Conf = Num_Of_Unlocks / Num_Of_OrgUser_Data

                else:

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

                    Mean_Num_Of_Att_Data += predictions.shape[0]
                    FAR = false_acceptances / predictions.shape[0]

            Mean_Num_Of_Att_Data /= len(self.users_decisions.keys()) - 1

            metrics_row = {
                'OriginalUser': self.original_user,
                'Fold': 'f' + str(fold),

                'Module': self.module,
                'NumOfOrgUserTstData': Num_Of_OrgUser_Data,
                'MeanNumOfAttData': Mean_Num_Of_Att_Data,

                'FRR': FRR,
                'FAR': FAR,
                'NumOfUnlocks': Num_Of_Unlocks,
                'FRR_Conf': FRR_Conf,
                'NumOfAcceptTL': Num_Of_Acceptances_Till_Lock
            }

            metrics = metrics.append(metrics_row, ignore_index=True)

        return metrics
