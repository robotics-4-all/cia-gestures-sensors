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
from s3_Features_Sensors import Features_Sensors
from s3_Features_Gestures import Features_Swipes
from utils.help_functions import linear_regression as lr
import numpy as np
from scipy.stats import skew, kurtosis, entropy
from scipy.fftpack import fft,fft2, fftshift
import pandas as pd


########################################
# Initialize Functions
########################################
#--------------------------------------------------
# FeatureExtraction_Swipes : Add a swipes features in the FeautureObject
# Gesture - A swipe
# Output - The desired output of the spesific swipe
# Normalize - If True normalize gestures data in a spesific screen size
# FeautureObject - The object that contains the features of the swipes, must have the shape of Features_Swipes class in s3_Features_Gestures
#--------------------------------------------------
def FeatureExtraction_Swipes(Gesture, Output, Normalize, FeautureObject):
    
    scalar_width = 400
    scalar_height = 700
    
    FeautureObject.setUser(Gesture['User'])
    FeautureObject.setScreenName(Gesture['Screen'])
    
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
    
    FeautureObject.setOutput(Output)
    
    return  FeautureObject
        
        
#--------------------------------------------------
# Create_FDF_Gest : Return data frame of swipes features
# Original_User - The name of the original user
# DF_Gest - A data frame that must have the shape of Create_DF_Gestures function result in s2_CreateDataFrames
# Normalize - If True normalize gestures data in a spesific screen size
#--------------------------------------------------
def Create_FDF_Swipes(Original_User, DF_Gest, Normalize):

    F_Swipes = Features_Swipes()
    
    for idx in range(len(DF_Gest)):
        G = DF_Gest.loc[idx]
        
        if (G['G_Type'] == 'swipe'):
            User = G['User']
            
            if User == Original_User:
                F_Swipes = FeatureExtraction_Swipes(G, 1, Normalize, F_Swipes)
            else:
                F_Swipes = FeatureExtraction_Swipes(G, 0, Normalize, F_Swipes)
                
    FDF_Swipes = pd.DataFrame()
    
    FDF_Swipes['User'] = F_Swipes.getUser()
    FDF_Swipes['ScreenName'] = F_Swipes.getScreenName()
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
    FDF_Swipes['Output'] = F_Swipes.getOutput()
    
    return FDF_Swipes


#--------------------------------------------------
# FeatureExtraction_Sensors :
#--------------------------------------------------
def FeatureExtraction_Sensors(user, timestamp, dataset, samples, overlap, output, feautureObject):
    
    dataset_size = dataset.shape[0]
    i = 0
    flag = False
    
    while (dataset_size > 1):
        
        if (dataset_size <= samples):
            samples = dataset_size
            flag = True

        w = i * overlap
        end = w + samples    
            
        feautureObject.setUser(user)
        #feautureObject.setScreenName(screen)
              
        feautureObject.setTimeStamp(timestamp)
        feautureObject.setNum_Of_Samples(end - w)
           
        #DFT
        temp = dataset[w:end] # I add this line
        discreteFourier = fft(temp)
        # Frequencies
        freq = np.fft.fftfreq(samples)
    
        # Amplitudes
        idx = (np.absolute(discreteFourier)).argsort()[-2:][::-1]
        amplitude1 = np.absolute(discreteFourier[idx[0]])
        amplitude2 = np.absolute(discreteFourier[idx[1]])
        frequency2 = freq[idx[1]]
    
        # Frequency features
        mean_frequency = np.mean(freq)
        feautureObject.setAmplitude1(amplitude1)
        feautureObject.setAmplitude2(amplitude2)
        feautureObject.setFrequency2(frequency2)
        feautureObject.setMeanFrequency(mean_frequency)
    
        # Time Based Feautures
        feautureObject.setΜean(np.mean(dataset[w:end]))
        feautureObject.setSTD(np.std(dataset[w:end]))
        feautureObject.setMax(np.max(dataset[w:end]))
        feautureObject.setMin(np.min(dataset[w:end]))
        feautureObject.setRange(np.ptp(dataset[w:end]))
    
        percentile = np.percentile(dataset[w:end], [25, 50, 75])
        feautureObject.setPercentile25(percentile[0])
        feautureObject.setPercentile50(percentile[1])
        feautureObject.setPercentile75(percentile[2])
        feautureObject.setEntropy(entropy(dataset[w:end], base = 2))
    
        feautureObject.setKurtosis(kurtosis(dataset[w:end]))
        feautureObject.setSkewness(skew(dataset[w:end]))
    
        # Output Label
        feautureObject.setOutput(output)
        
        i = i + 1
        if flag:
            dataset_size = 0
        else:
            dataset_size = dataset_size - overlap        

    return  feautureObject


#--------------------------------------------------
# Create_FDF_Sensors : Return data frames of sensors features
# Original_User - The name of the original user
# DF_Users - A data frame that must have the shape same to that of findUsers_Common function result in s1_ExploreData
# DF_Acc, DF_Gyr - Data frames that must have the shape same to that of Create_DF_Sensors function result in s2_CreateDataFrames
#--------------------------------------------------
def Create_FDF_Sensors(Original_User, DF_Users, DF_Acc, DF_Gyr, Feature, WindowSize, Overlap):
    F_Acc = Features_Sensors()
    F_Gyr = Features_Sensors()
    
    for User in DF_Users['User'].values:
        List_Of_TimeStamps = DF_Users.loc[DF_Users['User'] == User]["List_Of_TimeStamps"].values[0]
        
        for i in range(len(List_Of_TimeStamps)):
            Data_Acc = DF_Acc.loc[(DF_Acc['TimeStamp'] == List_Of_TimeStamps[i]) & (DF_Acc['User'] == User)][Feature].values
            Data_Gyr = DF_Gyr.loc[(DF_Gyr['TimeStamp'] == List_Of_TimeStamps[i]) & (DF_Gyr['User'] == User)][Feature].values     
            
            if User == Original_User:
                F_Acc = FeatureExtraction_Sensors(User, List_Of_TimeStamps[i], Data_Acc, WindowSize, Overlap, 1, F_Acc)
                F_Gyr = FeatureExtraction_Sensors(User, List_Of_TimeStamps[i], Data_Gyr, WindowSize, Overlap, 1, F_Gyr)
            else:
                F_Acc = FeatureExtraction_Sensors(User, List_Of_TimeStamps[i], Data_Acc, WindowSize, Overlap, 0, F_Acc)
                F_Gyr = FeatureExtraction_Sensors(User, List_Of_TimeStamps[i], Data_Gyr, WindowSize, Overlap, 0, F_Gyr)
                
    FDF_Acc = pd.DataFrame()
    FDF_Gyr = pd.DataFrame()
    
    FDF_Acc['User'] = F_Acc.getUser()
    #FDF_Acc['ScreenName'] = F_Acc.getScreenName()
    FDF_Acc['TimeStamp'] = F_Acc.getTimeStamp()
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
    FDF_Acc['Output'] = F_Acc.getOutput()
    
    FDF_Gyr['User'] = F_Gyr.getUser()
    #FDF_Gyr['ScreenName'] = F_Gyr.getScreenName()
    FDF_Gyr['TimeStamp'] = F_Gyr.getTimeStamp()
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
    FDF_Gyr['Output'] = F_Gyr.getOutput() 
    
    return FDF_Acc, FDF_Gyr

    