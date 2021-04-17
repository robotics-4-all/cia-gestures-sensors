"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Labgroup

Author : Christos Emmanouil

Thesis : Continuous implicit authentication of mobile phone users with a combination of navigation and behavior data.

s5_Class_EvaluationMetrics
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
    TrnSize = []
    TstSize = []

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
        self.TrnSize = []
        self.TstSize = []


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

    def setTrnSize(self, value):
        self.TrnSize.append(value)
        
    def setTstSize(self, value):
        self.TstSize.append(value)


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

    def getTrnSize(self):
        return self.TrnSize

    def getTstSize(self):
        return self.TstSize