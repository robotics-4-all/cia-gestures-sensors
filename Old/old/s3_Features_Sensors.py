class Features_Sensors:
    
    User = []
    ScreenName = []
    
    TimeStamp = []
    Num_Of_Samples = []
  
    Μean = []
    STD = []
    Max = []
    Min = []
    Range = []
    Percentile25 = []
    Percentile50 = []
    Percentile75 = []
    Kurtosis = []
    Skewness = []
    Entropy = []

    Amplitude1 = []
    Amplitude2 = []
    Frequency2 = []
    MeanFrequency = []

    Dx = []
    Dy = []
    Vx = []
    Vy = []

    Output = []

    def __init__(self):
        self.User = []
        self.ScreenName = []
        
        self.TimeStamp = []
        self.Num_Of_Samples = []
        
        self.Μean = []
        self.STD = []
        self.Max = []
        self.Min = []
        self.Range = []
        self.Percentile25 = []
        self.Percentile50 = []
        self.Percentile75 = []
        self.Kurtosis = []
        self.Skewness = []
        self.Entropy = []

        self.Amplitude1 = []
        self.Amplitude2 = []
        self.Frequency2 = []
        self.MeanFrequency = []

        self.Dx = []
        self.Dy = []
        self.Vx = []
        self.Vy = []
        
        self.Output = []

    # Set Methods
    def setUser(self, value):
        self.User.append(value)
        
    def setScreenName(self, value):
        self.ScreenName.append(value)
        
    def setTimeStamp(self, value):
        self.TimeStamp.append(value)
        
    def setNum_Of_Samples(self, value):
        self.Num_Of_Samples.append(value)
    
    def setΜean(self, value):
        self.Μean.append(value)
    
    def setSTD(self, value):
        self.STD.append(value)

    def setMax(self, value):
        self.Max.append(value)
    
    def setMin(self, value):
        self.Min.append(value)

    def setRange(self, value):
        self.Range.append(value)

    def setPercentile25(self, value):
        self.Percentile25.append(value)

    def setPercentile50(self, value):
        self.Percentile50.append(value)

    def setPercentile75(self, value):
        self.Percentile75.append(value)

    def setKurtosis(self, value):
        self.Kurtosis.append(value)

    def setSkewness(self, value):
        self.Skewness.append(value)

    def setEntropy(self, value):
        self.Entropy.append(value)

    def setAmplitude1(self, value):
        self.Amplitude1.append(value)

    def setAmplitude2(self, value):
        self.Amplitude2.append(value)

    def setFrequency2(self, value):
        self.Frequency2.append(value)

    def setMeanFrequency(self, value):
        self.MeanFrequency.append(value)

    def setDx(self, value):
        self.Dx.append(value)  

    def setDy(self, value):
        self.Dy.append(value)

    def setVx(self, value):
        self.Vx.append(value)

    def setVy(self, value):
        self.Vy.append(value)
        
    def setOutput(self, value):
        self.Output.append(value)

    # Get Methods
    def getUser(self):
        return self.User
    
    def getScreenName(self):
        return self.ScreenName    
    
    def getTimeStamp(self):
        return self.TimeStamp
    
    def getNum_Of_Samples(self):
        return self.Num_Of_Samples
    
    def getMean(self):
        return self.Μean

    def getSTD(self):
        return self.STD
    
    def getMax(self):
        return self.Max
    
    def getMin(self):
        return self.Min

    def getRange(self):
        return self.Range

    def getPercentile25(self):
        return self.Percentile25

    def getPercentile50(self):
        return self.Percentile50

    def getPercentile75(self):
        return self.Percentile75

    def getKurtosis(self):
        return self.Kurtosis

    def getEntropy(self):
        return self.Entropy

    def getSkewness(self):
        return self.Skewness

    def getAmplitude1(self):
        return self.Amplitude1

    def getAmplitude2(self):
        return self.Amplitude2

    def getFrequency2(self):
        return self.Frequency2

    def getMeanFrequency(self):
        return self.MeanFrequency

    def getDx(self):
        return self.Dx

    def getDy(self):
        return self.Dy

    def getVx(self):
        return self.Vx

    def getVy(self):
        return self.Vy
    
    def getOutput(self):
        return self.Output