"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Lab Group

Author : Christos Emmanouil
"""


class EvaluationMetrics:

    Accuracy = []
    F1Score = []
    ROC = []
    FAR = []
    FRR = []
    FalseAccept = []
    FalseReject = []
    TrueAccept = []
    TrueReject = []
    TrnOrgSize = []
    TstOrgSize =[]
    TstAttSize = []

    def __init__(self):
        self.Accuracy = []
        self.F1Score = []
        self.ROC = []
        self.FAR = []
        self.FRR = []
        self.FalseAccept = []
        self.FalseReject = []
        self.TrueAccept = []
        self.TrueReject = []
        self.TrnOrgSize = []
        self.TstOrgSize = []
        self.TstAttSize = []

    # Set Methods
    def setAccuracy(self, value):
        self.Accuracy.append(value)

    def setF1Score(self, value):
        self.F1Score.append(value)

    def setROC(self, value):
        self.ROC.append(value)

    def setFAR(self, value):
        self.FAR.append(value)

    def setFRR(self, value):
        self.FRR.append(value)

    def setFalseAccept(self, value):
        self.FalseAccept.append(value)

    def setFalseReject(self, value):
        self.FalseReject.append(value)

    def setTrueAccept(self, value):
        self.TrueAccept.append(value)

    def setTrueReject(self, value):
        self.TrueReject.append(value)

    def setTrnOrgSize(self, value):
        self.TrnOrgSize.append(value)

    def setTstOrgSize(self, value):
        self.TstOrgSize.append(value)

    def setTstAttSize(self, value):
        self.TstAttSize.append(value)

    # Get Methods
    def getAccuracy(self):
        return self.Accuracy

    def getF1Score(self):
        return self.F1Score

    def getROC(self):
        return self.ROC

    def getFAR(self):
        return self.FAR

    def getFRR(self):
        return self.FRR

    def getFalseAccept(self):
        return self.FalseAccept

    def getFalseReject(self):
        return self.FalseReject

    def getTrueAccept(self):
        return self.TrueAccept

    def getTrueReject(self):
        return self.TrueReject

    def getTrnOrgSize(self):
        return self.TrnOrgSize

    def getTstOrgSize(self):
        return self.TstOrgSize

    def getTstAttSize(self):
        return self.TstAttSize
