"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import pandas as pd


#  ============ #
#    Classes    #
# ============= #
class Evaluator:

    def __init__(self):

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
        self.NumOfAcceptS = []
        self.NumOfAcceptG = []

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
        df['NumOfAcceptS'] = self.NumOfAcceptS
        df['NumOfAcceptG'] = self.NumOfAcceptG

        return df
