"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Lab Group

Author : Christos Emmanouil
"""


class EvaluationMetrics:

    OrgTrnSize = []  # Number of samples of original user used for training
    OrgTstSize = []  # Number of samples of original user used for testing
    AttNum = []  # Number of attackers
    Att_TotalSize = []  # Total number of attackers samples
    Att_AvgSize = []  # Average number of the samples number per attacker
    FRR = []  # False rejection rate in original user's testing samples
    FRR_Conf = []  # False rejection rate calculated from the num_of_unlocks
    FAR_Total = []  # False acceptance rate in the total of attackers samples
    FAR_Avg = []  # Average of false acceptance rate of its attacker's samples
    Num_Of_Unlocks = []  # Number of unlocks an original user forced to do in a system with confidence levels
    Num_Of_Accepted_Avg = []  # Average number of the successful attempts its attacker made until locked
    OrgTrnSize_Std = []
    OrgTstSize_Std = []
    AttNum_Std = []
    Att_TotalSize_Std = []
    Att_AvgSize_Std = []
    FRR_Std = []
    FRR_Conf_Std = []
    FAR_Total_Std = []
    FAR_Avg_Std = []
    Num_Of_Unlocks_Std = []
    Num_Of_Accepted_Avg_Std = []

    def __init__(self):
        self.OrgTrnSize = []
        self.OrgTstSize = []
        self.AttNum = []
        self.Att_TotalSize = []
        self.Att_AvgSize = []
        self.FRR = []
        self.FRR_Conf = []
        self.FAR_Total = []
        self.FAR_Avg = []
        self.Num_Of_Unlocks = []
        self.Num_Of_Accepted_Avg = []
        self.OrgTrnSize_Std = []
        self.OrgTstSize_Std = []
        self.AttNum_Std = []
        self.Att_TotalSize_Std = []
        self.Att_AvgSize_Std = []
        self.FRR_Std = []
        self.FRR_Conf_Std = []
        self.FAR_Total_Std = []
        self.FAR_Avg_Std = []
        self.Num_Of_Unlocks_Std = []
        self.Num_Of_Accepted_Avg_Std = []

    # Set Methods
    def setOrgTrnSize(self, value):
        self.OrgTrnSize.append(value)

    def setOrgTstSize(self, value):
        self.OrgTstSize.append(value)

    def setAttNum(self, value):
        self.AttNum.append(value)

    def setAtt_TotalSize(self, value):
        self.Att_TotalSize.append(value)

    def setAtt_AvgSize(self, value):
        self.Att_AvgSize.append(value)

    def setFRR(self, value):
        self.FRR.append(value)

    def setFRR_Conf(self, value):
        self.FRR_Conf.append(value)

    def setFAR_Total(self, value):
        self.FAR_Total.append(value)

    def setFAR_Avg(self, value):
        self.FAR_Avg.append(value)

    def setNum_Of_Unlocks(self, value):
        self.Num_Of_Unlocks.append(value)

    def setNum_Of_Accepted_Avg(self, value):
        self.Num_Of_Accepted_Avg.append(value)

    def setOrgTrnSize_Std(self, value):
        self.OrgTrnSize_Std.append(value)

    def setOrgTstSize_Std(self, value):
        self.OrgTstSize_Std.append(value)

    def setAttNum_Std(self, value):
        self.AttNum_Std.append(value)

    def setAtt_TotalSize_Std(self, value):
        self.Att_TotalSize_Std.append(value)

    def setAtt_AvgSize_Std(self, value):
        self.Att_AvgSize_Std.append(value)

    def setFRR_Std(self, value):
        self.FRR_Std.append(value)

    def setFRR_Conf_Std(self, value):
        self.FRR_Conf_Std.append(value)

    def setFAR_Total_Std(self, value):
        self.FAR_Total_Std.append(value)

    def setFAR_Avg_Std(self, value):
        self.FAR_Avg_Std.append(value)

    def setNum_Of_Unlocks_Std(self, value):
        self.Num_Of_Unlocks_Std.append(value)

    def setNum_Of_Accepted_Avg_Std(self, value):
        self.Num_Of_Accepted_Avg_Std.append(value)

    # Get Methods
    def getOrgTrnSize(self):
        return self.OrgTrnSize

    def getOrgTstSize(self):
        return self.OrgTstSize

    def getAttNum(self):
        return self.AttNum

    def getAtt_TotalSize(self):
        return self.Att_TotalSize

    def getAtt_AvgSize(self):
        return self.Att_AvgSize

    def getFRR(self):
        return self.FRR

    def getFRR_Conf(self):
        return self.FRR_Conf

    def getFAR_Total(self):
        return self.FAR_Total

    def getFAR_Avg(self):
        return self.FAR_Avg

    def getNum_Of_Unlocks(self):
        return self.Num_Of_Unlocks

    def getNum_Of_Accepted_Avg(self):
        return self.Num_Of_Accepted_Avg

    def getOrgTrnSize_Std(self):
        return self.OrgTrnSize_Std

    def getOrgTstSize_Std(self):
        return self.OrgTstSize_Std

    def getAttNum_Std(self):
        return self.AttNum_Std

    def getAtt_TotalSize_Std(self):
        return self.Att_TotalSize_Std

    def getAtt_AvgSize_Std(self):
        return self.Att_AvgSize_Std

    def getFRR_Std(self):
        return self.FRR_Std

    def getFRR_Conf_Std(self):
        return self.FRR_Conf_Std

    def getFAR_Total_Std(self):
        return self.FAR_Total_Std

    def getFAR_Avg_Std(self):
        return self.FAR_Avg_Std

    def getNum_Of_Unlocks_Std(self):
        return self.Num_Of_Unlocks_Std

    def getNum_Of_Accepted_Avg_Std(self):
        return self.Num_Of_Accepted_Avg_Std
