"""
This script was created at 20-Sep-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import numpy as np

from s4_GetResults_ClfSuperClass import ClfSuperClass


#  ============== #
#    Functions    #
# =============== #
def get_final_decisions(dec_acc: np.ndarray, dec_gyr: np.ndarray, dec_swp: np.ndarray) -> np.ndarray:

    min_size = min(dec_acc.shape[0], dec_gyr.shape[0], dec_swp.shape[0])
    final_decision = dec_acc[0:min_size] + dec_gyr[0:min_size] + dec_swp[0:min_size]

    return final_decision


#  ============ #
#    Classes    #
# ============= #
class Ensemble(ClfSuperClass):

    def __init__(self, original_user: str, initial_decisions: dict):

        data_type = 'ags'
        self.initial_decisions = initial_decisions

        super(Ensemble, self).__init__(original_user, data_type)

    def get_final_predictions(self) -> dict:

        for fold in range(self.folds):
            for user in self.initial_decisions['acc']:

                if user not in self.users_decisions:
                    self.users_decisions[user] = {}
                    self.users_predictions[user] = {}

                dec_acc = self.initial_decisions['acc'][user][fold]
                dec_gyr = self.initial_decisions['gyr'][user][fold]
                dec_swp = self.initial_decisions['swp'][user][fold]

                self.users_decisions[user][fold] = get_final_decisions(dec_acc, dec_gyr, dec_swp)

                predictions = np.empty(self.users_decisions[user][fold].shape[0])
                for idx in range(self.users_decisions[user][fold].shape[0]):
                    predictions[idx] = 1 if self.users_decisions[user][fold][idx] > 0 else -1
                self.users_predictions[user][fold] = predictions

        return self.users_predictions
