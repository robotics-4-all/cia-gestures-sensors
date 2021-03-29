"""
Aristotle University of Thessaloniki
Intelligent Systems & Software Engineering Labgroup

Author : Christos Emmanouil

Thesis : Continuous implicit authentication of mobile phone users with a combination of navigation and behavior data.

DataFramesCreator : This script contains functions in order to create accelerometer, gyroscope and gestures data frames.
"""
########################################
# Imports
########################################
import pandas as pd
import ujson as json
import numpy as np
from utils.MongoDBHandler import MongoDBHandler
from utils.DBDataHandler import DBDataHandler
from bson.objectid import ObjectId

########################################
# Initialize Functions
########################################
#--------------------------------------------------
# create_AcGr_DFs_NotGesSyn : Create data frames for accelerometer and gyroscope data
# SensorsData_Path - The directory where the sensors json file are
# DF_valUsers - A data frame of the users, the data frame must have the shape of a NoSyced result of findUsers_SGdata function in s1_DataExplorer
# ScreenName - The type of screen
#--------------------------------------------------
def create_AcGr_DFs_NotGesSyn(SensorsData_Path, DF_valUsers, ScreenName):
    DF_Accelerometer = pd.DataFrame(columns= ['Screen', 'User', 'Timestamp', 'X', 'Y', 'Z', 'Magnitude', 'Combine_Angle'])
    DF_Gyroscope = pd.DataFrame(columns= ['Screen', 'User', 'Timestamp', 'X', 'Y', 'Z', 'Magnitude', 'Combine_Angle'])
    
    users = list(DF_valUsers['User'])
    for user in users:
        List_Of_TimeStamps = DF_valUsers.loc[DF_valUsers['User'] == user]["List_Of_TimeStamps"].values[0]
        AccGyrSizes_Of_TimeStamps = DF_valUsers.loc[DF_valUsers['User'] == user]["AccGyrSizes_Of_TimeStamps"].values[0]
        
        for i in range(len(List_Of_TimeStamps)):
            timestamp = str(int(List_Of_TimeStamps[i]))
            with open(SensorsData_Path + "\\" + user + "_" + timestamp + ".json") as jsonFile:
                json_text = json.load(jsonFile)
                
                AccSize = 0
                for j in json_text['accelerometer']:
                    # Incase the sensors data (accelerometer, gyroscope) are synced together, the AccGyrSizes_Of_TimeStamps contains the correct number of data needed
                    if (AccSize == AccGyrSizes_Of_TimeStamps[i][0]):
                        break
                    if ScreenName in j['screen']:
                        Screen = j['screen']
                        X = j['x']
                        Y = j['y']
                        Z = j['z']
                        if X == 0 and Y == 0:
                            continue
                        Magnitude = np.sqrt(X**2 + Y**2 + Z**2)
                        Combine_Angle = np.sqrt(Y**2 + Z**2)
                        df = {'Screen': Screen, 'User': user, 'Timestamp': List_Of_TimeStamps[i], 'X': X, 'Y': Y, 'Z': Z, 'Magnitude': Magnitude, 'Combine_Angle': Combine_Angle}
                        DF_Accelerometer = DF_Accelerometer.append(df, ignore_index=True)
                        AccSize = AccSize + 1
                
                GyrSize = 0
                for j in json_text['gyroscope']:
                    if (GyrSize == AccGyrSizes_Of_TimeStamps[i][1]):
                        break
                    if ScreenName in j['screen']:
                        Screen = j['screen']
                        X = j['x']
                        Y = j['y']
                        Z = j['z']
                        if X == 0 and Y == 0:
                            continue
                        Magnitude = np.sqrt(X**2 + Y**2 + Z**2)
                        Combine_Angle = np.sqrt(Y**2 + Z**2)
                        df = {'Screen': Screen, 'User': user, 'Timestamp': List_Of_TimeStamps[i], 'X': X, 'Y': Y, 'Z': Z, 'Magnitude': Magnitude, 'Combine_Angle': Combine_Angle}
                        DF_Gyroscope = DF_Gyroscope.append(df, ignore_index=True)                   
                        GyrSize = GyrSize + 1
                        
    return DF_Accelerometer, DF_Gyroscope 


#--------------------------------------------------
# create_AcGr_DFs_GesSyn : Create data frames for accelerometer and gyroscope data which are synced with gestures
# SensorsData_Path - The directory where the sensors json file are
# DF_valUsers - A data frame of the users, the data frame must have the shape of a Syced result of findUsers_SGdata function in s1_DataExplorer
# ScreenName - The type of screen
#--------------------------------------------------
def create_AcGr_DFs_GesSyn(SensorsData_Path, DF_valUsers, ScreenName):
    DF_Accelerometer = pd.DataFrame(columns= ['Screen', 'User', 'Timestamp', 'X', 'Y', 'Z', 'Magnitude', 'Combine_Angle', 'Gesture_ID'])
    DF_Gyroscope = pd.DataFrame(columns= ['Screen', 'User', 'Timestamp', 'X', 'Y', 'Z', 'Magnitude', 'Combine_Angle', 'Gesture_ID'])
    
    users = list(DF_valUsers['User'])
    for user in users:
        Gestures_IDs = DF_valUsers.loc[DF_valUsers['User'] == user]["Gestures_IDs"].values[0]
        List_Of_TimeStamps_per_Gesture = DF_valUsers.loc[DF_valUsers['User'] == user]["List_Of_TimeStamps_per_Gesture"].values[0]
        AccGyrSizes_Of_TimeStamps_per_Gesture = DF_valUsers.loc[DF_valUsers['User'] == user]["AccGyrSizes_Of_TimeStamps_per_Gesture"].values[0]
        
        for i in range(len(Gestures_IDs)):
            Gestures_ID = Gestures_IDs[i]
            Gesture_List_Of_TimeStamps = List_Of_TimeStamps_per_Gesture[i]
            Gesture_AccGyrSizes_Of_TimeStamps = AccGyrSizes_Of_TimeStamps_per_Gesture[i]
            
            for k in range(len(Gesture_List_Of_TimeStamps)):
                timestamp = str(int(Gesture_List_Of_TimeStamps[k]))
                with open(SensorsData_Path + "\\" + user + "_" + timestamp + ".json") as jsonFile:
                    json_text = json.load(jsonFile)
                    
                AccSize = 0
                for j in json_text['accelerometer']:
                    # The sensors data (accelerometer, gyroscope) are synced together, the AccGyrSizes_Of_TimeStamps contains the correct number of data needed
                    if (AccSize == Gesture_AccGyrSizes_Of_TimeStamps[k][0]):
                        break
                    if ScreenName in j['screen']:
                        Screen = j['screen']
                        X = j['x']
                        Y = j['y']
                        Z = j['z']
                        if X == 0 and Y == 0:
                            continue
                        Magnitude = np.sqrt(X**2 + Y**2 + Z**2)
                        Combine_Angle = np.sqrt(Y**2 + Z**2)
                        df = {'Screen': Screen, 'User': user, 'Timestamp': Gesture_List_Of_TimeStamps[k], 'X': X, 'Y': Y, 'Z': Z, 'Magnitude': Magnitude, 'Combine_Angle': Combine_Angle, 'Gesture_ID': Gestures_ID}
                        DF_Accelerometer = DF_Accelerometer.append(df, ignore_index=True)
                        AccSize = AccSize + 1
                
                GyrSize = 0
                for j in json_text['gyroscope']:
                    if (GyrSize == Gesture_AccGyrSizes_Of_TimeStamps[k][1]):
                        break
                    if ScreenName in j['screen']:
                        Screen = j['screen']
                        X = j['x']
                        Y = j['y']
                        Z = j['z']
                        if X == 0 and Y == 0:
                            continue
                        Magnitude = np.sqrt(X**2 + Y**2 + Z**2)
                        Combine_Angle = np.sqrt(Y**2 + Z**2)
                        df = {'Screen': Screen, 'User': user, 'Timestamp': Gesture_List_Of_TimeStamps[k], 'X': X, 'Y': Y, 'Z': Z, 'Magnitude': Magnitude, 'Combine_Angle': Combine_Angle, 'Gesture_ID': Gestures_ID}
                        DF_Gyroscope = DF_Gyroscope.append(df, ignore_index=True)                   
                        GyrSize = GyrSize + 1   
                        
    return DF_Accelerometer, DF_Gyroscope               


#--------------------------------------------------
# create_AcGr_DFs : Create data frames for accelerometer and gyroscope data (Synced or Not Synced with gestures)
# SensorsData_Path - The directory where the sensors json file are
# ScreenName - The type of screen
# DF_valUsers - A data frame of the users, the data frame can have the shape of a Synced or Not Synced result of findUsers_SGdata function in s1_DataExplorer
# synced_SGData - A boolean that is True if the DF_valUsers is Synced or False if the DF_valUsers is Not Synced
#--------------------------------------------------   
def create_AcGr_DFs(SensorsData_Path, ScreenName, DF_valUsers, synced_SGData):
    
    if synced_SGData:
        DF_Accelerometer, DF_Gyroscope = create_AcGr_DFs_GesSyn(SensorsData_Path, DF_valUsers, ScreenName)
    else:
        DF_Accelerometer, DF_Gyroscope = create_AcGr_DFs_NotGesSyn(SensorsData_Path, DF_valUsers, ScreenName)
        
    return DF_Accelerometer, DF_Gyroscope
        

#--------------------------------------------------
# create_Ge_DFs : Create data frames for gestures data
# GesturesData_DatabaseName - The dabase name in the mongoDB localhost:27017
# DF_valUsers - A data frame of the users, the data frame can have the shape of a Synced or Not Synced result of findUsers_SGdata function in s1_DataExplorer
# ScreenName - The type of screen
#--------------------------------------------------
def create_Ge_DFs(GesturesData_DatabaseName, DF_valUsers, ScreenName):
    DF_Gestures = pd.DataFrame(columns= ['Screen', 'User', 'Gesture_ID', 'T_Start', 'T_Stop', 'Gesture_Data', 'Device_Height', 'Device_Width'])
    
    m = MongoDBHandler('mongodb://localhost:27017/', GesturesData_DatabaseName)
    d = DBDataHandler(m)
    
    users = list(DF_valUsers['User'])
    for user in users:
        Gestures_IDs = DF_valUsers.loc[DF_valUsers['User'] == user]["Gestures_IDs"].values[0]
        
        for i in range(len(Gestures_IDs)):
            Gesture_ID = Gestures_IDs[i]

            ges = d.get_gestures({'_id':ObjectId(Gesture_ID)})
            T_Start = ges[0]['t_start']
            T_Stop = ges[0]['t_stop']
            Screen = ges[0]['screen']
            Gesture_Data = ges[0]['data']
            Device_ID = ges[0]['device_id']
            
            dev = d.get_devices({'device_id':Device_ID})
            Device_Height = dev[0]['height']
            Device_Width = dev[0]['width']
            
            df = {'Screen': Screen, 'User': user, 'Gesture_ID': Gesture_ID, 'T_Start': T_Start, 'T_Stop': T_Stop, 'Gesture_Data': Gesture_Data, 'Device_Height': Device_Height, 'Device_Width': Device_Width}
            DF_Gestures = DF_Gestures.append(df, ignore_index=True)
            
    return DF_Gestures        

    
#--------------------------------------------------
# Create_SensorsGestures_DataFrames : Create data frames for accelerometer, gyroscope and gestures data
# SensorsData_Path - The directory where the sensors json file are
# GesturesData_DatabaseName - The dabase name in the mongoDB localhost:
# ScreenName - The type of screen
# Valid_Users_DataFrame - A data frame of the users, the data frame can have the shape of a Synced or Not Synced result of findUsers_SGdata function in s1_DataExplorer
# Is_SensorsGestures_Synced - A boolean that is True if the Valid_Users_DataFrame is Synced or False if the Valid_Users_DataFrame is Not Synced
def Create_SensorsGestures_DataFrames(SensorsData_Path, GesturesData_DatabaseName, ScreenName, Valid_Users_DataFrame, Is_SensorsGestures_Synced):
    DF_Accelerometer, DF_Gyroscope = create_AcGr_DFs(SensorsData_Path, ScreenName, Valid_Users_DataFrame, Is_SensorsGestures_Synced)
    DF_Gestures = create_Ge_DFs(GesturesData_DatabaseName, Valid_Users_DataFrame, ScreenName)
    return DF_Accelerometer, DF_Gyroscope, DF_Gestures
