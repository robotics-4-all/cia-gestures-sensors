"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Labgroup

Author : Christos Emmanouil

Thesis : Continuous implicit authentication of mobile phone users with a combination of navigation and behavior data.

s5_Class_EvaluationMetrics
"""

class EvaluationMetrics:
  
    TrnOrgSize = []
    TstOrgSize =[]
    TstAttSize = []
    Num_Of_Unlocks = [] # For original users, posa unlocks xriastike na kanei?
    Num_Of_Accepted = [] # For attackers

    def __init__(self):
        self.TrnOrgSize = []
        self.TstOrgSize = []
        self.TstAttSize = []
        self.Num_Of_Unlocks = []
        self.Num_Of_Accepted = []

    # Set Methods
    def setTrnOrgSize(self, value):
        self.TrnOrgSize.append(value)
        
    def setTstOrgSize(self, value):
        self.TstOrgSize.append(value)

    def setTstAttSize(self, value):
        self.TstAttSize.append(value)
        
    def setNum_Of_Unlocks(self, value):
        self.Num_Of_Unlocks.append(value)

    def setNum_Of_Accepted(self, value):
        self.Num_Of_Accepted.append(value)
        
    # Get Methods
    def getTrnOrgSize(self):
        return self.TrnOrgSize

    def getTstOrgSize(self):
        return self.TstOrgSize
    
    def getTstAttSize(self):
        return self.TstAttSize
    
    def getNum_Of_Unlocks(self):
        return self.Num_Of_Unlocks

    def getNum_Of_Accepted(self):
        return self.Num_Of_Accepted