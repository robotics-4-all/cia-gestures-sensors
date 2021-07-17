"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Labgroup

Author : Christos Emmanouil

Thesis : Continuous implicit authentication of mobile phone users with a combination of navigation and behavior data.

s3_Class_Features_Swipes
"""

class Features_Swipes:
    
    User = []
    Screen = []
    
    Type = []
    
    Time_Start = []
    Time_Stop = []
    Duration = []
    
    Trace_Length_Horizontal = []
    Trace_Length_Vertical = []
    Direction = []
    
    Slope = []
    Mean_Square_Error = []
    Mean_Abs_Error = []
    Median_Abs_Error = []
    Coef_Determination = []
    
    Mean_X = []
    Mean_Y = []
    
    Acceleration_Horizontal = []
    Acceleration_Vertical = []
    
    
    def __init__(self):
        self.User = []
        self.Screen = []
        
        self.Type = []
        
        self.Time_Start = []
        self.Time_Stop = []
        self.Duration = []
        
        self.Trace_Length_Horizontal = []
        self.Trace_Length_Vertical = []
        self.Direction = []
        
        self.Slope = []
        self.Mean_Square_Error = []
        self.Mean_Abs_Error = []
        self.Median_Abs_Error = []
        self.Coef_Determination = []
        
        self.Mean_X = []
        self.Mean_Y = []
        
        self.Acceleration_Horizontal = []
        self.Acceleration_Vertical = []
        
    
    # Set Methods
    def setUser(self, value):
        self.User.append(value)
        
    def setScreen(self, value):
        self.Screen.append(value)
    
    def setType(self, value):
        self.Type.append(value)
    
    def setTime_Start(self, value):
        self.Time_Start.append(value)
    
    def setTime_Stop(self, value):
        self.Time_Stop.append(value)
        
    def setDuration(self, value):
        self.Duration.append(value)
    
    def setTrace_Length_Horizontal(self, value):
        self.Trace_Length_Horizontal.append(value)
    
    def setTrace_Length_Vertical(self, value):
        self.Trace_Length_Vertical.append(value)
    
    def setDirection(self, value):
        self.Direction.append(value)
    
    def setSlope(self, value):
        self.Slope.append(value)
    
    def setMean_Square_Error(self, value):
        self.Mean_Square_Error.append(value)
    
    def setMean_Abs_Error(self, value):
        self.Mean_Abs_Error.append(value)
    
    def setMedian_Abs_Error(self, value):
        self.Median_Abs_Error.append(value)
    
    def setCoef_Determination(self, value):
        self.Coef_Determination.append(value)
        
    def setAcceleration_Horizontal(self, value):
        self.Acceleration_Horizontal.append(value)
        
    def setAcceleration_Vertical(self, value):
        self.Acceleration_Vertical.append(value)
    
    def setMean_X(self, value):
        self.Mean_X.append(value)
    
    def setMean_Y(self, value):
        self.Mean_Y.append(value)
        
        
    # Get Methods
    def getUser(self):
        return self.User
    
    def getScreen(self):
        return self.Screen
    
    def getType(self):
        return self.Type
    
    def getTime_Start(self):
        return self.Time_Start
    
    def getTime_Stop(self):
        return self.Time_Stop
    
    def getDuration(self):
        return self.Duration
    
    def getTrace_Length_Horizontal(self):
        return self.Trace_Length_Horizontal
    
    def getTrace_Length_Vertical(self):
        return self.Trace_Length_Vertical
    
    def getDirection(self):
        return self.Direction
    
    def getSlope(self):
        return self.Slope
    
    def getMean_Square_Error(self):
        return self.Mean_Square_Error
    
    def getMean_Abs_Error(self):
        return self.Mean_Abs_Error
    
    def getMedian_Abs_Error(self):
        return self.Median_Abs_Error
    
    def getCoef_Determination(self):
        return self.Coef_Determination
    
    def getAcceleration_Horizontal(self):
        return self.Acceleration_Horizontal
        
    def getAcceleration_Vertical(self):
        return self.Acceleration_Vertical
    
    def getMean_X(self):
        return self.Mean_X
    
    def getMean_Y(self):
        return self.Mean_Y