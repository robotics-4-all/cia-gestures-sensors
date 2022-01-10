"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import pandas as pd


# ============= #
#    Classes    #
# ============= #
class FeaturesSns:

    def __init__(self):

        self.User = []
        self.Type = []
        self.StartTime = []
        self.StopTime = []
        self.Group = []
        self.Window = []
        self.Mean = []
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

    # Set Methods
    def setUser(self, value=None):
        self.User.append(value)

    def setType(self, value=None):
        self.Type.append(value)

    def setStartTime(self, value=None):
        self.StartTime.append(value)

    def setStopTime(self, value=None):
        self.StopTime.append(value)

    def setGroup(self, value=None):
        self.Group.append(value)

    def setWindow(self, value=None):
        self.Window.append(value)

    def setMean(self, value=None):
        self.Mean.append(value)

    def setSTD(self, value=None):
        self.STD.append(value)

    def setMax(self, value=None):
        self.Max.append(value)

    def setMin(self, value=None):
        self.Min.append(value)

    def setRange(self, value=None):
        self.Range.append(value)

    def setPercentile25(self, value=None):
        self.Percentile25.append(value)

    def setPercentile50(self, value=None):
        self.Percentile50.append(value)

    def setPercentile75(self, value=None):
        self.Percentile75.append(value)

    def setKurtosis(self, value=None):
        self.Kurtosis.append(value)

    def setSkewness(self, value=None):
        self.Skewness.append(value)

    def setEntropy(self, value=None):
        self.Entropy.append(value)

    def setAmplitude1(self, value=None):
        self.Amplitude1.append(value)

    def setAmplitude2(self, value=None):
        self.Amplitude2.append(value)

    def setFrequency2(self, value=None):
        self.Frequency2.append(value)

    def setMeanFrequency(self, value=None):
        self.MeanFrequency.append(value)

    # Create dataframe method
    def create_dataframe(self, feature: str, first: bool) -> pd.DataFrame:

        df = pd.DataFrame()
        if first:
            df['User'] = self.User
            df['Type'] = self.Type
            df['StartTime'] = self.StartTime
            df['StopTime'] = self.StopTime
            df['Group'] = self.Group
            df['Window'] = self.Window
        df['Mean_' + feature] = self.Mean
        df['STD_' + feature] = self.STD
        df['Max_' + feature] = self.Max
        df['Min_' + feature] = self.Min
        df['Range_' + feature] = self.Range
        df['Percentile25_' + feature] = self.Percentile25
        df['Percentile50_' + feature] = self.Percentile50
        df['Percentile75_' + feature] = self.Percentile75
        df['Kurtosis_' + feature] = self.Kurtosis
        df['Skewness_' + feature] = self.Skewness
        df['Entropy_' + feature] = self.Entropy
        df['Amplitude1_' + feature] = self.Amplitude1
        df['Amplitude2_' + feature] = self.Amplitude2
        df['Frequency2_' + feature] = self.Frequency2
        df['MeanFrequency_' + feature] = self.MeanFrequency

        return df


class FeaturesGes:

    def __init__(self):

        self.User = []
        self.Type = []
        self.StartTime = []
        self.StopTime = []
        self.Duration = []
        self.MeanX = []
        self.MeanY = []
        self.TraceLength = []
        self.StartStopLength = []
        self.TraceProjection = []
        self.ScreenPercentage = []
        self.StartVelocity = []
        self.StopVelocity = []
        self.AccelerationHor = []
        self.AccelerationVer = []
        self.Slope = []
        self.MeanSquareError = []
        self.MeanAbsError = []
        self.MedianAbsError = []
        self.CoefDetermination = []

    # Set Methods
    def setUser(self, value=None):
        self.User.append(value)

    def setType(self, value=None):
        self.Type.append(value)

    def setStartTime(self, value=None):
        self.StartTime.append(value)

    def setStopTime(self, value=None):
        self.StopTime.append(value)

    def setDuration(self, value=None):
        self.Duration.append(value)

    def setMeanX(self, value=None):
        self.MeanX.append(value)

    def setMeanY(self, value=None):
        self.MeanY.append(value)

    def setTraceLength(self, value=None):
        self.TraceLength.append(value)

    def setStartStopLength(self, value=None):
        self.StartStopLength.append(value)

    def setTraceProjection(self, value=None):
        self.TraceProjection.append(value)

    def setScreenPercentage(self, value=None):
        self.ScreenPercentage.append(value)

    def setStartVelocity(self, value=None):
        self.StartVelocity.append(value)

    def setStopVelocity(self, value=None):
        self.StopVelocity.append(value)

    def setAccelerationHor(self, value=None):
        self.AccelerationHor.append(value)

    def setAccelerationVer(self, value=None):
        self.AccelerationVer.append(value)

    def setSlope(self, value=None):
        self.Slope.append(value)

    def setMeanSquareError(self, value=None):
        self.MeanSquareError.append(value)

    def setMeanAbsError(self, value=None):
        self.MeanAbsError.append(value)

    def setMedianAbsError(self, value=None):
        self.MedianAbsError.append(value)

    def setCoefDetermination(self, value=None):
        self.CoefDetermination.append(value)

    # Create dataframe method
    def create_dataframe(self) -> pd.DataFrame:

        df = pd.DataFrame()
        df['User'] = self.User
        df['Type'] = self.Type
        df['StartTime'] = self.StartTime
        df['StopTime'] = self.StopTime
        df['Duration'] = self.Duration
        df['MeanX'] = self.MeanX
        df['MeanY'] = self.MeanY
        df['TraceLength'] = self.TraceLength
        df['StartStopLength'] = self.StartStopLength
        df['ScreenPercentage'] = self.ScreenPercentage
        df['TraceProjection'] = self.TraceProjection
        df['StartVelocity'] = self.StartVelocity
        df['StopVelocity'] = self.StopVelocity
        df['AccelerationHor'] = self.AccelerationHor
        df['AccelerationVer'] = self.AccelerationVer
        df['Slope'] = self.Slope
        df['MeanSquareError'] = self.MeanSquareError
        df['MeanAbsError'] = self.MeanAbsError
        df['MedianAbsError'] = self.MedianAbsError
        df['CoefDetermination'] = self.CoefDetermination

        return df
