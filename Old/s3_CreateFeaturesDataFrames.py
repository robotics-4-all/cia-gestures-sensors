"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Labgroup

Author : Christos Emmanouil

Thesis : Continuous implicit authentication of mobile phone users with a combination of navigation and behavior data.

CreateFeaturesDataFrames : This script contains functions in order to create features frames from accelerometer, gyroscope and gestures data frames.
"""

########################################
# Imports
########################################
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.fftpack import fft,fft2, fftshift
from scipy.stats import skew, kurtosis, entropy
from s3_Features_Gestures import Features_Swipes
from s3_Features_Sensors import Features_Sensors
from s0_HelpFunctions import linear_regression as lr


########################################
# Initialize Functions
########################################
#--------------------------------------------------
# FeatureExtraction_Swipes : Add a swipes features in the FeautureObject
# Gesture - A swipe
# Normalize - If True normalize gestures data in a spesific screen size
# FeautureObject - The object that contains the features of the swipes, must have the shape of Features_Swipes class in s3_Features_Gestures
#--------------------------------------------------
def FeatureExtraction_Swipes(Gesture, Normalize, FeautureObject):
    
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
        length_horizontal = scalar_height * length_vertical / Gesture['D_Height']
        
    FeautureObject.setTrace_Length_Horizontal(np.abs(length_horizontal))
    FeautureObject.setTrace_Length_Vertical(np.abs(length_vertical))
    
    if (np.abs(length_horizontal) > np.abs(length_vertical)):
        if (length_horizontal > 0):
            direction = 'right'
        else:
            direction = 'left'
    else:
        if (length_vertical > 0):
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
    
    Acceleration_Horizontal = (Gesture['G_Data'][-1]['vx'] - Gesture['G_Data'][0]['vx'])/((Gesture['G_tStop'] - Gesture['G_tStart'])*0.001)
    Acceleration_Vertical = (Gesture['G_Data'][-1]['vy'] - Gesture['G_Data'][0]['vy'])/((Gesture['G_tStop'] - Gesture['G_tStart'])*0.001)
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
    
    return  FeautureObject
        
        
#--------------------------------------------------
# Create_FDF_Gest : Return data frame of swipes features
# DF_Gest - A data frame that must have the shape of Create_DF_Gestures function result in s2_CreateDataFrames
# Normalize - If True normalize gestures data in a spesific screen size
#--------------------------------------------------
def Create_FDF_Swipes(DF_Gest, Normalize):

    F_Swipes = Features_Swipes()
    
    print(flush=True)
    for idx in tqdm(range(len(DF_Gest)), desc = '-> Extracting Swipes Features'):
        G = DF_Gest.loc[idx]
        
        if (G['G_Type'] == 'swipe'):
            F_Swipes = FeatureExtraction_Swipes(G, Normalize, F_Swipes)
                
    FDF_Swipes = pd.DataFrame()
    
    FDF_Swipes['User'] = F_Swipes.getUser()
    FDF_Swipes['Screen'] = F_Swipes.getScreen()
    FDF_Swipes['Type'] = F_Swipes.getType()
    FDF_Swipes['Time_Start'] = F_Swipes.getTime_Start()
    FDF_Swipes['Time_Stop'] = F_Swipes.getTime_Stop()
    FDF_Swipes['Duration'] = F_Swipes.getDuration()
    FDF_Swipes['Trace_Length_Horizontal'] = F_Swipes.getTrace_Length_Horizontal()
    FDF_Swipes['Trace_Length_Vertical'] = F_Swipes.getTrace_Length_Vertical()
    FDF_Swipes['Direction'] = F_Swipes.getDirection()
    FDF_Swipes['Slope'] = F_Swipes.getSlope()
    FDF_Swipes['Mean_Square_Error'] = F_Swipes.getMean_Square_Error()
    FDF_Swipes['Mean_Abs_Error'] = F_Swipes.getMean_Abs_Error()
    FDF_Swipes['Median_Abs_Error'] = F_Swipes.getMedian_Abs_Error()
    FDF_Swipes['Coef_Determination'] = F_Swipes.getCoef_Determination()
    FDF_Swipes['Mean_X'] = F_Swipes.getMean_X()
    FDF_Swipes['Mean_Y'] = F_Swipes.getMean_Y()
    FDF_Swipes['Acceleration_Horizontal'] = F_Swipes.getAcceleration_Horizontal()
    FDF_Swipes['Acceleration_Vertical'] = F_Swipes.getAcceleration_Vertical()
    
    print(flush=True)
    print('-> Extracting Swipes Features Finished', end = '')
    
    return FDF_Swipes


#--------------------------------------------------
# FeatureExtraction_Sensors :
#--------------------------------------------------
def FeatureExtraction_Sensors(User, TimeStamp, Screen, Dataset, FeautureObject):
    
    Dataset_Size = Dataset.shape[0]

    if Dataset_Size > 1:
        FeautureObject.setUser(User)
        FeautureObject.setTimeStamp(TimeStamp)
        FeautureObject.setScreen(Screen)
        FeautureObject.setNum_Of_Samples(Dataset_Size)
           
        #DFT
        discreteFourier = fft(Dataset)
        # Frequencies
        freq = np.fft.fftfreq(Dataset_Size)
    
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
    
        # Time Based Feautures
        FeautureObject.setΜean(np.mean(Dataset))
        FeautureObject.setSTD(np.std(Dataset))
        FeautureObject.setMax(np.max(Dataset))
        FeautureObject.setMin(np.min(Dataset))
        FeautureObject.setRange(np.ptp(Dataset))
    
        percentile = np.percentile(Dataset, [25, 50, 75])
        FeautureObject.setPercentile25(percentile[0])
        FeautureObject.setPercentile50(percentile[1])
        FeautureObject.setPercentile75(percentile[2])
        FeautureObject.setEntropy(entropy(Dataset, base = 2))
    
        FeautureObject.setKurtosis(kurtosis(Dataset))
        FeautureObject.setSkewness(skew(Dataset))

    return  FeautureObject


#--------------------------------------------------
# Create_FDF_Sensors : Return data frames of sensors features
# DF_Users - A data frame that must have the shape same to that of findUsers_Common function result in s1_ExploreData
# DF_Acc, DF_Gyr - Data frames that must have the shape same to that of Create_DF_Sensors function result in s2_CreateDataFrames
#--------------------------------------------------
def Create_FDF_Sensors(DF_Users, DF_Acc, DF_Gyr, Feature):
    F_Acc = Features_Sensors()
    F_Gyr = Features_Sensors()
    
    print(flush=True)
    for User in tqdm(DF_Users['User'].values, desc = '-> Extracting Sensors Features'):
        List_Of_TimeStamps = DF_Users.loc[DF_Users['User'] == User]['List_Of_TimeStamps'].values[0]
        Screens_Of_TimeStamps = DF_Users.loc[DF_Users['User'] == User]['Screens_Of_TimeStamps'].values[0]
        
        for i in range(len(List_Of_TimeStamps)):
            TimeStamp = List_Of_TimeStamps[i]
            for j in range(len(Screens_Of_TimeStamps[i])):
                Screen = Screens_Of_TimeStamps[i][j]
                Data_Acc = DF_Acc.loc[(DF_Acc['User'] == User) & (DF_Acc['TimeStamp'] == TimeStamp) & (DF_Acc['Screen'] == Screen)][Feature].values
                Data_Gyr = DF_Gyr.loc[(DF_Gyr['User'] == User) & (DF_Gyr['TimeStamp'] == TimeStamp) & (DF_Gyr['Screen'] == Screen)][Feature].values     
                
                F_Acc = FeatureExtraction_Sensors(User, TimeStamp, Screen, Data_Acc, F_Acc)
                F_Gyr = FeatureExtraction_Sensors(User, TimeStamp, Screen, Data_Gyr, F_Gyr)
                
    FDF_Acc = pd.DataFrame()
    FDF_Gyr = pd.DataFrame()
    
    FDF_Acc['User'] = F_Acc.getUser()
    FDF_Acc['TimeStamp'] = F_Acc.getTimeStamp()
    FDF_Acc['Screen'] = F_Acc.getScreen()
    FDF_Acc['Num_Of_Samples'] = F_Acc.getNum_Of_Samples()
    FDF_Acc['Mean'] = F_Acc.getMean()
    FDF_Acc['STD'] = F_Acc.getSTD()
    FDF_Acc['Max'] = F_Acc.getMax()
    FDF_Acc['Min'] = F_Acc.getMin()
    FDF_Acc['Range'] = F_Acc.getRange()
    FDF_Acc['Percentile25'] = F_Acc.getPercentile25()
    FDF_Acc['Percentile50'] = F_Acc.getPercentile50()
    FDF_Acc['Percentile75'] = F_Acc.getPercentile75()
    FDF_Acc['Kurtosis'] = F_Acc.getKurtosis()
    FDF_Acc['Skewness'] = F_Acc.getSkewness()
    FDF_Acc['Entropy'] = F_Acc.getEntropy()
    FDF_Acc['Amplitude1'] = F_Acc.getAmplitude1()
    FDF_Acc['Amplitude2'] = F_Acc.getAmplitude2()
    FDF_Acc['Frequency2'] = F_Acc.getFrequency2()
    FDF_Acc['MeanFrequency'] = F_Acc.getMeanFrequency()
    
    FDF_Gyr['User'] = F_Gyr.getUser()
    FDF_Gyr['TimeStamp'] = F_Gyr.getTimeStamp()
    FDF_Gyr['Screen'] = F_Gyr.getScreen()
    FDF_Gyr['Num_Of_Samples'] = F_Gyr.getNum_Of_Samples()
    FDF_Gyr['Mean'] = F_Gyr.getMean()
    FDF_Gyr['STD'] = F_Gyr.getSTD()
    FDF_Gyr['Max'] = F_Gyr.getMax()
    FDF_Gyr['Min'] = F_Gyr.getMin()
    FDF_Gyr['Range'] = F_Gyr.getRange()
    FDF_Gyr['Percentile25'] = F_Gyr.getPercentile25()
    FDF_Gyr['Percentile50'] = F_Gyr.getPercentile50()
    FDF_Gyr['Percentile75'] = F_Gyr.getPercentile75()
    FDF_Gyr['Kurtosis'] = F_Gyr.getKurtosis()
    FDF_Gyr['Skewness'] = F_Gyr.getSkewness()
    FDF_Gyr['Entropy'] = F_Gyr.getEntropy()
    FDF_Gyr['Amplitude1'] = F_Gyr.getAmplitude1()
    FDF_Gyr['Amplitude2'] = F_Gyr.getAmplitude2()
    FDF_Gyr['Frequency2'] = F_Gyr.getFrequency2()
    FDF_Gyr['MeanFrequency'] = F_Gyr.getMeanFrequency()
    
    print(flush=True)
    print('-> Extracting Sensors Features Finished', end = '')
    
    return FDF_Acc, FDF_Gyr