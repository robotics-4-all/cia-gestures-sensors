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
        self.Screen = []

        self.Timestamp = []
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

        self.Dx = []
        self.Dy = []
        self.Vx = []
        self.Vy = []

    # Set Methods
    def setUser(self, value=None):
        self.User.append(value)

    def setScreen(self, value=None):
        self.Screen.append(value)

    def setTimestamp(self, value=None):
        self.Timestamp.append(value)

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

    def setDx(self, value=None):
        self.Dx.append(value)

    def setDy(self, value=None):
        self.Dy.append(value)

    def setVx(self, value=None):
        self.Vx.append(value)

    def setVy(self, value=None):
        self.Vy.append(value)

    # Create dataframe method
    def create_dataframe(self) -> pd.DataFrame:

        df = pd.DataFrame()

        df['User'] = self.User
        df['Screen'] = self.Screen
        df['Timestamp'] = self.Timestamp
        df['StartTime'] = self.StartTime
        df['StopTime'] = self.StopTime
        df['Group'] = self.Group
        df['Window'] = self.Window
        df['Mean'] = self.Mean
        df['STD'] = self.STD
        df['Max'] = self.Max
        df['Min'] = self.Min
        df['Range'] = self.Range
        df['Percentile25'] = self.Percentile25
        df['Percentile50'] = self.Percentile50
        df['Percentile75'] = self.Percentile75
        df['Kurtosis'] = self.Kurtosis
        df['Skewness'] = self.Skewness
        df['Entropy'] = self.Entropy
        df['Amplitude1'] = self.Amplitude1
        df['Amplitude2'] = self.Amplitude2
        df['Frequency2'] = self.Frequency2
        df['MeanFrequency'] = self.MeanFrequency

        return df


class FeaturesGes:

    def __init__(self):
        self.User = []
        self.Screen = []
        self.Type = []

        self.TimeStart = []
        self.TimeStop = []
        self.Duration = []

        self.MeanX = []
        self.MeanY = []

        self.TraceLength = []
        self.StartStopLength = []

        self.TraceProjection = []
        self.ScreenPercentage = []

        self.Ratio = []
        self.Deviation = []
        self.Leaning = []

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

    def setScreen(self, value=None):
        self.Screen.append(value)

    def setType(self, value=None):
        self.Type.append(value)

    def setTimeStart(self, value=None):
        self.TimeStart.append(value)

    def setTimeStop(self, value=None):
        self.TimeStop.append(value)

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

    def setRatio(self, value=None):
        self.Ratio.append(value)

    def setDeviation(self, value=None):
        self.Deviation.append(value)

    def setLeaning(self, value=None):
        self.Leaning.append(value)

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
        df['Screen'] = self.Screen
        df['Type'] = self.Type
        df['TimeStart'] = self.TimeStart
        df['TimeStop'] = self.TimeStop
        df['Duration'] = self.Duration
        df['MeanX'] = self.MeanX
        df['MeanY'] = self.MeanY
        df['TraceLength'] = self.TraceLength
        df['StartStopLength'] = self.StartStopLength
        df['ScreenPercentage'] = self.ScreenPercentage
        df['TraceProjection'] = self.TraceProjection
        df['Ratio'] = self.Ratio
        df['Deviation'] = self.Deviation
        df['Leaning'] = self.Leaning
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
