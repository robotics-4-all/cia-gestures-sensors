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
# Create_DF_Sensors : Create data frames for accelerometer and gyroscope data
# SensData_Path - The directory where the sensors json file are
# DF_Users - A data frame that must have the shape of findUsers_Common function result in s1_ExploreData
# ScreenName - The type of screen
#--------------------------------------------------
def Create_DF_Sensors(SensData_Path, DF_Users, ScreenName):
    DF_Acc = pd.DataFrame(columns= ['User', 'Screen', 'TimeStamp', 'X', 'Y', 'Z', 'Magnitude', 'Combine_Angle'])
    DF_Gyr = pd.DataFrame(columns= ['User', 'Screen', 'TimeStamp', 'X', 'Y', 'Z', 'Magnitude', 'Combine_Angle'])
    
    Users = list(DF_Users['User'])
    for User in Users:
        List_Of_TimeStamps = DF_Users.loc[DF_Users['User'] == User]["List_Of_TimeStamps"].values[0]
        AccGyrSizes_Of_TimeStamps = DF_Users.loc[DF_Users['User'] == User]["AccGyrSizes_Of_TimeStamps"].values[0]
        
        for i in range(len(List_Of_TimeStamps)):
            TimeStamp = str(int(List_Of_TimeStamps[i]))
            with open(SensData_Path + "\\" + User + "_" + TimeStamp + ".json") as jsonFile:
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
                        df = {'User': User, 'Screen': Screen, 'TimeStamp': List_Of_TimeStamps[i], 'X': X, 'Y': Y, 'Z': Z, 'Magnitude': Magnitude, 'Combine_Angle': Combine_Angle}
                        DF_Acc = DF_Acc.append(df, ignore_index=True)
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
                        df = {'User': User, 'Screen': Screen, 'TimeStamp': List_Of_TimeStamps[i], 'X': X, 'Y': Y, 'Z': Z, 'Magnitude': Magnitude, 'Combine_Angle': Combine_Angle}
                        DF_Gyr = DF_Gyr.append(df, ignore_index=True)                   
                        GyrSize = GyrSize + 1
                        
    return DF_Acc, DF_Gyr      


#--------------------------------------------------
# Create_DF_Gestures : Create data frames for gestures data
# GestData_DBName - The dabase name in the mongoDB localhost:27017
# DF_Users - A data frame that must have the shape of findUsers_Common function result in s1_ExploreData
# ScreenName - The type of screen
#--------------------------------------------------
def Create_DF_Gestures(GestData_DBName, DF_Users, ScreenName):
    DF_Gest = pd.DataFrame(columns= ['User', 'Screen', 'G_ID', 'G_Type', 'G_tStart', 'G_tStop', 'G_Duration', 'G_Data', 'D_Height', 'D_Width'])
    
    m = MongoDBHandler('mongodb://localhost:27017/', GestData_DBName)
    d = DBDataHandler(m)
    
    Users = list(DF_Users['User'])
    for User in Users:
        G_IDs = DF_Users.loc[DF_Users['User'] == User]["Gestures_IDs"].values[0]
        
        for i in range(len(G_IDs)):
            G_ID = G_IDs[i]
            G = d.get_gestures({'_id':ObjectId(G_ID)})
            Screen = G[0]['screen']
            G_Type = G[0]['type']
            G_tStart = G[0]['t_start']
            G_tStop = G[0]['t_stop']
            G_Duration = G_tStop - G_tStart
            G_Data = G[0]['data']
            
            D_ID = G[0]['device_id']            
            D = d.get_devices({'device_id':D_ID})
            D_Height = D[0]['height']
            D_Width = D[0]['width']
            
            df = {'User': User, 'Screen': Screen, 'G_ID': G_ID, 'G_Type': G_Type, 'G_tStart': G_tStart, 'G_tStop': G_tStop, 'G_Duration': G_Duration, 'G_Data': G_Data, 'D_Height': D_Height, 'D_Width': D_Width}
            DF_Gest = DF_Gest.append(df, ignore_index=True)
            
    return DF_Gest      

