"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Lab Group

Author : Christos Emmanouil
"""
# ============= #
#    Imports    #
# ============= #
import numpy as np
import pandas as pd
from random import randint


# =============== #
#    Functions    #
# =============== #
def SplitDFF_OrgAtt(DFF, Original_User):
    """
    Split feature dataframes in original user & attackers.

    :param DFF: A dataframe of features, must have the 'Output' column
    :param Original_User: Original user name
    :return: A dataframe with the original user data, a dataframe with the attackers data
    """

    DFF_Original = pd.DataFrame()
    DFF_Attackers = pd.DataFrame()
    for i in range(len(DFF)):
        row = DFF.loc[i]
        if row['User'] == Original_User:
            DFF_Original = DFF_Original.append(row, ignore_index=True)
        else:
            DFF_Attackers = DFF_Attackers.append(row, ignore_index=True)
    DFF_Original['Output'] = 1
    DFF_Attackers['Output'] = -1

    return DFF_Original, DFF_Attackers


def SplitRandom(DFF, Split_Rate):
    """
    Split dataframe in train & test set in a random way.

    :param DFF: A dataframe
    :param Split_Rate: The percentage of entries that the test set must contain
    :return: The train and the test dataframes
    """

    Trn = DFF
    Tst = pd.DataFrame()
    Num_Test_Data = int(np.floor(len(Trn) * Split_Rate))
    for i in range(Num_Test_Data):
        rnd = randint(0, len(Trn) - 1)
        row = Trn.loc[rnd]
        Tst = Tst.append(row, ignore_index=True)
        Trn = Trn.drop(rnd)
        Trn = Trn.reset_index(drop=True)

    return Trn, Tst


def SplitRandom_Synced(FDF_1, FDF_2, Split_Rate):
    """
    Split 2 dataframes in the same random way in train & test sets

    :param FDF_1: A dataframe
    :param FDF_2: A dataframe, with the same size as the FDF_1
    :param Split_Rate: The percentage of entries that the test set must contain
    :return: The train and the test dataframes
    """

    Trn_1 = FDF_1
    Tst_1 = pd.DataFrame()
    Trn_2 = FDF_2
    Tst_2 = pd.DataFrame()
    Num_Test_Data = int(np.floor(len(Trn_1) * Split_Rate))
    for i in range(Num_Test_Data):
        rnd = randint(0, len(Trn_1) - 1)
        row_1 = Trn_1.loc[rnd]
        row_2 = Trn_2.loc[rnd]
        Tst_1 = Tst_1.append(row_1, ignore_index=True)
        Tst_2 = Tst_2.append(row_2, ignore_index=True)
        Trn_1 = Trn_1.drop(rnd)
        Trn_2 = Trn_2.drop(rnd)
        Trn_1 = Trn_1.reset_index(drop=True)
        Trn_2 = Trn_2.reset_index(drop=True)

    return Trn_1, Tst_1, Trn_2, Tst_2
