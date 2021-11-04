"""
This script was created at 20-Sep-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import numpy as np


#  ============ #
#    Classes    #
# ============= #
class ClfSuperClass:

    def __init__(self, original_user: str, data_type: str):

        self.original_user = original_user
        self.data_type = data_type

        self.folds = 10

        self.users_decisions = {}
        self.users_predictions = {}

    def calculate_metrics(self) -> dict:

        FRR = []
        Number_Of_Unlocks = []
        FRR_Conf = []
        FAR = []
        Number_Of_Acceptances_Till_Lock = []

        for fold in range(self.folds):
            for user in self.users_decisions:

                predictions = self.users_predictions[user][fold]
                threshold = 35
                confidence = 60

                if user == self.original_user:

                    false_rejections = 0
                    number_of_unlocks = 0
                    for sample in predictions:

                        if confidence < threshold:
                            confidence = 60
                            number_of_unlocks += 1

                        if sample == 1:
                            confidence += 5
                        else:
                            confidence -= 15
                            false_rejections += 1

                        if confidence > 100:
                            confidence = 100

                    frr = false_rejections / predictions.shape[0]
                    frr_conf = number_of_unlocks / predictions.shape[0]

                    FRR.append(frr)
                    Number_Of_Unlocks.append(number_of_unlocks)
                    FRR_Conf.append(frr_conf)

                else:

                    false_acceptances = 0
                    number_of_acceptances_till_lock = 0
                    flag = True
                    for sample in predictions:

                        if confidence >= threshold:
                            number_of_acceptances_till_lock += 1
                        else:
                            flag = False

                        if sample == 1:
                            if flag:
                                confidence += 5
                            false_acceptances += 1
                        else:
                            if flag:
                                confidence -= 15

                        if confidence > 100:
                            confidence = 100

                    far = false_acceptances / predictions.shape[0]

                    FAR.append(far)
                    Number_Of_Acceptances_Till_Lock.append(number_of_acceptances_till_lock)

        FRR = np.array(FRR)
        Number_Of_Unlocks = np.array(Number_Of_Unlocks)
        FRR_Conf = np.array(FRR_Conf)
        FAR = np.array(FAR)
        Number_Of_Acceptances_Till_Lock = np.array(Number_Of_Acceptances_Till_Lock)

        num_data_orgu = 0
        for fold in self.users_decisions[self.original_user]:
            num_data_orgu += self.users_decisions[self.original_user][fold].shape[0]

        mean_num_data_att = 0
        for user in self.users_decisions:
            if user != self.original_user:
                for fold in self.users_decisions[user]:
                    mean_num_data_att += self.users_decisions[user][fold].shape[0]
        mean_num_data_att /= len(self.users_decisions.keys()) - 1

        metrics = {
            'Data_Type': self.data_type,

            'OrgUser': self.original_user,
            'OrgUser_NoD': num_data_orgu,

            'Attacker_Mean_NoD': mean_num_data_att,

            'FRR_min': FRR.min(),
            'FRR_max': FRR.max(),
            'FRR_std': FRR.std(),
            'FRR_mean': FRR.mean(),

            'NU_min': Number_Of_Unlocks.min(),
            'NU_max': Number_Of_Unlocks.max(),
            'NU_std': Number_Of_Unlocks.std(),
            'NU_mean': Number_Of_Unlocks.mean(),

            'FRR_Conf_min': FRR_Conf.min(),
            'FRR_Conf_max': FRR_Conf.max(),
            'FRR_Conf_std': FRR_Conf.std(),
            'FRR_Conf_mean': FRR_Conf.mean(),

            'FAR_min': FAR.min(),
            'FAR_max': FAR.max(),
            'FAR_std': FAR.std(),
            'FAR_mean': FAR.mean(),

            'NATL_min': Number_Of_Acceptances_Till_Lock.min(),
            'NATL_max': Number_Of_Acceptances_Till_Lock.max(),
            'NATL_std': Number_Of_Acceptances_Till_Lock.std(),
            'NATL_mean': Number_Of_Acceptances_Till_Lock.mean(),
        }

        return metrics
