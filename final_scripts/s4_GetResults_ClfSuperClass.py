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

    def __init__(self, original_user: str, data_type: str, users_data: dict):

        self.original_user = original_user
        self.data_type = data_type
        self.users_data = users_data

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
            for user in self.users_data:

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

        num_data = 0
        for user in self.users_data:
            if user != self.original_user:
                num_data += self.users_data[user].shape[0]
        num_data /= len(self.users_data) - 1

        metrics = {
            'Data_Type': self.data_type,

            'OrgUser': self.original_user,
            'OrgUser_NoD': self.users_data[self.original_user].shape[0],

            'Attacker_Mean_NoD': num_data,

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
