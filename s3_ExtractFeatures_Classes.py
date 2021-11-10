"""
This script was created at 14-Sep-21
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
        self.Timestamp = []
        self.Screen = []

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
    def setUser(self, value):
        self.User.append(value)

    def setTimestamp(self, value):
        self.Timestamp.append(value)

    def setScreen(self, value):
        self.Screen.append(value)

    def setMean(self, value):
        self.Mean.append(value)

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

    # Create dataframe method
    def create_dataframe(self) -> pd.DataFrame:

        df = pd.DataFrame()

        df['User'] = self.User
        df['Timestamp'] = self.Timestamp
        df['Screen'] = self.Screen
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


class FeaturesSwp:

    def __init__(self):
        self.User = []
        self.TimeStart = []
        self.TimeStop = []
        self.Screen = []

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
    def setUser(self, value):
        self.User.append(value)

    def setTimeStart(self, value):
        self.TimeStart.append(value)

    def setTimeStop(self, value):
        self.TimeStop.append(value)

    def setScreen(self, value):
        self.Screen.append(value)

    def setDuration(self, value):
        self.Duration.append(value)

    def setMeanX(self, value):
        self.MeanX.append(value)

    def setMeanY(self, value):
        self.MeanY.append(value)

    def setTraceLength(self, value):
        self.TraceLength.append(value)

    def setStartStopLength(self, value):
        self.StartStopLength.append(value)

    def setTraceProjection(self, value):
        self.TraceProjection.append(value)

    def setScreenPercentage(self, value):
        self.ScreenPercentage.append(value)

    def setRatio(self, value):
        self.Ratio.append(value)

    def setDeviation(self, value):
        self.Deviation.append(value)

    def setLeaning(self, value):
        self.Leaning.append(value)

    def setStartVelocity(self, value):
        self.StartVelocity.append(value)

    def setStopVelocity(self, value):
        self.StopVelocity.append(value)

    def setAccelerationHor(self, value):
        self.AccelerationHor.append(value)

    def setAccelerationVer(self, value):
        self.AccelerationVer.append(value)

    def setSlope(self, value):
        self.Slope.append(value)

    def setMeanSquareError(self, value):
        self.MeanSquareError.append(value)

    def setMeanAbsError(self, value):
        self.MeanAbsError.append(value)

    def setMedianAbsError(self, value):
        self.MedianAbsError.append(value)

    def setCoefDetermination(self, value):
        self.CoefDetermination.append(value)

    # Create dataframe method
    def create_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame()

        df['User'] = self.User
        df['TimeStart'] = self.TimeStart
        df['TimeStop'] = self.TimeStop
        df['Screen'] = self.Screen
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


class FeaturesTap:

    def __init__(self):
        self.User = []
        self.TimeStart = []
        self.TimeStop = []
        self.Screen = []

        self.Duration = []

    # Set Methods
    def setUser(self, value):
        self.User.append(value)

    def setTimeStart(self, value):
        self.TimeStart.append(value)

    def setTimeStop(self, value):
        self.TimeStop.append(value)

    def setScreen(self, value):
        self.Screen.append(value)

    # Create dataframe method
    def create_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame()

        df['User'] = self.User
        df['TimeStart'] = self.TimeStart
        df['TimeStop'] = self.TimeStop
        df['Screen'] = self.Screen
        df['Duration'] = self.Duration

        return df
