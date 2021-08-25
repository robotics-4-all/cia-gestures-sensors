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
from tqdm import tqdm
from scipy.fftpack import fft
from scipy.stats import skew, kurtosis, entropy

from s0_Funcs_Util_v000 import linear_regression as lr
from s3_Class_Features_Swipes_v000 import Features_Swipes
from s3_Class_Features_Sensors_v000 import Features_Sensors


# =============== #
#    Functions    #
# =============== #
def FeatureExtraction_Swipes(Gesture, Normalize, FeautureObject):
    """
    Extract features from a gesture.

    :param Gesture: A dataframe row, contains details for a gesture
    :param Normalize: If True normalize gestures data in a specific screen size
    :param FeautureObject: An object from Features_Swipes class in s3_Class_Features_Swipes_v000
    :return: The updated FeatureObject
    """
    scalar_width = 400
    scalar_height = 700

    FeautureObject.setUser(Gesture['User'])
    FeautureObject.setScreen(Gesture['Screen'])
    FeautureObject.setType(Gesture['G_Type'])
    FeautureObject.setTime_Start(Gesture['G_tStart'])
    FeautureObject.setTime_Stop(Gesture['G_tStop'])
    FeautureObject.setDuration(Gesture['G_Duration'])

    x_positions = []
    y_positions = []
    x_positions.append(Gesture['G_Data'][0]['x0'])
    y_positions.append(Gesture['G_Data'][0]['y0'])
    for data in Gesture['G_Data']:
        x_positions.append(data["moveX"])
        y_positions.append(data["moveY"])

    length_horizontal = x_positions[-1] - x_positions[0]
    length_vertical = y_positions[-1] - y_positions[0]
    if Normalize:
        length_horizontal = scalar_width * length_horizontal / Gesture['D_Width']
        length_vertical = scalar_height * length_vertical / Gesture['D_Height']
    FeautureObject.setTrace_Length_Horizontal(np.abs(length_horizontal))
    FeautureObject.setTrace_Length_Vertical(np.abs(length_vertical))

    if np.abs(length_horizontal) > np.abs(length_vertical):
        if length_horizontal > 0:
            direction = 'right'
        else:
            direction = 'left'
    else:
        if length_vertical > 0:
            direction = 'up'
        else:
            direction = 'down'
    FeautureObject.setDirection(direction)

    Trace_Stats = lr(x_positions, y_positions)
    FeautureObject.setSlope(Trace_Stats['slope'])
    FeautureObject.setMean_Square_Error(Trace_Stats['mean_squared_error'])
    FeautureObject.setMean_Abs_Error(Trace_Stats['mean_abs_error'])
    FeautureObject.setMedian_Abs_Error(Trace_Stats['median_abs_error'])
    FeautureObject.setCoef_Determination(Trace_Stats['coef_determination'])

    Acceleration_Horizontal = ((Gesture['G_Data'][-1]['vx'] - Gesture['G_Data'][0]['vx']) /
                               ((Gesture['G_tStop'] - Gesture['G_tStart'])*0.001))
    Acceleration_Vertical = ((Gesture['G_Data'][-1]['vy'] - Gesture['G_Data'][0]['vy']) /
                             ((Gesture['G_tStop'] - Gesture['G_tStart'])*0.001))
    FeautureObject.setAcceleration_Horizontal(Acceleration_Horizontal)
    FeautureObject.setAcceleration_Vertical(Acceleration_Vertical)

    mean_x = 0
    mean_y = 0
    for x in x_positions:
        mean_x += x
    for y in y_positions:
        mean_y += y
    mean_x /= len(x_positions)
    mean_y /= len(y_positions)
    if Normalize:
        mean_x = scalar_width * mean_x / Gesture['D_Width']
        mean_y = scalar_height * mean_y / Gesture['D_Height']
    FeautureObject.setMean_X(mean_x)
    FeautureObject.setMean_Y(mean_y)

    return FeautureObject


def Create_DFF_Swipes(DF_Gest, Normalize):
    """
    Create a dataframe with swipes features.

    :param DF_Gest: A dataframe that returned from the Create_DF_Gestures function in s2_Funcs_CreateDataFrames_v002
    :param Normalize: If True normalize gestures data in a specific screen size
    :return: A dataframe with the swipes features
    """

    F_Swipes = Features_Swipes()
    for idx in tqdm(range(len(DF_Gest))):
        G = DF_Gest.loc[idx]
        if G['G_Type'] == 'swipe':
            F_Swipes = FeatureExtraction_Swipes(G, Normalize, F_Swipes)
    DFF_Swipes = pd.DataFrame()

    DFF_Swipes['User'] = F_Swipes.getUser()
    DFF_Swipes['Screen'] = F_Swipes.getScreen()
    DFF_Swipes['Type'] = F_Swipes.getType()
    DFF_Swipes['Time_Start'] = F_Swipes.getTime_Start()
    DFF_Swipes['Time_Stop'] = F_Swipes.getTime_Stop()
    DFF_Swipes['Duration'] = F_Swipes.getDuration()
    DFF_Swipes['Trace_Length_Horizontal'] = F_Swipes.getTrace_Length_Horizontal()
    DFF_Swipes['Trace_Length_Vertical'] = F_Swipes.getTrace_Length_Vertical()
    DFF_Swipes['Direction'] = F_Swipes.getDirection()
    DFF_Swipes['Slope'] = F_Swipes.getSlope()
    DFF_Swipes['Mean_Square_Error'] = F_Swipes.getMean_Square_Error()
    DFF_Swipes['Mean_Abs_Error'] = F_Swipes.getMean_Abs_Error()
    DFF_Swipes['Median_Abs_Error'] = F_Swipes.getMedian_Abs_Error()
    DFF_Swipes['Coef_Determination'] = F_Swipes.getCoef_Determination()
    DFF_Swipes['Mean_X'] = F_Swipes.getMean_X()
    DFF_Swipes['Mean_Y'] = F_Swipes.getMean_Y()
    DFF_Swipes['Acceleration_Horizontal'] = F_Swipes.getAcceleration_Horizontal()
    DFF_Swipes['Acceleration_Vertical'] = F_Swipes.getAcceleration_Vertical()

    print('-> Extracting Swipes Features Finished')

    return DFF_Swipes


def FeatureExtraction_Sensors(User, TimeStamp, Screen, Dataset, Window, Overlap, FeautureObject):
    """
    Extract features from a sensors data window.
    The window contains data from the same screen.

    :param User: The user name
    :param TimeStamp: The timestamp
    :param Screen: The sceen name
    :param Dataset: The window with the data
    :param Window: The window size from which the features will be extracted
    :param Overlap: The overlap between the windows
    :param FeautureObject: An object from Features_Sensors class in s3_Class_Features_Sensors_v000
    :return: The updated FeatureObject
    """

    Overlap = int(Overlap * Window)
    Dataset_Size = Dataset.shape[0]
    if Dataset_Size >= Window:
        Flag = True
        Start = 0
        while Dataset_Size > 0:

            Stop = Start + Window

            FeautureObject.setUser(User)
            FeautureObject.setTimeStamp(TimeStamp)
            FeautureObject.setScreen(Screen)
            FeautureObject.setNum_Of_Samples(Stop - Start)
            # DFT
            discreteFourier = fft(Dataset[Start:Stop])
            freq = np.fft.fftfreq(Stop - Start)
            # Amplitudes
            idx = (np.absolute(discreteFourier)).argsort()[-2:][::-1]
            amplitude1 = np.absolute(discreteFourier[idx[0]])
            amplitude2 = np.absolute(discreteFourier[idx[1]])
            frequency2 = freq[idx[1]]
            # Frequency features
            mean_frequency = np.mean(freq)
            FeautureObject.setAmplitude1(amplitude1)
            FeautureObject.setAmplitude2(amplitude2)
            FeautureObject.setFrequency2(frequency2)
            FeautureObject.setMeanFrequency(mean_frequency)
            # Time Based Features
            FeautureObject.setΜean(np.mean(Dataset[Start:Stop]))
            FeautureObject.setSTD(np.std(Dataset[Start:Stop]))
            FeautureObject.setMax(np.max(Dataset[Start:Stop]))
            FeautureObject.setMin(np.min(Dataset[Start:Stop]))
            FeautureObject.setRange(np.ptp(Dataset[Start:Stop]))
            percentile = np.percentile(Dataset[Start:Stop], [25, 50, 75])
            FeautureObject.setPercentile25(percentile[0])
            FeautureObject.setPercentile50(percentile[1])
            FeautureObject.setPercentile75(percentile[2])
            FeautureObject.setEntropy(entropy(Dataset[Start:Stop], base=2))
            FeautureObject.setKurtosis(kurtosis(Dataset[Start:Stop]))
            FeautureObject.setSkewness(skew(Dataset[Start:Stop]))

            if Flag:
                Dataset_Size = Dataset_Size - (Stop - Start)
                Flag = False
            else:
                Dataset_Size = Dataset_Size - (Stop - Start) + Overlap
            if Dataset_Size + Overlap < Window:
                if Dataset_Size < Overlap:
                    break
                Overlap = Window - Dataset_Size
            Start = Stop - Overlap

    return FeautureObject


def Create_DFF_Sensors(DF_Users, DF_Acc, DF_Gyr, Feature, Window, Overlap):
    """
    Create two dataframes with sensors features.
    The window contains data from the same screen.

    :param DF_Users: A sensors dataframe that returned from the findUsers_Common function in s1_Funcs_ExploreData_v002
    :param DF_Acc: A dataframe that returned from the Create_DF_Sensors function in s2_Funcs_CreateDataFrames_v002
    :param DF_Gyr: A dataframe that returned from the Create_DF_Sensors function in s2_Funcs_CreateDataFrames_v002
    :param Feature: The sensor feature from which the other features will be extracted (Magnitude)
    :param Window: The window size from which the features will be extracted
    :param Overlap: The overlap between the windows
    :return: Two dataframes with sensors features
    """

    F_Acc = Features_Sensors()
    F_Gyr = Features_Sensors()
    for User in tqdm(DF_Users['User'].values):
        List_Of_TS = DF_Users.loc[DF_Users['User'] == User]['List_Of_TS'].values[0]
        S_Of_TSs = DF_Users.loc[DF_Users['User'] == User]['S_Of_TSs'].values[0]
        for i in range(len(List_Of_TS)):
            TS = List_Of_TS[i]
            for j in range(len(S_Of_TSs[i])):
                Screen = S_Of_TSs[i][j]
                Data_Acc = DF_Acc.loc[(DF_Acc['User'] == User) &
                                      (DF_Acc['TS'] == TS) &
                                      (DF_Acc['Screen'] == Screen)][Feature].values
                Data_Gyr = DF_Gyr.loc[(DF_Gyr['User'] == User) &
                                      (DF_Gyr['TS'] == TS) &
                                      (DF_Gyr['Screen'] == Screen)][Feature].values
                F_Acc = FeatureExtraction_Sensors(User, TS, Screen, Data_Acc, Window, Overlap, F_Acc)
                F_Gyr = FeatureExtraction_Sensors(User, TS, Screen, Data_Gyr, Window, Overlap, F_Gyr)
    DFF_Acc = pd.DataFrame()
    DFF_Gyr = pd.DataFrame()

    DFF_Acc['User'] = F_Acc.getUser()
    DFF_Acc['TimeStamp'] = F_Acc.getTimeStamp()
    DFF_Acc['Screen'] = F_Acc.getScreen()
    DFF_Acc['Num_Of_Samples'] = F_Acc.getNum_Of_Samples()
    DFF_Acc['Mean'] = F_Acc.getMean()
    DFF_Acc['STD'] = F_Acc.getSTD()
    DFF_Acc['Max'] = F_Acc.getMax()
    DFF_Acc['Min'] = F_Acc.getMin()
    DFF_Acc['Range'] = F_Acc.getRange()
    DFF_Acc['Percentile25'] = F_Acc.getPercentile25()
    DFF_Acc['Percentile50'] = F_Acc.getPercentile50()
    DFF_Acc['Percentile75'] = F_Acc.getPercentile75()
    DFF_Acc['Kurtosis'] = F_Acc.getKurtosis()
    DFF_Acc['Skewness'] = F_Acc.getSkewness()
    DFF_Acc['Entropy'] = F_Acc.getEntropy()
    DFF_Acc['Amplitude1'] = F_Acc.getAmplitude1()
    DFF_Acc['Amplitude2'] = F_Acc.getAmplitude2()
    DFF_Acc['Frequency2'] = F_Acc.getFrequency2()
    DFF_Acc['MeanFrequency'] = F_Acc.getMeanFrequency()

    DFF_Gyr['User'] = F_Gyr.getUser()
    DFF_Gyr['TimeStamp'] = F_Gyr.getTimeStamp()
    DFF_Gyr['Screen'] = F_Gyr.getScreen()
    DFF_Gyr['Num_Of_Samples'] = F_Gyr.getNum_Of_Samples()
    DFF_Gyr['Mean'] = F_Gyr.getMean()
    DFF_Gyr['STD'] = F_Gyr.getSTD()
    DFF_Gyr['Max'] = F_Gyr.getMax()
    DFF_Gyr['Min'] = F_Gyr.getMin()
    DFF_Gyr['Range'] = F_Gyr.getRange()
    DFF_Gyr['Percentile25'] = F_Gyr.getPercentile25()
    DFF_Gyr['Percentile50'] = F_Gyr.getPercentile50()
    DFF_Gyr['Percentile75'] = F_Gyr.getPercentile75()
    DFF_Gyr['Kurtosis'] = F_Gyr.getKurtosis()
    DFF_Gyr['Skewness'] = F_Gyr.getSkewness()
    DFF_Gyr['Entropy'] = F_Gyr.getEntropy()
    DFF_Gyr['Amplitude1'] = F_Gyr.getAmplitude1()
    DFF_Gyr['Amplitude2'] = F_Gyr.getAmplitude2()
    DFF_Gyr['Frequency2'] = F_Gyr.getFrequency2()
    DFF_Gyr['MeanFrequency'] = F_Gyr.getMeanFrequency()

    print('-> Extracting Sensors Features Finished')

    return DFF_Acc, DFF_Gyr
